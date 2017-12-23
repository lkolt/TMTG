import markov
import sys

grammar_input = open('grammarZero.txt')
grammar = []
#precompile = '[ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B]START[1,1][1,1][1,1][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B]' # for 7


def clear(s):
    return s.strip().strip("'")


num = sys.argv[1]
if not markov.chekcCor(num):
    print('Incorrect number')

else :
    precompile = '[ ,B]'*(2 * len(num))
    precompile += 'START'
    for c in num:
        precompile += '[' + c + ',' + c + ']'
    precompile += '[ ,B]'*(2 * len(num))
    print(precompile)

    for line in grammar_input:
        l, r = line.split(" -> ")
        grammar.append((clear(l), clear(r), False))

    flag, result = markov.run(grammar, precompile)
    if flag:
        print('OK')
        solution = open('solution.txt', 'w')
        solution.writelines(result)
        solution.close()
    else:
        print('Its not a prime number')
