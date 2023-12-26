import itertools
import math
import statistics 
import matplotlib.pyplot as plt
import time

# Record the start time
start_time = time.time()

voters = [  'Tumpat',
                'Pengkalan Chepa',
                'Kota Bharu',
                'Pasir Mas',
                'Rautau Panjang',
                'Kubang Kerlan',
                'Bachok',
                'Ketereh',
                'Tanah Merah',
                'Pasir Puteh',
                'Machang',
                'Jeli',
                'Kuala Krai',
                'Gua Musang']

size = [    149371,
                106982,
                115450,
                94544,
                93248,
                113640,
                123183,
                85281,
                98782,
                113070,
                88825,
                59798,
                92335,
                70254
]

def get_combinations(List): 
    combination = []

    for k in range(1, len(List) + 1):
    # to generate combination
        combination.extend(itertools.combinations(List, k))
    return combination   


def calculate(voting_weights):
    quota = sum(voting_weights)/2

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
            if sum(combinations_no_j[k]) < quota and sum(combinations_no_j[k])+leftover > quota:
                critical += 1
        num_critical.append(critical)
    #print(num_critical) 

    # return num_critical

    total = sum(num_critical)
    index = [x/total for x in num_critical]
    return index

def prob_i(n):
    if (n % 2) == 1:
        binom = math.sqrt(2/math.pi) * math.sqrt(n**(2*n+1)/(((n-1)**n)*((n+1)**(n+2))))
        
    else:
        binom = math.sqrt(2/(math.pi * n))

    return binom

def main():
    lowvar = 1121
    lowalpha = 0
    #lowbanzhaf = []
    lowbanzhafI = []

    var = []

    for i in range(1, 100):
        power = i/100
        weights = [x**power for x in size]

        #all district's banzhaf index
        banzhafA = calculate(weights)

        denominator = 0
        for k in range(len(voters)):
            denominator += prob_i(size[k])*banzhafA[k]*size[k]

        banzhafI = []
        for j in range(len(voters)):
            numerator = prob_i(size[j])*banzhafA[j]
            individual = numerator/denominator
            banzhafI.append(individual)

        variance = statistics.variance(banzhafI)
        var.append(variance)

        if variance < lowvar:
            lowvar = variance            
            lowalpha = power
            #lowbanzhaf = [x/sum(banzhafA) for x in banzhafA]
            '''
            normalize = 0
            for i in range(len(voters)):
                normalize += size[i]*banzhafI[i]
            lowbanzhafI = [x/normalize for x in banzhafI]
            '''
            #lowbanzhafI = [x/sum(banzhafI) for x in banzhafI]
            lowbanzhafI = banzhafI
    print()
    print(f"The lowest variance: {lowvar}")
    print(f"The optimal alpha: {lowalpha}")
    print(f"Banzhaf Index, when alpha = {lowalpha}:")
    for i in range(len(voters)):
        name = voters[i]
        #value = round(lowbanzhaf[i],4)
        value2 = lowbanzhafI[i]
        print(f"Individual in {name}: {value2}")
    print()
    print(f"List of Variances: {var}")
    
    check = 0
    for i in range(len(banzhafI)):
        check += banzhafI[i]*size[i]
    print()
    print(f"Check: {check}")


    plt.plot([x/100 for x in range(1,100)], var)
    plt.xlabel("alpha")
    plt.ylabel("Variance")   
    plt.show()

def exact(power):
    #print(f"When alpha = {power}:")

    weights = [x**power for x in size]

    #all district's banzhaf index
    banzhafA = calculate(weights)

    denominator = 0
    for k in range(len(voters)):
        denominator += prob_i(size[k])*banzhafA[k]*size[k]

    banzhafI = []
    for j in range(len(voters)):
        numerator = prob_i(size[j])*banzhafA[j]
        individual = numerator/denominator
        banzhafI.append(individual)

    variance = statistics.variance(banzhafI)
    
    return banzhafI+[variance]

main()
'''
optimal = exact(0.47)
sqrt = exact(0.5)
one = exact(1)
#ratio = [x/sum(size) for x in size]

def latex_float(f):
    float_str = "{0:.4e}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"${0} \times 10^{{{1}}}$".format(base, int(exponent))
    else:
        return float_str

for i in range(len(voters)):
    name = voters[i]
    #numofvote = size[i]
    #head = ratio[i]
    first = latex_float(one[i])
    second = latex_float(sqrt[i])
    third = latex_float(optimal[i])
    varoptimal = latex_float(optimal[-1])
    varsqrt = latex_float(sqrt[-1])
    varone = latex_float(one[-1])
    print(f"{name} & {first} & {second} & {third} \\\\")
print("\hline")
print(f"\\textbf{{VARIANCE}} & {varone} & {varsqrt} & {varoptimal} \\\\")
print("\hline")
'''

# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the runtime