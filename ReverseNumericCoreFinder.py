# Reverse Numeric Core Finder (English + proper nouns)
# Compatible with your Version 2.0.1 solver in NumericCoresWORKING.py

from NumericCores import process_token

def load_wordlist(filename="wordlist.txt"):
    words = []
    with open(filename, "r") as f:
        for line in f:
            w = line.strip().upper()
            if len(w) == 4 and w.isalpha():
                words.append(w)
    return words

def find_words_for_core(target, wordlist):
    matches = []
    for word in wordlist:
        token, core, letter, trace = process_token(word)
        if core == target:
            matches.append((word, trace))
    return matches

def main():
    print("Reverse Numeric Core Finder")
    target = int(input("Enter target core (1–999): ").strip())
    print()

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
