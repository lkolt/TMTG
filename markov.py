def contains(s, sub):
    return s.find(sub) != -1


def check_out(s, t):
    res = True
    for c in s:
        if not (c in ['0', '1', ' '] or (t == '-t1' and c in ['&', 'B', '@'])):
            res = False
    return res


def find_rule(a, w):
    try:
        return list(filter(lambda lrb: contains(w, lrb[0]), a))[0]
    except IndexError:
        raise ValueError("not found")


def apply_rule(lrb, s):
    l, r, b = lrb
    return s.replace(l, r, 1)


def apply_alg(a, w, log):
    l, r, b = r = find_rule(a, w)
    log.append('{} -> {}\n'.format(r[0], r[1]))
    return apply_rule(r, w), b


def run(a, w, t):
    result = []
    log = []
    flag = False                            # whether Halting rule was applied
    try:
        while not flag:                     # Normal rule was applied
            result.append(w + '\n')
            w, flag = apply_alg(a, w, log)  # apply a rule
        result.append(w)
    except ValueError:                      # No rule was applied
        pass

    res = check_out(w, t)
    return res, log, result
