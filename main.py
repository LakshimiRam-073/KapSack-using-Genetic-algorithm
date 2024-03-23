import random
import Items
import matplotlib.pyplot as plt

filename = "items"
population_size = 10
generations = 100
mutations = 0.1
carrier_limit = 28.0
list_items = []

## spliting the input from the items file
with open(filename, "r") as f:
    for line in f:
        newline = line.strip()
        newline = newline.split(" ")

        id, weight, value = newline[0], newline[1], newline[2]
        newitem = Items.Item(int(id), float(weight), float(value))
        list_items.append(newitem)

items_len = len(list_items)


##create random value
def create_random_solution(items_len):
    rand_solution = []
    for i in range(0, items_len):
        rand_solution.append(random.randint(0, 1))
    return rand_solution


def valid_solution(new_solution, weight_limit, list_items):
    total_weight = 0
    for i in range(0, len(new_solution)):
        if new_solution[i] == 1:
            total_weight += list_items[i].weight
        if total_weight > weight_limit:
            return False
    return True


def check_if_both_are_same(new_solution, existing_solution):
    for i in range(0, len(new_solution)):
        if (existing_solution[i] != new_solution[i]):
            return False
    return True


## creating random population
def create_initial_population(population_s, item_list, weight_limit):
    population = []
    i = 0
    while i < population_s:
        new_solution = create_random_solution(items_len)
        if valid_solution(new_solution, weight_limit, item_list):
            if len(population) == 0:
                population.append(new_solution)
                i += 1
            else:
                skip = False
                for j in range(0,len(population)):
                    if check_if_both_are_same(new_solution, population[j]):
                        skip = True
                        continue
                if not skip:
                    population.append(new_solution)
                    i += 1
    return population


def calc_value(list_items, player):
    total = 0
    for i in range(0, len(player)):
        if player[i] ==1:
            total += list_items[i].value
    return total


def tournament_selection(population):
    selected1 = random.randint(0, len(population) - 1)
    selected2 = random.randint(0, len(population) - 1)
    if calc_value(list_items, population[selected1]) > calc_value(list_items, population[selected2]):
        winner = population[selected1]
    else:
        winner = population[selected2]
    return  winner


def crossover(parent1, parent2, weight_limit, list_items):
    breakpoint = random.randint(0, len(parent2))
    first_part = parent1[:breakpoint]
    second_part = parent2[breakpoint:]
    child = first_part + second_part
    if valid_solution(child, weight_limit, list_items):
        return child
    return crossover(parent1, parent2, weight_limit, list_items)


def mutation(chromosome):
    temp = chromosome
    mutation_index_1, mutation_index_2 = random.sample(range(0, len(chromosome)), 2)
    temp[mutation_index_1], temp[mutation_index_2] = temp[mutation_index_2], temp[mutation_index_1]

    if valid_solution(temp, carrier_limit, list_items):
        return temp
    else:
        return mutation(chromosome)  # Return the mutated chromosome


def best_of_population(generation,list_items):
    best_value =0

    for i in range(0,len(generation)):
        value = calc_value(list_items,generation[i])
        if value > best_value:
            best_value = value
    return best_value

def create_generation(previous_population,weight_limit,mutations_ratio):
    newgen=[]
    for i in range(0,len(previous_population)):
        parent1 = tournament_selection(previous_population)
        parent2 = tournament_selection(previous_population)
        child = crossover(parent1,parent2,weight_limit,list_items)
        if random.random() < mutations_ratio:
            mutation(child)
        newgen.append(child)
    return newgen

value_list = []

def create_genetic_algo(generation_size,weight_limit,population_size,mutatio_rate,list_items):
    population = create_initial_population(population_size,list_items,weight_limit)
    for i in range(0,generation_size):
        population = create_generation(population,weight_limit,mutatio_rate)
        print(population[0])

        print("value for gen ",i+1," is ",calc_value(list_items,population[0]))
        value_list.append(best_of_population(population,list_items))
    return population,value_list


best_species,values =create_genetic_algo(generations,carrier_limit,population_size,mutations,list_items)
plt.plot(values)
plt.xlabel('generations')
plt.ylabel('values')
plt.title("Values of the solutions during the generations")
plt.show()
