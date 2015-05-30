from random import choice
from random import randrange
from random import uniform
from random import random

TARGET = 5123
CHAR_LENGTH = 4
POPULATION_SIZE = 100
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001
GENE_LENGTH = CHAR_LENGTH*240
GENERATIONS = 400

REPRESENTATION_TABLE = dict([
    ('0000','0'),
    ('0001','1'),
    ('0010','2'),
    ('0011','3'),
    ('0100','4'),
    ('0101','5'),
    ('0110','6'),
    ('0111','7'),
    ('1000','8'),
    ('1001','9'),
    ('1010','+'),
    ('1011','-'),
    ('1100','*'),
    ('1101','/'),
    ('1110',''),
    ('1111','')])

class Chromosone:
    def __init__(self, g=None):
        self.gene = g if g else "".join(choice("01") for i in range(GENE_LENGTH))
        self.fitness = calculateFitness(self.gene)
        
def roulette(p):
    totalfitness = 0
    for i in p:
        totalfitness += i.fitness
    therandom = uniform(0,totalfitness)
    thechosen = None
    for i in p:
        therandom -= i.fitness
        if therandom < i.fitness:
            thechosen = i
            p.remove(thechosen)
            break
    return thechosen

def mate(c1,c2):
    if random() < CROSSOVER_RATE:
        crossoverpt = randrange(GENE_LENGTH)
        offspring1 = Chromosone(c1.gene[:crossoverpt] + c2.gene[crossoverpt:])
        offspring2 = Chromosone(c2.gene[:crossoverpt] + c1.gene[crossoverpt:])
    else:
        offspring1 = c1
        offspring2 = c2
    mutate(offspring1)
    mutate(offspring2)
    return [offspring1, offspring2]

def mutate(c):
    newgene = ""
    for i in c.gene:
        if random() < MUTATION_RATE:
            newgene += '0' if i == '1' else '1'
        else:
            newgene += i
    c.gene = newgene

def calculateFitness(g):
    s = convert(g)
    ans = evalStr(s)
    fitness = 1.0/(abs(TARGET-ans)) if TARGET-ans !=0 else 1.1
    return fitness

def convert(g):
    split = [g[i:i+CHAR_LENGTH] for i in range(0, len(g), CHAR_LENGTH)]
    decoded = filter(lambda x: bool(x), map(lambda x: REPRESENTATION_TABLE[x], split))
    finalstring = "".join(makeSensible(decoded))
    return finalstring

def makeSensible(d):
    sensible = []
    nexttype = 'n'
    for i in d:
        if str.isdigit(i) and nexttype == 'n':
            sensible.append(i)
            nexttype = 'o'
        elif not str.isdigit(i) and nexttype == 'o':
            sensible.append(i)
            nexttype = 'n'
    try:
        if not str.isdigit(sensible[-1]):
            sensible.pop(-1)
    except:
        pass
    return sensible

def evalStr(s):
    try:
        return eval(s)
    except Exception:
        return 0

pop = []
newpop = []
for i in range(POPULATION_SIZE):
    pop.append(Chromosone())

topfitness = 0
while topfitness != 1.1:
    newpop = []
    while len(newpop) < POPULATION_SIZE:
        x = roulette(pop)
        y = roulette(pop)
        offsprings = mate(x,y)
        newpop.extend(offsprings)
        pop.extend([x,y])
    pop = newpop
    
    topfitness = 0
    for i in pop:
        topfitness = i.fitness if topfitness < i.fitness else topfitness
    print "Current Best Fitness: %s" % topfitness

for i in pop:
    if i.fitness == 1.1:
        print "Result: %s" % convert(i.gene)

