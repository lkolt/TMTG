import markov
import sys

# precompile = '[ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B]START[1,1][1,1][1,1][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B][ ,B]' # for 7 in type zero
# precompile = '[&,&][B,B][B,B][B,B][B,B][B,B][B,B][B,B][B,B][B,B][START,1,1][1,1][1,1][B,B][B,B][B,B][B,B][B,B][B,B][B,B][B,B][B,B][B,B][@,@]' # for 7 in type one


def clear(s):
    return s.strip().strip("'")


if len(sys.argv) != 6:
    print('Incorrect number of arguments')
    sys.exit(1)

t = sys.argv[1]
num = sys.argv[2]
g_in = sys.argv[3]
r_out = sys.argv[4]
s_out = sys.argv[5]
precompile = ''

if t == '-t0':
    precompile = '[ ,B]' * (2 * len(num))
    precompile += 'START'
    for c in num:
        precompile += '[' + c + ',' + c + ']'
    precompile += '[ ,B]' * (2 * len(num))
elif t == '-t1':
    precompile = '[&,&]'
    precompile += '[B,B]' * (2 * len(num))
    precompile += '[START,1,1]'
    for i in range(len(num) - 1):
        c = num[i + 1]
        precompile += '[' + c + ',' + c + ']'
    precompile += '[B,B]' * (2 * len(num))
    precompile += '[@,@]'
else:
    print('Incorrect type of grammar')
    sys.exit(1)

if not markov.check_out(num, t):
    print('Incorrect number')
    sys.exit(1)
print('-Generate initial sequence:')
print(precompile)
print('-Starting Markov machine...')

grammar_input = open(g_in)
grammar = []

for line in grammar_input:
    l, r = line.split(" -> ")
    grammar.append((clear(l), clear(r), False))

flag, rules, result = markov.run(grammar, precompile, t)
print('-Done:')
if flag:
    print(num + ' is a prime number')
else:
    print(num + ' is not a prime number')

rul = open(r_out, 'w')
rul.writelines(rules)
rul.close()

sol = open(s_out, 'w')
sol.writelines(result)
sol.close()
