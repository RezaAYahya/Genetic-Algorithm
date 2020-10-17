import random
import copy
import math
import matplotlib.pyplot as plt

# Representasi individu dalam biner
def createKromosom(krom_size):
    krom = []  
    for i in range(krom_size):
        krom.append(random.randint(0,1))      
    
    return krom

def createPopulasi(pop_size):
    pop = []
    for i in range(pop_size):
        pop.append(createKromosom(10))
        
    return pop

# Dekode Kromosom
def encoding_biner(arr, rmin, rmax, N):
    return (rmin + (((rmax - rmin)/ sum([2**(-(i+1)) for i in range(N)])) * sum([(arr[i]*(2**(-(i+1)))) for i in range(N)])))

# Perhitungan Fitness
def countFitness(krom):
    x1 = encoding_biner(krom[:5],-1,2,5)
    x2 = encoding_biner(krom[5:],-1,1,5)
    fit_val = (math.cos(x1)*math.sin(x2)) - (x1 / (x2**2 + 1))

    # f = 1 / (h+a)
    # a = 0.01
    # berarti nilai maksimumnya = 100
    return (1/(fit_val + 0.01))

def countAllFitness(pop, pop_size):
    fit_all = []    
    for i in range(pop_size):
        fit_all.append(countFitness(pop[i]))
    
    return fit_all

# Pemilihan Orangtua
def tournamentSelection(pop, tournament_size, pop_size):
    best_krom = []
    for i in range(1, tournament_size):
        krom = pop[random.randint(0,pop_size-1)]
        if (best_krom == [] or countFitness(krom) > countFitness(best_krom)):
            best_krom = krom

    return best_krom

# 1-point Crossover
def crossover(parent1, parent2, Pc):
    r = random.random()
    if (r <= Pc):
        point = random.randint(0,9)
        for i in range(point, 10):
            parent1[i], parent2[i] = parent2[i], parent1[i]
        
    return parent1, parent2

# Mutasi pada Representasi Biner
def mutasi(child, Pm):
    for i in range(0,10):
        r = random.random()
        if (r <= Pm):
            if (child[i] == 1):
                child[i] = 0
            else:
                child[i] = 1  

    return child

# Mengambil Kromosom Terbaik
def getElitisme(fit_all):    
    return fit_all.index(max(fit_all))


pop_size = 25
pop = createPopulasi(pop_size)
lFit = []

for i in range(50):
    fit = countAllFitness(pop, pop_size)
    newpop = []
    best = getElitisme(fit)
    lFit.append(countFitness(pop[best]))
    newpop.append(pop[best])
    t = 0
    while (t < pop_size-1):
        par1 = tournamentSelection(pop, pop_size//5, pop_size)
        par2 = tournamentSelection(pop, pop_size//5, pop_size)
        print(par2)
        while (par1 == par2):
            par2 = tournamentSelection(pop, pop_size//5, pop_size)
        print(par2)
        pr1 = copy.deepcopy(par1)
        pr2 = copy.deepcopy(par2)
        child = crossover(pr1, pr2, 0.8)
        for i in range(2):
            offspring = mutasi(child[i], 0.2)
            newpop.append(offspring)
        t += 2
    pop = newpop

result = pop[best]

print('\n========RESULT========')
print('Kromosom Terbaik : ', result)
print('X1 : ', result[:5], 'X2 : ', result[5:])
print('Nilai X1 : ', encoding_biner(result[:5],-1,2,5), 'Nilai X2 : ', encoding_biner(result[5:],-1,1,5))
print('Nilai Fitness :', countFitness(pop[best]))

plt.plot(lFit)
plt.xlabel('Generasi')
plt.ylabel('Fitness')
plt.show()