import numpy as np
from numpy.random import default_rng
rng = default_rng()

DEDUCTION = 0.75
RACERS = 14
BETTORS = 1000
TRIAL = 100000

# races = rng.integers(1, RACERS+1, size=(TRIAL, BETTORS))
# bet = 100
# payout = 0
# for race in races:
#     votes = np.sum(race==1)
#     p = votes/BETTORS
#     p = p * 1.5
#     odds = BETTORS * DEDUCTION/votes
#     win = rng.choice([1, 0], p=[p, 1-p])
#     if win:
#         payout += odds * bet

# invest = TRIAL * bet
# rate = payout/invest
# print(rate)

votes = 20
p = votes/BETTORS
odds = BETTORS * DEDUCTION/votes
print(p, odds)

v = BETTORS * DEDUCTION/37.5
print(v)
q = 1.5 * DEDUCTION/37.5
print(q)

# 期待する確率は、1.5 * 0.75/odds