#!/usr/bin/env python3
"""캐릭터 스프라이트 누끼·정렬·WebP 내보내기, 배경 리사이즈.

스프라이트는 단색 회색(#dcdcdc) 배경에서 생성한다. 흰 배경에서 생성하면
흰 블라우스·셔츠가 배경과 함께 지워지기 때문이다. 배경색은 네 모서리에서
읽어 테두리부터 연결된 영역만 지운다.
"""
import os
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFilter

RAW = "assets/raw"
OUT = "assets/img"

CHARS = {
    "seoyun": ["base", "blush", "surprised", "serious"],
    "haram": ["base", "blush", "surprised", "serious"],
}
BGS = ["bg_office_day", "bg_rooftop_sunset", "bg_office_night", "bg_store_night"]

ERODE, BLUR = 5, 0.6


def alpha_of(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape

    corners = np.array([a[2, 2], a[2, w - 3], a[h - 3, 2], a[h - 3, w - 3]])
    bgc = np.median(corners, axis=0)
    dist = np.abs(a - bgc).sum(axis=2)
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    cand = (dist < 30) | ((mx < 247) & (mx > 190) & ((mx - mn) < 10))

    m = Image.fromarray(np.where(cand, 255, 0).astype(np.uint8), "L")
    padded = Image.new("L", (w + 2, h + 2), 255)
    padded.paste(m, (1, 1))
    ImageDraw.floodfill(padded, (0, 0), 128, thresh=0)
    bg = (np.asarray(padded) == 128)[1:-1, 1:-1]

    al = Image.fromarray(np.where(~bg, 255, 0).astype(np.uint8), "L")
    al = al.filter(ImageFilter.MinFilter(ERODE)).filter(ImageFilter.GaussianBlur(BLUR))

    alpha = np.asarray(al).astype(np.float32)
    rgb = np.asarray(im).astype(np.float32)

    # 테두리에 붙어 남은 흰 조각(손가락 사이, 머리카락 옆)을 지운다.
    # 흰 블라우스·운동화처럼 큰 흰 영역은 건드리지 않는다.
    near_white = rgb.min(axis=2) > 243
    edge_zone = ndimage.binary_dilation(alpha < 40, iterations=5)
    junk = near_white & edge_zone & (alpha > 0)
    lab, n = ndimage.label(junk)
    for idx in range(1, n + 1):
        comp = lab == idx
        if int(comp.sum()) < 4000:
            alpha[comp] = 0
    alpha = ndimage.gaussian_filter(alpha, 0.5)

    core = alpha > 235
    filled = rgb.copy()
    have = core.copy()
    for _ in range(16):
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s_rgb = np.roll(filled, (dy, dx), axis=(0, 1))
            s_have = np.roll(have, (dy, dx), axis=(0, 1))
            take = (~have) & s_have
            filled[take] = s_rgb[take]
            have = have | take
    edge = (~core) & (alpha > 0)
    out = rgb.copy()
    out[edge] = filled[edge]

    arr = np.dstack([out.astype(np.uint8), alpha.astype(np.uint8)])
    return Image.fromarray(arr, "RGBA")


def main():
    os.makedirs(OUT, exist_ok=True)

    # 두 캐릭터의 머리 위·발 아래 기준을 맞추기 위해 공통 높이로 정규화한다.
    TARGET_H = 1500

    for name, exprs in CHARS.items():
        base = alpha_of(os.path.join(RAW, f"ch_{name}_base.png"))
        bbox = base.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        pad = 8
        box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
               min(base.width, bbox[2] + pad), min(base.height, bbox[3] + pad))
        size = (box[2] - box[0], box[3] - box[1])
        tw = round(size[0] * TARGET_H / size[1])
        for e in exprs:
            rgba = alpha_of(os.path.join(RAW, f"ch_{name}_{e}.png"))
            rgba = rgba.crop(box).resize((tw, TARGET_H), Image.LANCZOS)
            out = os.path.join(OUT, f"{name}_{e}.webp")
            rgba.save(out, "WEBP", quality=90, method=6)
            print(f"{name}_{e}", rgba.size, os.path.getsize(out))

    for b in BGS:
        im = Image.open(os.path.join(RAW, f"{b}.png")).convert("RGB")
        im = im.resize((1536, 864), Image.LANCZOS)
        out = os.path.join(OUT, f"{b.replace('bg_', '')}.webp")
        im.save(out, "WEBP", quality=86, method=6)
        print(b, os.path.getsize(out))


if __name__ == "__main__":
    main()
