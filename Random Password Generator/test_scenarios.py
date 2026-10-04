"""Automated checks for the 10 required test scenarios (run: python test_scenarios.py)."""
import builtins, io, string, contextlib
import password_generator as pg

def run(inputs):
    it = iter(inputs)
    builtins.input = lambda prompt="": next(it)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pg.main()
    return buf.getvalue()

def pw_from(out):
    return [l.split(": ")[1] for l in out.splitlines() if l.startswith("Generated password")]

def has(p, s): return any(c in s for c in p)
U, L, D, S = string.ascii_uppercase, string.ascii_lowercase, string.digits, pg.SYMBOLS

o = run(["8", "1,2", "n"]); p = pw_from(o)[0]
print("T1 ", len(p) == 8 and has(p, U) and has(p, L), p)
o = run(["12", "1,2,3,4", "n"]); p = pw_from(o)[0]
print("T2 ", len(p) == 12 and all(has(p, s) for s in (U, L, D, S)), p)
o = run(["10", "1,4", "n"]); p = pw_from(o)[0]
print("T3 ", len(p) == 10 and set(p) <= set(U + S) and has(p, U) and has(p, S), p)
o = run(["5", "8", "1,2", "n"]); print("T4 ", "at least 8" in o and len(pw_from(o)) == 1)
o = run(["-4", "8", "1,2", "n"]); print("T5 ", "at least 8" in o and len(pw_from(o)) == 1)
o = run(["abc", "8.5", "", "8", "1,2", "n"]); print("T6 ", o.count("whole number") == 3 and len(pw_from(o)) == 1)
o = run(["8", "1", "1,1", "9", "1,2", "n"]); print("T7 ", o.count("at least 2 different") == 2 and "invalid" in o)
o = run(["8", "1,2", "maybe", "y", "9", "2,3", "y", "12", "1,2,3,4", "n"]); print("T8 ", len(pw_from(o)) == 3 and "'y' for yes" in o)
ok9 = ok10 = True
for n in range(8, 60):
    for combo in ["1,2", "1,3", "1,4", "2,3", "2,4", "3,4", "1,2,3", "1,2,4", "1,3,4", "2,3,4", "1,2,3,4"]:
        sets = [pg.CHARACTER_TYPES[c][1] for c in combo.split(",")]
        for _ in range(20):
            p = pg.generate_password(n, sets)
            ok9 &= all(has(p, s) for s in sets); ok10 &= len(p) == n
print("T9 ", ok9); print("T10", ok10)
