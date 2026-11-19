#!/usr/bin/env python3
"""Scenario authoring DSL + JSON builder.

Each scene module exposes build(S). S.line() appends a node; by default a node
flows into the next appended node. S.choice() attaches choices to the previous
line. Labels make jump targets readable; they are resolved at the end.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import s0_prologue, s1_day1, s2_day2, s3_night1, s4_store, s5_final  # noqa: E402

MODULES = (s0_prologue, s1_day1, s2_day2, s3_night1, s4_store, s5_final)


class Scene:
    def __init__(self):
        self.nodes = []
        self.labels = {}
        self.used_ids = set()

    # ---- primitives -------------------------------------------------
    def line(self, text=None, who=None, e=None, bg=None, ch=None, show=None,
             hide=False, bgm=None, weather=None, fx=None, eff=None,
             ending=None, choices=None, show2=None, hide2=False, rain=None):
        nid = "n%03d" % (len(self.nodes) + 1)
        node = {}
        if who:
            node["who"] = who
        if text:
            node["text"] = text
        if e:
            node["e"] = e
        if bg:
            node["bg"] = bg
        if ch:
            node["ch"] = ch
        if show:
            node["show"] = show
        if hide:
            node["hide"] = True
        if show2:
            node["show2"] = show2
        if hide2:
            node["hide2"] = True
        if bgm:
            node["bgm"] = bgm
        if weather:
            node["weather"] = weather
        if fx:
            node["fx"] = fx
        if ending:
            node["ending"] = ending
        if choices:
            node["choices"] = choices
        if rain is not None:
            node["rain"] = rain
        self.nodes.append({"id": nid, "node": node})
        return nid

    def label(self, name):
        if name in self.labels:
            raise SystemExit("duplicate label: %s" % name)
        self.labels[name] = "n%03d" % (len(self.nodes) + 1)

    def choice(self, options, prompt=None):
        """Attach choices to the last line node."""
        last = self.nodes[-1]
        last["node"]["choices"] = options
        return last["id"]

    def goto(self, label):
        nid = "n%03d" % (len(self.nodes) + 1)
        self.nodes.append({"id": nid, "node": {"goto": "@" + label}})
        return nid

    def branch(self, rules):
        """rules: list of (cond, label). Last entry should be (None, label)."""
        nid = "n%03d" % (len(self.nodes) + 1)
        self.nodes.append({"id": nid, "node": {"branch": rules}})
        return nid

    # ---- finalize ---------------------------------------------------
    def finish(self):
        out = {}
        nodes = self.nodes
        label_targets = {v: k for k, v in self.labels.items()}

        for i, item in enumerate(nodes):
            n = item["node"]
            if "goto" in n:
                n["next"] = n.pop("goto")
            if "branch" in n:
                n["branch"] = [
                    {"if": c, "next": "@" + t} if c else {"next": "@" + t}
                    for c, t in n["branch"]
                ]
            if "choices" in n:
                for c in n["choices"]:
                    if "to" in c:
                        c["next"] = "@" + c.pop("to")
            # implicit next: the following node
            if ("next" not in n and "choices" not in n and "branch" not in n
                    and "ending" not in n and i + 1 < len(nodes)):
                n["next"] = nodes[i + 1]["id"]

        # resolve @label
        for item in nodes:
            n = item["node"]

            def ref(v):
                if isinstance(v, str) and v.startswith("@"):
                    key = v[1:]
                    if key not in self.labels:
                        raise SystemExit("unknown label: %s" % key)
                    return self.labels[key]
                return v

            if "next" in n:
                n["next"] = ref(n["next"])
            if "branch" in n:
                for b in n["branch"]:
                    b["next"] = ref(b["next"])
            if "choices" in n:
                for c in n["choices"]:
                    c["next"] = ref(c["next"])

        meta = META
        meta["count"] = len(nodes)
        for item in nodes:
            out[item["id"]] = item["node"]
        meta["start"] = nodes[0]["id"]
        meta["labelIndex"] = label_targets
        return {"meta": meta, "nodes": out}


META = {
    "title": "퇴근 삼십 분 전",
    "subtitle": "성수동 12층, 수습 마지막 주",
    "affMax": 20,
    "heroines": {
        "seoyun": {"name": "한서윤", "role": "프로덕트 팀장 · 5년차", "color": "#2f4f7f"},
        "haram": {"name": "오하람", "role": "프로덕트 디자이너 · 입사 동기", "color": "#e07a5f"},
    },
    "endings": {
        "seoyun_happy": {
            "no": "01", "label": "HAPPY END", "title": "리뷰는 내일, 대답은 오늘",
            "desc": "규칙은 심사 자리에서만 적용된다. 심사가 끝난 옥상에서, 그녀가 만든 규칙을 오늘부터 둘이 고쳐 쓰기로 했다.",
        },
        "seoyun_normal": {
            "no": "02", "label": "NORMAL END", "title": "다음 스프린트",
            "desc": "삼십 분은 말하기에 조금 짧았다. 다음 주에도 그녀는 팀장이고, 창가 자리의 스탠드는 여전히 밤늦게 켜진다.",
        },
        "haram_happy": {
            "no": "03", "label": "HAPPY END", "title": "계약 연장",
            "desc": "편의점 벤치에서 아이스크림 하나를 나눠 먹었다. 월요일부터 같은 팀, 그리고 계속.",
        },
        "haram_normal": {
            "no": "04", "label": "NORMAL END", "title": "마지막 프레임",
            "desc": "두 달 뒤, 그녀는 계단참에 그림 한 장을 두고 갔다. 이름은 마지막프레임.png. 설명은 없었다.",
        },
        "true_end": {
            "no": "05", "label": "TRUE END", "title": "제9조를 고쳐 쓰는 방법",
            "desc": "덮어 준 사람이 있으면 먼저 밝힌다. 이유를 먼저 묻는다. 셋이서 규칙을 고쳐 쓰고, 그다음에 우리 사이를 생각하기로 했다.",
        },
    },
}


def main():
    S = Scene()
    for mod in MODULES:
        mod.build(S)
    data = S.finish()
    out = os.path.join(os.path.dirname(__file__), "..", "src", "data", "scenario.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", out, len(data["nodes"]), "nodes", len(data["meta"]["endings"]), "endings")


if __name__ == "__main__":
    main()
