"""Plain-assert self-check. Run: python3 tests/test_core.py"""
import importlib.machinery
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "bin" / "grasp"
loader = importlib.machinery.SourceFileLoader("grasp", str(BIN))
g = importlib.util.module_from_spec(importlib.util.spec_from_loader("grasp", loader))
loader.exec_module(g)

# --- pure functions ---
assert g.leitner(0, 2) == 1 and g.leitner(4, 2) == 4 and g.leitner(3, 1) == 3 and g.leitner(3, 0) == 0
assert g.ema(None, 2) == 1.0 and g.ema(1.0, 0) == 0.7
assert g.parse_block('text\n```grasp\n{"concepts":["a/b"]}\n```') == {"concepts": ["a/b"]}
assert g.parse_block("no block") is None and g.parse_block("```grasp\nnot json\n```") is None
assert g.check_why("feat: x\n\nWHY: " + "word " * 15) is None
assert g.check_why("feat: x\n\nWHY: too short") is not None
assert g.check_why("Merge branch 'main'") is None


def ds(level=1, scores=(), **kw):
    d = {"level": level, "flags": {}, "history": [], "last_change_at": 0, "cooldown_until": 0, "pending": None}
    d["history"] = [{"score": s, "gap": 0, "plan_fix": None, "rush": False} for s in scores]
    d.update(kw)
    return d


assert g.propose(ds(1, [0.9, 0.9])) is None                          # not enough evidence
assert g.propose(ds(1, [0.9, 0.9, 0.9]))["to"] == 2                  # fade
assert g.propose(ds(1, [0.3, 0.4, 0.5]))["to"] == 0                  # support
assert g.propose(ds(3, [0.9, 0.9, 0.9])) is None                     # already max
assert g.propose(ds(1, [0.9] * 4, last_change_at=2)) is None         # change gap
assert g.propose(ds(1, [0.9] * 4, cooldown_until=5)) is None         # reject cooldown
rushy = ds(1, [0.9, 0.9, 0.9])
rushy["history"].append({"score": 0.0, "rush": True})
assert g.propose(rushy)["to"] == 2                                   # rush episodes ignored
over = ds(1, [0.6, 0.6, 0.6])
for h in over["history"]:
    h["gap"] = 0.4
assert g.propose(over)["flag"] == "calibrate"

# --- end-to-end through the CLI in a temp project ---
with tempfile.TemporaryDirectory() as tmp:
    proj, gh = Path(tmp) / "shop", Path(tmp) / "home"
    proj.mkdir()
    (proj / ".git").mkdir()
    (proj / "package.json").write_text(json.dumps({"dependencies": {"next": "15", "react": "19", "prisma": "6"}}))
    env = {**os.environ, "GRASP_HOME": str(gh), "GRASP_TODAY": "2026-11-01"}

    def run(*args, stdin="", day=None):
        e = {**env, **({"GRASP_TODAY": day} if day else {})}
        r = subprocess.run([sys.executable, str(BIN), *args], cwd=proj, input=stdin, text=True, capture_output=True, env=e)
        return r

    assert run("init").returncode == 0
    assert json.loads((proj / ".grasp/project.json").read_text())["domains"] == ["nextjs", "prisma"]

    out = run("start", "cart checkout").stdout
    assert "Episode #001" in out
    run("next")  # -> plan (L1 requires plan)
    hook_in = json.dumps({"cwd": str(proj), "user_input": "implement the cart"})
    gate = run("gate", stdin=hook_in).stdout
    assert json.loads(gate)["decision"] == "block"                     # L1 = hard gate
    assert run("gate", stdin=json.dumps({"cwd": str(proj), "user_input": "PLAN: cart in cookie"})).stdout == ""
    assert run("gate", stdin=json.dumps({"cwd": str(proj), "user_input": "!quick rename var"})).stdout == ""
    run("next")  # -> build
    stop = json.dumps({"cwd": str(proj), "prompt_id": "p1", "last_assistant_message": "done"})
    assert json.loads(run("ingest", stdin=stop).stdout)["decision"] == "block"   # missing block -> nudge once
    assert run("ingest", stdin=stop).stdout == ""                                 # ...only once
    msg = 'ok\n```grasp\n{"concepts":["nextjs/server-actions"],"cards":[{"scope":"project","concept":"nextjs/cart","q":"Why is the cart in a cookie?","a_hint":"no auth needed"}],"plan_fix":"minor"}\n```'
    run("ingest", stdin=json.dumps({"cwd": str(proj), "last_assistant_message": msg}))
    assert len(json.loads((proj / ".grasp/cards.json").read_text())) == 1

    ctx = json.loads(run("context", stdin=json.dumps({"cwd": str(proj)})).stdout)
    assert "BUILD" in ctx["hookSpecificOutput"]["additionalContext"]

    def close(score, day):
        a = [{"q": f"q{score}{day}", "concept": "nextjs/x", "scope": "concept", "a_hint": "h", "self": 2, "ai": score}]
        return run("close", stdin=json.dumps({"answers": a, "handoff": "cart uses cookie"}), day=day)

    r = close(2, "2026-11-01")
    assert r.returncode == 0 and "closed" in r.stdout, r.stderr
    assert list((proj / ".grasp/episodes").glob("001-*.md"))
    for i, day in enumerate(["2026-11-02", "2026-11-03"]):
        run("start", f"f{i}", day=day)
        r = close(2, day)
    assert "ADAPTATION PROPOSAL" in r.stdout and "L2" in r.stdout, r.stdout
    assert "Accepted" in run("adapt", "accept").stdout
    assert json.loads((gh / "profile.json").read_text())["domains"]["nextjs"]["level"] == 2

    out = run("start", "orders", day="2026-11-20").stdout              # 17 days away -> re-entry + due cards
    assert "RE-ENTRY" in out and "WARM-UP" in out, out
    assert "Why is the cart in a cookie?" in out
    cards = json.loads((gh / "cards.json").read_text())
    cards += [{**cards[0], "id": "c9001", "domain": "security", "q": "sec q", "due": "2026-11-01"},
              {**cards[0], "id": "c9002", "domain": "pytorch", "q": "torch q", "due": "2026-11-01"}]
    (gh / "cards.json").write_text(json.dumps(cards))
    due = run("due", "50").stdout
    assert "sec q" in due and "torch q" not in due                     # cross-cutting yes, other stack no
    assert run("start", "again").returncode != 0                       # one active episode at a time
    assert run("grade", "p0001", "2").returncode == 0
    assert "Domains" in run("status").stdout

print("ok")
