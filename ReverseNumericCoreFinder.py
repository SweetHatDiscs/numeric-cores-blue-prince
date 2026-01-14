# Reverse Numeric Core Finder (English + proper nouns)
# Compatible with NumericCores.py

from NumericCores import process_token

def load_wordlist(filename="wordlist.txt"):
    words = []
    with open(filename, "r") as f:
        for line in f:
            w = line.strip().upper()
            if len(w) == 4 and w.isalpha():
                words.append(w)
    return words

def parse_target(user_input):
    user_input = user_input.strip().upper()

    # Case 1: user typed a number
    if user_input.isdigit():
        return int(user_input)

    # Case 2: user typed a single letter
    if len(user_input) == 1 and user_input.isalpha():
        return ord(user_input) - ord('A') + 1

    # Invalid input
    raise ValueError("Input must be a number (1–999) or a single letter (A–Z).")

def find_words_for_core(target, wordlist):
    matches = []
    for word in wordlist:
        token, core, letter, trace = process_token(word)
        if core == target:
            matches.append((word, trace))
    return matches

def main():
    print("Reverse Numeric Core Finder")
    raw = input("Enter target core (1–999) OR a letter (A–Z): ")

    try:
        target = parse_target(raw)
    except ValueError as e:
        print(e)
        return

    print(f"\nSearching for words with core = {target}\n")

    wordlist = load_wordlist("wordlist.txt")
    results = find_words_for_core(target, wordlist)

    if not results:
        print(f"No words found with core = {target}")
        return

    print(f"Words with numeric core {target}:")
    print("----------------------------------")
    for word, trace in results:
        print(f"{word}  →  {trace}")
    print("----------------------------------")
    print(f"Total matches: {len(results)}")

if __name__ == "__main__":
    main()
