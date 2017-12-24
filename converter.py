import sys
import Zero
import One


if len(sys.argv) != 3:
    print('Incorrect number of arguments')
    sys.exit(1)

t = sys.argv[1]
g_out = sys.argv[2]

if t == '-t0':
    Zero.run(g_out)
elif t == '-t1':
    One.run(g_out)
else:
    print('Incorrect type of grammar')
    sys.exit(1)

print('Done!')
