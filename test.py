import math

dmg = 40
max_range = 80

def damage(range):
    print('real.range: ' + str(range))
    range = range - (50 + 50) / 2 / 2 / 4
    range = max(range, 1)
    print('range: ' + str(range))

    dmg = 40 - math.pow((( -2 * max_range / math.pow(max_range, 2) ) * math.pi * range), 2)

    #print('damage: ' + str(dmg / max(range, 1)))
    print('damage: ' + str(dmg))


for i in range(80):
    print(damage(i))