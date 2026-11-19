#!/usr/bin/env python3
"""시나리오 전수 검사.

1) 구조: 끊깅 링크, 막다른 길, 잘못된 엔딩/배경/캐릭터, 선택지 개수
2) 도달성: 조건을 무시한 그래프 탐색으로 고아 노드 찾기
3) 플레이 검증: 무작위·전략적 플레이를 수천 번 돌려 모든 엔딩 도달 여부,
   막다른 길, 무한 루프, 호감도 최대치 확인
4) 문장 점검: 번역체·맞춤법·부호 패턴
"""
import json
import os
import random
import re
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "src", "data", "scenario.json")

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)
nodes = data["nodes"]
meta = data["meta"]

BGS = ("office_day", "rooftop_sunset", "office_night", "store_night")
AFF = ("seoyun", "haram")
errors, warnings = [], []


# ---------- 1. 구조 ----------
for nid, n in nodes.items():
    targets = []
    if n.get("next"):
        targets.append(n["next"])
    for c in n.get("choices", []):
        targets.append(c["next"])
    for b in n.get("branch", []):
        targets.append(b["next"])
    for t in targets:
        if t not in nodes:
            errors.append("broken link %s -> %s" % (nid, t))
    if (not n.get("text") and not n.get("choices") and not n.get("branch")
            and not n.get("ending") and not n.get("next")):
        errors.append("node %s has no text/choices/ending" % nid)
    if not n.get("ending") and not n.get("next") and not n.get("choices") and not n.get("branch"):
        errors.append("dead end at %s" % nid)
    if n.get("ending") and n["ending"] not in meta["endings"]:
        errors.append("unknown ending %s at %s" % (n["ending"], nid))
    if n.get("choices") and len(n["choices"]) < 2:
        errors.append("choice with <2 options at %s" % nid)
    if n.get("show") and n["show"]["id"] not in meta["heroines"]:
        errors.append("unknown character %s at %s" % (n["show"]["id"], nid))
    if n.get("show2") and n["show2"]["id"] not in meta["heroines"]:
        errors.append("unknown character %s at %s" % (n["show2"]["id"], nid))
    if n.get("bg") and n["bg"] not in BGS:
        errors.append("unknown bg %s at %s" % (n["bg"], nid))
    if n.get("branch") and not n["branch"]:
        errors.append("empty branch at %s" % nid)
    if n.get("who") and n["who"] not in ("나", "한서윤", "오하람") and n["who"] not in (
            "최규진", "박도현", "이지수"):
        errors.append("unknown speaker %s at %s" % (n["who"], nid))


# ---------- 2. 고아 노드 ----------
reach = set()
q = deque([meta["start"]])
while q:
    cur = q.popleft()
    if cur in reach:
        continue
    reach.add(cur)
    n = nodes.get(cur)
    if not n:
        continue
    for t in ([n.get("next")] + [c.get("next") for c in n.get("choices", [])]
              + [b.get("next") for b in n.get("branch", [])]):
        if t and t not in reach:
            q.append(t)
orphans = [i for i in nodes if i not in reach]
if orphans:
    errors.append("unreachable nodes: %s" % ", ".join(orphans[:12]))


# ---------- 3. 플레이 검증 ----------
def test_cond(c, aff, flags):
    if not c:
        return True
    if c.get("flag") and c["flag"] not in flags:
        return False
    if c.get("flag2") and c["flag2"] not in flags:
        return False
    if c.get("noflag") and c["noflag"] in flags:
        return False
    for k, v in (c.get("affMin") or {}).items():
        if aff.get(k, 0) < v:
            return False
    for k, v in (c.get("affMax") or {}).items():
        if aff.get(k, 0) > v:
            return False
    return True


def play(pick, limit=4000):
    """pick(node, usable_choices, aff, flags) -> choice index"""
    aff = {"seoyun": 0, "haram": 0}
    flags = set()
    seen = set()
    cur = meta["start"]
    steps = 0
    while True:
        steps += 1
        if steps > limit:
            return None, aff, flags, steps, "loop"
        n = nodes.get(cur)
        if n is None:
            return None, aff, flags, steps, "missing %s" % cur
        if cur in seen and not n.get("ending"):
            return None, aff, flags, steps, "loop at %s" % cur
        seen.add(cur)
        if n.get("branch"):
            nxt = None
            for b in n["branch"]:
                if test_cond(b.get("if"), aff, flags):
                    nxt = b["next"]
                    break
            if nxt is None:
                nxt = n["branch"][-1]["next"]
            cur = nxt
            continue
        if n.get("ending"):
            return n["ending"], aff, flags, steps, None
        if n.get("choices"):
            usable = [c for c in n["choices"] if test_cond(c.get("when"), aff, flags)]
            if not usable:
                return None, aff, flags, steps, "no option at %s" % cur
            c = usable[pick(n, usable, aff, flags) % len(usable)]
            if c.get("eff"):
                for k in AFF:
                    if c["eff"].get(k):
                        aff[k] = aff.get(k, 0) + c["eff"][k]
            if c.get("flag"):
                flags.add(c["flag"])
            cur = c["next"]
            continue
        if n.get("eff"):
            for k in AFF:
                if n["eff"].get(k):
                    aff[k] = aff.get(k, 0) + n["eff"][k]
        if not n.get("next"):
            return None, aff, flags, steps, "dead end %s" % cur
        cur = n["next"]


rng = random.Random(20261119)
endings_hit = {}
max_aff = {"seoyun": 0, "haram": 0}
bad = []


def note(end, aff, steps, err):
    if err:
        bad.append(err)
        return
    endings_hit[end] = endings_hit.get(end, 0) + 1
    for k in max_aff:
        max_aff[k] = max(max_aff[k], aff[k])


for i in range(4000):
    end, aff, flags, steps, err = play(lambda n, u, a, f: rng.randrange(len(u)))
    note(end, aff, steps, err)


def strongest(key):
    def pick(n, usable, aff, flags):
        best, bi = -999, 0
        for i, c in enumerate(usable):
            score = (c.get("eff") or {}).get(key, 0) * 2
            if c.get("flag") in ("seo_note", "haram_truth", "haram_contract"):
                score += 1
            if score > best:
                best, bi = score, i
        return bi
    return pick


for key in AFF:
    for _ in range(50):
        end, aff, flags, steps, err = play(strongest(key))
        note(end, aff, steps, err)


def true_pick(n, usable, aff, flags):
    want = {"seo_note", "haram_truth"}
    best, bi = -999, 0
    for i, c in enumerate(usable):
        fl = c.get("flag")
        score = 0
        if fl in want and fl not in flags:
            score += 4
        eff = c.get("eff") or {}
        score += min(eff.get("seoyun", 0), eff.get("haram", 0)) * 3
        score += (eff.get("seoyun", 0) + eff.get("haram", 0)) * 0.4
        if score > best:
            best, bi = score, i
    return bi


for _ in range(80):
    end, aff, flags, steps, err = play(true_pick)
    note(end, aff, steps, err)

if bad:
    counts = {}
    for b in bad:
        counts[b] = counts.get(b, 0) + 1
    for b, c in list(counts.items())[:8]:
        errors.append("play issue x%d: %s" % (c, b))

for e in meta["endings"]:
    if e not in endings_hit:
        errors.append("ending never reached: %s" % e)

# ---------- 4. 문장 점검 ----------
TECH = ["PR", "QA", "API", "CSS", "NaN", "Figma", "URL", "UI", "UX", "IT", "CTO",
        "Invalid Date", "png"]
BAD = [
    (r"당신", '번역체 "당신"'),
    (r"그것은|그것을|그것이 ", "지시대명사 번역체"),
    (r"할 수 있을 것이다", "번역체"),
    (r"되어진|되어지는", "이중 피동"),
    (r"  +", "연속 공백"),
    (r"되요|안되요|됬", "맞춤법(되/돼)"),
    (r"[!?]{2,}", "중복 문장부호"),
    (r"(?<!L)[a-zA-Z]{2,}", "영문 혼입"),
    (r"\.\.\.", "... 사용(… 권장)"),
    (r"ㅋ", "ㅋㅋ체"),
    (r"있었음|했음\.", "구어체 종결"),
]
lint = 0
for nid, n in nodes.items():
    texts = [n.get("text")] + [c.get("t") for c in n.get("choices", [])]
    for t in texts:
        if not t:
            continue
        for w in TECH:
            t = t.replace(w, "가" * len(w))
        for pat, label in BAD:
            if re.search(pat, t):
                warnings.append("%s %s: %s" % (nid, label, t[:44].replace("\n", " ")))
                lint += 1
    if n.get("text") and len(n["text"]) > 190:
        warnings.append("%s 긴 대사 (%d자)" % (nid, len(n["text"])))

# ---------- 5. 보고 ----------
choice_nodes = [n for n in nodes.values() if n.get("choices")]
chars = sum(len(n.get("text") or "") for n in nodes.values())

print("-" * 56)
print("nodes            :", len(nodes))
print("reachable        :", len(reach))
print("choice points    :", len(choice_nodes), "/ options:",
      sum(len(n["choices"]) for n in choice_nodes))
print("endings reached  :", ", ".join("%s x%d" % (k, v) for k, v in sorted(endings_hit.items())))
print("max affinity     : seoyun %d / haram %d" % (max_aff["seoyun"], max_aff["haram"]))
print("script length    :", chars, "chars")
print("lint warnings    :", lint)
print("-" * 56)

if warnings:
    print("\n[warnings]")
    for w in warnings[:40]:
        print(" ·", w)
    if len(warnings) > 40:
        print(" … +%d" % (len(warnings) - 40))

if errors:
    print("\n[errors]")
    for e in errors:
        print(" ✕", e)
    sys.exit(1)

print("\n✓ 구조 검사 통과 — 끊긴 링크·막다른 길·고아 노드·도달 불가 엔딩 없음")
