#!/usr/bin/env python3
"""대사 화자와 화면에 서 있는 캐릭터가 어긋나는 지점을 찾는다."""
import json, os
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "..", "src", "data", "scenario.json"), encoding="utf-8"))
nodes, meta = data["nodes"], data["meta"]

WHO = {"한서윤": "seoyun", "오하람": "haram"}


def test(c, aff, flags):
    if not c:
        return True
    if c.get("flag") and c["flag"] not in flags:
        return False
    if c.get("flag2") and c["flag2"] not in flags:
        return False
    for k, v in (c.get("affMin") or {}).items():
        if aff.get(k, 0) < v:
            return False
    return True


seen = set()
queue = deque([(meta["start"], {}, frozenset(), (None, None))])
issues = []
guard = 0
while queue:
    nid, aff, flags, who = queue.popleft()
    while True:
        guard += 1
        if guard > 400000:
            break
        n = nodes.get(nid)
        if not n:
            break
        main, side = who
        if n.get("hide"):
            main, side = None, None
        if n.get("hide2"):
            side = None
        if n.get("show"):
            main = n["show"]["id"]
        if n.get("show2"):
            side = n["show2"]["id"]
        who = (main, side)
        spk = WHO.get(n.get("who"))
        if spk and spk not in who:
            issues.append((nid, n.get("who"), who, (n.get("text") or "")[:46]))
            main = spk
            who = (main, side)
        if n.get("ending"):
            break
        if n.get("choices"):
            for c in n["choices"]:
                k = (c["next"], aff.get("seoyun", 0), aff.get("haram", 0), flags, who)
                if k not in seen and test(c.get("when"), aff, flags):
                    seen.add(k)
                    a2 = dict(aff)
                    for kk, vv in (c.get("eff") or {}).items():
                        a2[kk] = a2.get(kk, 0) + vv
                    f2 = set(flags)
                    if c.get("flag"):
                        f2.add(c["flag"])
                    queue.append((c["next"], a2, frozenset(f2), who))
            break
        nid2 = n.get("next")
        k = (nid2, aff.get("seoyun", 0), aff.get("haram", 0), flags, who)
        if k in seen:
            break
        seen.add(k)
        if not nid2:
            break
        nid = nid2

print("mismatch lines:", len(issues))
for i in issues:
    print(" ", i[0], "화자=%s / 화면=%s | %s" % i[1:])
