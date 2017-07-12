import math

dmg = 40
max_range = 80

def damage2(range):
    print('real.range: ' + str(range))
    range = range - (50 + 50) / 2 / 2 / 4
    range = max(range, 1)
    print('range: ' + str(range))

    dmg = 40 - math.pow((( -2 * max_range / math.pow(max_range, 2) ) * math.pi * range), 2)

    #print('damage: ' + str(dmg / max(range, 1)))
    print('damage: ' + str(dmg))


def damage(range):
    maxRange = 20
    dmg = 40

    diff = maxRange - sigmoid(range, maxRange)
    c = diff / maxRange

    print "range", range
    print "diff", diff
    print "c", c
    print "dmg", (dmg * c)
    print ""




def logarifm(x):
    try:
        v = math.log(-1 * x + 20, 1.22) + 5
    except ValueError:
        v = 0
    return v / 20


def sigmoid(x, maxRange):
    v = maxRange * 2 / (1 + math.pow(math.e, (x * -1 / 9))) - maxRange
    v = max(1, v)
    v = min(maxRange, v + 0.01)
    print "sigmoid", x, v
    return v



for i in range(30):
    print i, 40 * logarifm(i)