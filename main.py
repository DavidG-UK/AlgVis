import random
NUMDICE = 1
MAX_ROLL = 8
MODIFIER = 2
total = 0

for i in range(NUMDICE):
    total += random.randint(1, MAX_ROLL)

print(total)