#!/usr/bin/python3
# Numeric Core Solver — Version 2.0.1
#
# Finalized rules:
# - For alphabetic words: chunks are exactly the per-letter values.
# - For numeric tokens: use 1–2 digit partitions.
# - Identity operations (*1, /1, -0) are ALLOWED.
# - Operators: one each of -, *, / in any order.
# - No zero intermediates.
# - No negative intermediates.
# - Minimal positive integer core; recurse on 4+ digit cores.
# - At the top and bottom of output, print the collected letter results in bright red.

from fractions import Fraction

# ---------- ANSI COLOR CODES ----------
COLOR = "\033[91m"      # bright red
RESET = "\033[0m"

# ---------- Permutations ----------

def permutations(seq):
    if len(seq) <= 1:
        return [seq[:]]
    perms = []
    for i in range(len(seq)):
        seq[i], seq[0] = seq[0], seq[i]
        for p in permutations(seq[1:]):
            perms.append([seq[0]] + p)
        seq[i], seq[0] = seq[0], seq[i]
    return perms

# ---------- Core computation ----------

def compute_cores(start, operands, pretrace=""):
    def sub(a, b): return a - b
    def mult(a, b): return a * b
    def div(a, b):
        if b != 0:
            return Fraction(a) / Fraction(b)
        return None

    ops = [(sub, "-"), (mult, "*"), (div, "÷")]
    op_orders = permutations(ops)
    result = []

    for ops_seq in op_orders:
        t = operands[0]
        trace = f"{pretrace} → {t}" if pretrace else f"{start}: {t}"
        ok = True

        for (op, name), operand in zip(ops_seq, operands[1:]):
            t0 = op(t, operand)
            if t0 is None or t0 == 0:
                ok = False
                break
            if t0 < 0:
                ok = False
                break
            t = t0
            trace += f", {name} {operand}"

        if ok and Fraction(t).denominator == 1 and t > 0:
            t = int(t)
            trace += f"; Core = {t}"
            result.append((t, trace))

    return result

# ---------- Numeric partitioning ----------

def partitions_1_or_2(ndigits):
    parts = []
    for a in (1, 2):
        for b in (1, 2):
            for c in (1, 2):
                for d in (1, 2):
                    if a + b + c + d == ndigits:
                        parts.append([a, b, c, d])
    return parts

def make_seq(digits, part):
    out = []
    i = 0
    for n in part:
        out.append(digits[i:i+n])
        i += n
    return out

# ---------- Core wrappers ----------

def min_core(cs):
    if cs:
        return min(cs, key=lambda x: x[0])
    return None

def cores_numeric(digits, pretrace=""):
    ndigits = len(digits)
    if ndigits < 4:
        return []

    all_candidates = []
    for p in partitions_1_or_2(ndigits):
        xs = make_seq(digits, p)
        s = [int(ds) for ds in xs]
        all_candidates.extend(compute_cores(digits, s, pretrace=pretrace))

    m = min_core(all_candidates)
    if m:
        core, trace = m
        s2 = str(core)
        if len(s2) >= 4:
            sub_run = cores_numeric(s2, pretrace=trace)
            if sub_run:
                return sub_run
        return [m]
    return []

def cores_word(operands, start_digits, pretrace=""):
    all_candidates = compute_cores(start_digits, operands, pretrace=pretrace)
    m = min_core(all_candidates)
    if m:
        core, trace = m
        s2 = str(core)
        if len(s2) >= 4:
            sub_run = cores_numeric(s2, pretrace=trace)
            if sub_run:
                return sub_run
        return [m]
    return []

# ---------- Word handling ----------

def word_to_operands(word):
    return [ord(c) - ord('A') + 1 for c in word.upper()]

def word_to_digits(word):
    return "".join(str(ord(c) - ord('A') + 1) for c in word.upper())

def core_to_letter(core):
    return chr(ord('A') + core - 1) if 1 <= core <= 26 else "?"

# ---------- Batch mode ----------

def process_token(token):
    if token.isalpha():
        ops = word_to_operands(token)
        digits = word_to_digits(token)
        run = cores_word(ops, digits)
    else:
        digits = "".join(ch for ch in token if ch.isdigit())
        run = cores_numeric(digits)

    if not run:
        return token, None, None, "No core found"

    core, trace = run[0]
    letter = core_to_letter(core)
    return token, core, letter, trace

def main():
    print("Numeric Core Solver (Version 2.0.1)")
    print("Enter multiple words or numbers separated by spaces.")
    line = input("Input: ").strip()
    tokens = line.split()
    print()

    letters = []
    results = []

    for tok in tokens:
        word, core, letter, info = process_token(tok)
        if letter is not None:
            letters.append(letter)
        results.append((word, core, letter, info))

    banner = "".join(letters)
    print(f"{COLOR}=== {banner} ==={RESET}\n")

    for word, core, letter, info in results:
        print(f"Input: {word}")
        if core is None:
            print(f"  Result: {info}\n")
        else:
            print(f"  Core: {core}")
            print(f"  Letter: {letter}")
            print(f"  Trace: {info}\n")

    print(f"{COLOR}=== {banner} ==={RESET}")

if __name__ == "__main__":
    main()
