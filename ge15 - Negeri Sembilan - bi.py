import itertools
import math
import statistics 
import matplotlib.pyplot as plt

voters = [  'Jelebu',
            'Jempoi',
            'Seremban',
            'Kuala Pilah',
            'Rasah',
            'Rembau',
            'Port Dickson',
            'Tampin']

size = [    59561,
            95813,
            157244,
            63247,
            155896,
            133555,
            104450,
            81099]

def get_combinations(List):
    combination = []

    for k in range(1, len(List) + 1):
        # to generate combination
        combination.extend(itertools.combinations(List, k))
    return combination


def calculate(voting_weights):
    if voting_weights == [1 for x in voting_weights]:
        index = [x / len(voting_weights) for x in voting_weights]
    else:
        quota = sum(voting_weights) / 2

        num_critical = []

        for j in range(len(voting_weights)):
            critical = 0

            # a temporary list
            temp = voting_weights
            # remove the one that we are calculating for
            leftover = temp.pop(j)

            # all the possible coalitions without the one that we popped out
            combinations_no_j = get_combinations(temp)

            # place back
            temp.insert(j, leftover)

            for k in range(len(combinations_no_j)):
                # the conditions to check if s/he is critical in a winning coalition
                if sum(combinations_no_j[k]) < quota and sum(combinations_no_j[k]) + leftover > quota:
                    critical += 1
            num_critical.append(critical)
        # print(num_critical)

        # return num_critical

        total = sum(num_critical)
        index = [x / total for x in num_critical]
    return index


def prob_i(n):
    if (n % 2) == 1:
        binom = math.sqrt(2 / math.pi) * math.sqrt(n ** (2 * n + 1) / (((n - 1) ** n) * ((n + 1) ** (n + 2))))

    else:
        binom = math.sqrt(2 / (math.pi * n))

    return binom


def main():
    lowvar = 1121
    lowalpha = 0
    # lowbanzhaf = []
    lowbanzhafI = []
    lower = 0
    upper = 0

    var = []

    for i in range(0, 201):
        power = i / 100
        weights = [x ** power for x in size]

        # all district's banzhaf index
        banzhafA = calculate(weights)

        denominator = 0
        for k in range(len(voters)):
            denominator += prob_i(size[k]) * banzhafA[k] * size[k]

        banzhafI = []
        for j in range(len(voters)):
            numerator = prob_i(size[j]) * banzhafA[j]
            individual = numerator / denominator
            banzhafI.append(individual)

        variance = statistics.variance(banzhafI)
        var.append(variance)

        if variance < lowvar:
            lowvar = variance
            lowalpha = power
            lower = power
            # lowbanzhaf = [x/sum(banzhafA) for x in banzhafA]
            '''
            normalize = 0
            for i in range(len(voters)):
                normalize += size[i]*banzhafI[i]
            lowbanzhafI = [x/normalize for x in banzhafI]
            '''
            # lowbanzhafI = [x/sum(banzhafI) for x in banzhafI]
            lowbanzhafI = banzhafI
        elif variance == lowvar:
            upper = power

    print()
    print(f"The lowest variance: {lowvar}")
    print(f"The interval of optimal alpha: {lower}, {upper}")
    '''
    print(f"Banzhaf Index, when alpha = {lowalpha}:")
    for i in range(len(voters)):
        name = voters[i]
        #value = round(lowbanzhaf[i],4)
        value2 = lowbanzhafI[i]
        print(f"Individual in {name}: {value2}")
    print()
    '''
    print(f"List of Variances: {var}")
    print(f"List of Banzhaf index of Districts: {banzhafA}")

    check = 0
    for i in range(len(banzhafI)):
        check += banzhafI[i] * size[i]
    print()
    print(f"Check: {check}")

    plt.plot([x / 100 for x in range(0, 201)], var)
    plt.xlabel("alpha")
    plt.ylabel("Variance")
    plt.show()

    return lowalpha


def exact(power):
    # print(f"When alpha = {power}:")

    weights = [x ** power for x in size]

    # all district's banzhaf index
    banzhafA = calculate(weights)

    denominator = 0
    for k in range(len(voters)):
        denominator += prob_i(size[k]) * banzhafA[k] * size[k]

    banzhafI = []
    for j in range(len(voters)):
        numerator = prob_i(size[j]) * banzhafA[j]
        individual = numerator / denominator
        banzhafI.append(individual)

    variance = statistics.variance(banzhafI)
    sd = variance ** 0.5

    return banzhafI + [variance] + [sd]


#main()

optimal = exact(0.44)
sqrt = exact(0.5)
one = exact(1)
zero = exact(0)
ratio = [x / sum(size) for x in size]


def latex_float(f):
    float_str = "{0:.4e}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"${0} \times 10^{{{1}}}$".format(base, int(exponent))
    else:
        return float_str


for i in range(len(voters)):
    name = voters[i]
    # numofvote = size[i]
    head = round(ratio[i], 4)
    veryfirst = latex_float(zero[i])
    first = latex_float(one[i])
    second = latex_float(sqrt[i])
    third = latex_float(optimal[i])
    varoptimal = latex_float(optimal[-2])
    varsqrt = latex_float(sqrt[-2])
    varone = latex_float(one[-2])
    varzero = latex_float(zero[-2])
    sdoptimal = latex_float(optimal[-1])
    sdsqrt = latex_float(sqrt[-1])
    sdone = latex_float(one[-1])
    sdzero = latex_float(zero[-1])
    print(f"{name} & {head} & {veryfirst} & {first} & {second} & {third} \\\\")
print("\hline")
print(f"\\textbf{{VARIANCE}} & & {varzero} & {varone} & {varsqrt} & {varoptimal} \\\\")
print("\hline")
print(f"\\textbf{{SD}} & & {sdzero} & {sdone} & {sdsqrt} & {sdoptimal} \\\\")
print("\hline")
