# The authors of this work have released all rights to it and placed it
# in the public domain under the Creative Commons CC0 1.0 waiver
# (http://creativecommons.org/publicdomain/zero/1.0/).
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# Retrieved from: http://en.literateprograms.org/Markov_algorithm_simulator_(Python)?oldid=19173


def contains(s, sub):
    return s.find(sub) != -1


def chekcCor(s):
    res = True
    for c in s:
        if not c in ['0', '1', ' ']:
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
    log.append('\nFound {}, execute {} -> {}:\n'.format(l, r[0], r[1]))
    return apply_rule(r, w), b


def run(a, w):
    result = []
    log = []
    flag = False                      # whether Halting rule was applied
    lastW = w
    try:
        while not flag:               # Normal rule was applied
            result.append(w)
            w, flag = apply_alg(a, w, log) # apply a rule
            #print(w)
            lastW = w
        result.append(w)
    except ValueError:                # No rule was applied
        pass

    res = chekcCor(lastW)
    return res, map(lambda lr: lr[1] + lr[0], zip(log, result))
