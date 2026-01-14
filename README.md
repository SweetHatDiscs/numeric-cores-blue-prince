# numeric-cores-blue-prince
Numeric Core solver and Reverse Numeric Core generator

This project implements a Numeric Core solver for the puzzle game Blue Prince.  
It also includes a Reverse Numeric Core Finder, which searches through the word list and generates a list of possible four-letter words for the given numeric core.
This was written by GPT 5.1, which generated the wordlist as well, using uncommon English words and proper nouns.  The wordlist may contain hallucinations and can be replaced with your own wordlist.

It includes:
-NumericCores.py - the main solver.  Provide either a number or a word or a list of numbers and words separated by a space and it will provide the numeric core as well as any associated letter.
-ReverseNumericCoreFinder.py - finds all words that produce a given numeric core
-wordlist.txt - very expansive list of 4 letter english words and proper nouns

## Requirements
Python 3.10+

##Usage
python NumericCores.py
or
python ReverseNumericCoreFinder.py
