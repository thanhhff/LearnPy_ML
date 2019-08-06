# Sale = c1*TV + c2*Radio + c3*Newspaper + c4 * 1.0
# Find: [c1 c2 c3 c4]

import pandas as pd
import random
import numpy as np
import math
import matplotlib.pyplot as plt

n = 4  # size of indivudal (chromosome) - 3 feature + 1 bias
m = 100  # size of population
n_generations = 200  # number of generations
losses = []  # để vẽ biểu đồ quá trình tối ưu

# Import dữ liệu
dataframe = pd.read_csv('advertising.csv')

features = dataframe.values[:, :3]
prices = dataframe.values[:, 3]

# Add bias
features = np.concatenate((features, np.ones((features.shape[0], 1))), axis=1)


def compute_loss(individual):
    estimated_prices = []
    for feature in features:
        estimated_price = sum(c * x for x, c in zip(feature, individual))
        estimated_prices.append(estimated_price)

    losses = [abs(y_est - y_gt) for y_est, y_gt in zip(estimated_prices, prices)]
    return sum(losses)


def compute_fitness(individual):
    loss = compute_loss(individual)
    # loss + 1 dưới mẫu tránh trường hợp mẫu = 0
    fitness = 1 / (loss + 1)
    return fitness


def generate_random_value(bound=100):
    return (random.random()) * bound


def creat_individual():
    return [generate_random_value() for _ in range(n)]


def crossover(individual1, individual2, crossover_rate=0.9):
    # Lai ghép giữa 2 cá thể
    individual1_new = individual1.copy()
    individual2_new = individual2.copy()

    for i in range(n):
        if random.random() < crossover_rate:
            # Trong trường hợp True sẽ hoán đổi 2 gen của 2 cá thể với nhau
            individual1_new[i] = individual2[i]
            individual2_new[i] = individual1[i]

    return individual1_new, individual2_new


def mutate(individual, mutation_rate=0.05):
    # Đột biến
    individual_m = individual.copy()

    for i in range(n):
        if random.random() < mutation_rate:
            # Trong trường hợp True sẽ đột biến gen đó
            # Đột biến bằng việc random
            individual_m[i] = generate_random_value()

    return individual_m


def selection(sorted_old_population):
    index1 = random.randint(0, m - 1)
    while True:
        index2 = random.randint(0, m - 1)
        # Lựa chọn 2 gen khác nhau trong cá thể
        if index2 != index1:
            break

    # Lựa chọn individual_s trong sorted_population
    individual_s = sorted_old_population[index1]
    if index2 > index1:
        individual_s = sorted_old_population[index2]
    return individual_s


def create_new_population(old_population, elitism=2, gen=1):
    # key=compute_fitness -> Sắp xếp tăng dần
    sorted_population = sorted(old_population, key=compute_fitness)

    if gen % 10 == 0:
        losses.append(compute_loss(sorted_population[m - 1]))
        print('Best loss:', compute_loss(sorted_population[m - 1]))

    new_population = []
    while len(new_population) < m - elitism:
        # Selection
        individual_s1 = selection(sorted_population)
        individual_s2 = selection(sorted_population)

        # Crossover
        individual_c1, individual_c2 = crossover(individual_s1, individual_s2)

        # Mutation
        individual_m1 = mutate(individual_c1)
        individual_m2 = mutate(individual_c2)

        new_population.append(individual_m1)
        new_population.append(individual_m2)

    for ind in sorted_population[m - elitism:]:
        new_population.append(ind.copy())

    return new_population


population = [creat_individual() for _ in range(m)]
for i in range(n_generations):
    population = create_new_population(population, 2, i)

# y = [i for i in range(n_generations)]

# Vẽ losses
fig1 = plt.figure('Kết quả Best loss')
plt.plot(losses[:n_generations])
plt.show()


# Vẽ mức độ chênh lệch
sorted_population = sorted(population, key=compute_fitness)
individual = sorted_population[m - 1]

estimated_prices = []
for feature in features:
    estimated_price = sum(c*x for x, c in zip(feature, individual))
    estimated_prices.append(estimated_price)

losses = [abs(y_est - y_gt) for y_est, y_gt in zip(estimated_prices, prices)]
# Tổng lỗi khi dùng kết quả dự đoán
print('Value loss: ',sum(losses))

fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(prices, c='green')
plt.plot(estimated_prices, c='blue')
plt.show()


