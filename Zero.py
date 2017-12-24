"""
    Turing machine to grammar type 0 converter
    Author: Kanteev Leonid, 2017, SPBU
"""

from collections import defaultdict

sigma_alphabet = '01'
gamma_alphabet = sigma_alphabet + 'ab*B$'
eps = ' '
start_state = 'START'
final_states = {'STOP'}
states = {'STOP'}
delta = []

# Reading TM
TM = open('TM.txt', 'r')

for line in TM:
    if len(line) > 1 and line[0] != '/':
        lst = line.split('->')
        charLeft = lst[0][:1]
        stateLeft = lst[0][1:]
        charRight = lst[1][:1]
        stateRight = lst[1][1:-2]
        direction = lst[1][-2:-1]
        states.add(stateLeft)
        delta.append([stateLeft, charLeft, stateRight, charRight, direction])

# Adding grammar rules
res_grammar = defaultdict(list)
res_grammar['A1'] += ['[' + eps + ',' + 'B]' + 'A1'] + [start_state + ' A2']
res_grammar['A2'] += ['[' + a + ',' + a + ']' + 'A2' for a in sigma_alphabet] + ['A3']
res_grammar['A3'] += ['[' + eps + ',' + 'B]' + 'A3'] + [eps]

for (q, C, p, D, d) in delta:
    if d == 'R':
        for a in sigma_alphabet + eps:
            res_grammar[q + '[' + a + ',' + C + ']'] += ['[' + a + ',' + D + ']' + p]
    elif d == 'L':
        for a in sigma_alphabet + eps:
            for b in sigma_alphabet + eps:
                for E in gamma_alphabet:
                    res_grammar['[' + b + ',' + E + ']' + q + '[' + a + ',' + C + ']'] += [p + '[' + b + ',' + E + '][' + a + ',' + D + ']']

for final in final_states:
    for a in sigma_alphabet + eps:
        for C in gamma_alphabet:
            res_grammar['[' + a + ',' + C + ']' + final] += [final + a + final]
            res_grammar[final + '[' + a + ',' + C + ']'] += [final + a + final]
    res_grammar[final] += [eps]

# Output grammar
with open('GrammarZero.txt', 'w') as f:
    for k, v in res_grammar.items():
        for right in v:
            f.write(k + ' -> ' + right + '\n')
