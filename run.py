import argparse
import sys

from random import shuffle

LONGEST_STRING_LEN = 1

def main():
    global LONGEST_STRING_LEN
    args = process_parameters()

    with open(args.wordlist, 'r', encoding='utf-8') as f:
        lines = [str.lower(line.replace('\n', '')) for line in f.readlines()]

    shuffle(lines)
    LONGEST_STRING_LEN = len(max(lines, key=len))

    ranked = {}
    for line in lines:
        complexity = rank_complexity(line)
        #print(f"Calculated complexity: {complexity} {line}")
        if complexity >= args.mincomplexity and complexity <= args.maxcomplexity:
            ranked[line] = complexity
    
    if not args.n:
        args.n = len(lines)

    if not args.outputfile:
        out = sys.stdout
    else:
        out = open(args.outputfile, 'w', encoding='utf-8')

    i = 1   
    for word, complexity in ranked.items():
        if i <= args.n:
            print(f"{word} {complexity}", file=out)
        i += 1

    if out is not sys.stdout:
        out.close()

def rank_complexity(word):
    #
    # 3 dimensions 
    #   a) length, weight: 2
    #   b) occurence of accents, weight:  5
    #   c) letter distribution, weight: 3
    #   Complexity = a*0.2 + b*0.5 + c*0.3
    a = rank_length(word) * 0.2
    b = rank_accent_occurence(word) * 0.5
    c = rank_transitions(word) * 0.3
    return round(a+b+c)

def rank_length(word):
    return round((len(word) / LONGEST_STRING_LEN) * 10)

def rank_accent_occurence(word):
    high_value = 'ťďňó'
    low_value = 'ěščřžýáíéůú'

    base_weight = 2.5
    easy_accent = 0
    hard_accent = 0
    both_accents = 0
   
    for letter in word:
        if letter in high_value:
            hard_accent = 2.5
        elif letter in low_value:
            easy_accent = 2.5

    if hard_accent and easy_accent:
        both_accents = 2.5

    return base_weight + easy_accent + hard_accent + both_accents

def rank_transitions(word):
    trans = keyboard_side_transitions(word)
    if trans >= 10:
        return 10
    else:
        return trans


def keyboard_side_transitions(word):
    left = 'qwertasdfgyxcvěščřďť'   # remainder = 'zuiopúhjklůbnmóňžýáíé'
    transitions = 0
    was_left = word[0] in left
    for letter in word[1:]:
        is_left = letter in left
        if was_left != is_left:
            transitions += 1
        was_left = is_left
    
    return transitions
        
def process_parameters():
    """
     --wordlist/-w
     --outputfile/-o
     -n -
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist on input', required=True)
    parser.add_argument('-o', '--outputfile', help='Where to write the output')
    parser.add_argument('-m', '--mincomplexity', help='Minimum complexity limit', type=int, choices=range(0, 10), default=0)
    parser.add_argument('-M', '--maxcomplexity', help='Maximum complexity limit', type=int, choices=range(0, 10), default=10)
    parser.add_argument('-n', help='How many words should be produced on the output (random ordering).', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    main()