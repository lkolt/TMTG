"""
    Turing machine to grammar type 1 converter
    Author: Kanteev Leonid, 2017, SPBU
"""

from collections import defaultdict

sigma_alphabet = '01B&@'
gamma_alphabet = sigma_alphabet + 'ab*$'
eps = ' '
delta = []
start_state = 'START'
final_states = {'STOP'}
states = set()


def run(out):
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

    res_grammar = defaultdict(list)

    # 1:    A1 → [q0, ¢, a, a, &]
    for terminal in sigma_alphabet:
        res_grammar["A1"] += ['[&,' + start_state + ',' + terminal + ',' + terminal + ',' + '@]']

    for q, A, p, B, d in filter(lambda x: x[0] in states, delta):
        for a in sigma_alphabet:
            if A == '&' and d == 'R':
                for X in gamma_alphabet:
                    # 2.1:  [q, ¢, X, a, &] → [¢, p, X, a, &],  if (p, ¢, R) ∈ δ(q, ¢) and q ∈ Q \ F
                    res_grammar['[' + q + ',&,' + X + ',' + a + ',@]'] += ['[&,' + p + ',' + X + ',' + a + ',' + '@]']
                    # 5.1:  [q, ¢, X, a] → [¢, p, X, a],        if (p, ¢, R) ∈ δ(q, ¢) and q ∈ Q \ F
                    res_grammar['[' + q + ',&,' + X + ',' + a + ']'] += ['[&,' + p + ',' + X + ',' + a + ']']
            else:
                if A == '@' and d == 'L':
                    for X in gamma_alphabet:
                        # 2.4:  [¢, X, a, q, &] → [¢, p, X, a, &],  if (p, &, L) ∈ δ(q, &) and q ∈ Q \ F
                        res_grammar['[&,' + X + ',' + a + ',' + q + ',@]'] += ['[&,' + p + ',' + X + ',' + a + ',@]']
                        # 7.2:  [X, a, q, &] → [p, X, a, &],        if (p, &, L) ∈ δ(q, &) and q ∈ Q \ F
                        res_grammar['[' + X + ',' + a + ',' + q + ',@]'] += ['[' + p + ',' + X + ',' + a + ',@]']
                else:
                    # X == A and Y == B
                    if d == 'L':
                        # 2.2:  [¢, q, X, a, &] → [p, ¢, Y, a, &],  if (p, Y, L) ∈ δ(q, X) and q ∈ Q \ F
                        res_grammar['[&,' + q + ',' + A + ',' + a + ',' + '@]'] += ['[' + p + ',&,' + B + ',' + a + ',@]']
                        # 5.2:  [¢, q, X, a] → [p, ¢, Y, a],        if (p, Y, L) ∈ δ(q, X) and q ∈ Q \ F
                        res_grammar['[&,' + q + ',' + A + ',' + a + ']'] += ['[' + p + ',&,' + B + ',' + a + ']']

                        for Z in gamma_alphabet:
                            for b in sigma_alphabet:
                                # 6.2:  [Z, b] [q, X, a] → [p, Z, b] [Y, a],        if (p, Y, L) ∈ δ(q, X) and q ∈ Q \ F
                                res_grammar['[' + Z + ',' + b + '][' + q + ',' + A + ',' + a + ']'] += ['[' + p + ',' + Z + ',' + b + '][' + B + ',' + a + ']']
                                # 6.4:  [¢, Z, b] [q, X, a] → [¢, p, Z, b] [Y, a],  if (p, Y, L) ∈ δ(q, X) and q ∈ Q \ F
                                res_grammar['[&,' + Z + ',' + b + '][' + q + ',' + A + ',' + a + ']'] += ['[&,' + p + ',' + Z + ',' + b + '][' + B + ',' + a + ']']
                                # 7.3:  [Z, b] [q, X, a, &] → [p, Z, b] [Y, a, &],  if (p, Y, L) ∈ δ(q, X) and q ∈ Q \ F
                                res_grammar['[' + Z + ',' + b + '][' + q + ',' + A + ',' + a + ',@]'] += ['[' + p + ',' + Z + ',' + b + '][' + B + ',' + a + ',@]']
                    else:
                        # 2.3:  [¢, q, X, a, &] → [¢, Y, a, p, &],  if (p, Y, R) ∈ δ(q, X) and q ∈ Q \ F
                        res_grammar['[&,' + q + ',' + A + ',' + a + ',@]'] += ['[&,' + B + ',' + a + ',' + p + ',@]']

                        for Z in gamma_alphabet:
                            for b in sigma_alphabet:
                                # 5.3:  [¢, q, X, a] [Z, b] → [¢, Y, a] [p, Z, b],  if (p, Y, R) ∈ δ(q, X) and q ∈ Q \ F
                                res_grammar['[&,' + q + ',' + A + ',' + a + '][' + Z + ',' + b + ']'] += ['[&,' + B + ',' + a + '][' + p + ',' + Z + ',' + b + ']']
                                # 6.1:  [q, X, a] [Z, b] → [Y, a] [p, Z, b],        if (p, Y, R) ∈ δ(q, X) and q ∈ Q \ F
                                res_grammar['[' + q + ',' + A + ',' + a + '][' + Z + ',' + b + ']'] += ['[' + B + ',' + a + '][' + p + ',' + Z + ',' + b + ']']
                                # 6.3:  [q, X, a] [Z, b, &] → [Y, a] [p, Z, b, &],  if (p, Y, R) ∈ δ(q, X) and q ∈ Q \ F
                                res_grammar['[' + q + ',' + A + ',' + a + '][' + Z + ',' + b + ',@]'] += ['[' + B + ',' + a + '][' + p + ',' + Z + ',' + b + ',@]']

                                # 7.1:  [q, X, a, &] → [Y, a, p, &],                if (p, Y, R) ∈ δ(q, X) and q ∈ Q \ F
                        res_grammar['[' + q + ',' + A + ',' + a + ',@]'] += ['[' + B + ',' + a + ',' + p + ',@]']


    res_grammar['[A1]'] += ['[B,B][A1]']
    res_grammar['[A1]'] += ['[&,&][A1]']
    res_grammar['[A2]'] += ['[A3]']
    res_grammar['[A3]'] += ['[B,B][A3]']
    res_grammar['[A3]'] += ['[B,B,@]']
    for a in sigma_alphabet:
        # 4.1:  A1 → [q0, ¢, a, a] A2
        res_grammar['[A1]'] += ['[&,' + start_state + ',' + a + ',' + a + '][A2]']
        # 4.2:  A2 → [a, a] A2
        res_grammar['[A2]'] += ['[' + a + ',' + a + '][A2]']
        # 4.3:  A1 → [q0, a, a] A2
        res_grammar['[A1]'] += ['[' + start_state + ',' + a + ',' + a + '][A2]']


    for q in final_states:
        for X in gamma_alphabet:
            for a in sigma_alphabet:
                # 3.1:  [q, ¢, X, a, &] → a, q ∈ F
                res_grammar['[' + q + ',&,' + X + ',' + a + ',@]'] += [a]
                # 3.2:  [¢, q, X, a, &] → a, q ∈ F
                res_grammar['[&,' + q + ',' + X + ',' + a + ',@]'] += [a]
                # 3.3:  [¢, X, a, q, &] → a, q ∈ F
                res_grammar['[&,' + X + ',' + a + ',' + q + ',@]'] += [a]
                # 8.1:  [q, ¢, X, a] → a,   if q ∈ F
                res_grammar['[' + q + ',&,' + X + ',' + a + ']'] += [a]
                # 8.2:  [¢, q, X, a] → a,   if q ∈ F
                res_grammar['[&,' + q + ',' + X + ',' + a + ']'] += [a]
                # 8.3:  [q, X, a] → a,      if q ∈ F
                res_grammar['[' + q + ',' + X + ',' + a + ']'] = [a]
                # 8.4:  [q, X, a, &] → a,   if q ∈ F
                res_grammar['[' + q + ',' + X + ',' + a + ',@]'] += [a]
                # 8.5:  [X, a, q, &] → a,   if q ∈ F
                res_grammar['[' + X + ',' + a + ',' + q + ',@]'] += [a]

                # 9
                for b in sigma_alphabet:
                    # 9.1:  a[X, b] → ab
                    res_grammar[a + '[' + X + ',' + b + ']'] += [a + ' ' + b]
                    # 9.2:  a[X, b, &] → ab
                    res_grammar[a + '[' + X + ',' + b + ',@]'] += [a + ' ' + b]
                    # 9.3:  [X, a]b → ab
                    res_grammar['[' + X + ',' + a + ']' + b] += [a + ' ' + b]
                    # 9.4:  [¢, X, a]b → ab
                    res_grammar['[&,' + X + ',' + a + ']' + b] += [a + ' ' + b]

    with open(out, 'w') as f:
        for k, v in res_grammar.items():
            for right in v:
                f.write(k + ' -> ' + right + '\n')
