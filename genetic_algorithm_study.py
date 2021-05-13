# -*- coding: utf-8 -*-

import random


class Gene:
    def __init__(self, gene_size: int = 0, data: list = None):
        if data is not None:
            self.data = data
        else:
            self.data = random.sample(range(0, 10), gene_size)
        self.fitness = 0

    def __str__(self):
        return f'{str(self.data)}, Fitness : {str(self.fitness)}'


class Chromosome:
    answer = []

    def __init__(self, gene_size: int = 0, population_size: int = 0, genes: list = None):
        if genes is not None:
            self.genes = genes
        else:
            self.genes = [Gene(gene_size) for _ in range(population_size)]
        for i in self.genes:
            i.fitness = Chromosome.get_fitness(i.data, Chromosome.answer)

    def __str__(self):
        result = ''
        for i, g in enumerate(self.genes):
            result += f'Gene #{i + 1} : '
            result += str(g)
            result += '\n'

        return result

    def sort(self):
        self.genes.sort(key=lambda k: k.fitness, reverse=True)

    @staticmethod
    def get_fitness(data: list, answer: list) -> int:
        strike_score = len([True for i, g in enumerate(data) if g is answer[i]]) * 150
        ball_score = len([True for i, d in enumerate(data) if d != answer[i] and d in answer]) * 100

        return strike_score + ball_score

    @staticmethod
    def extract_parent_using_fitness(data: list) -> Gene:
        fitness_sum = sum(i.fitness for i in data)
        pick = random.uniform(0, fitness_sum)
        current = 0

        for i in data:
            current += i.fitness
            if current > pick:
                return i

    @staticmethod
    def crossover(genes: list) -> (Gene, Gene):
        father = Chromosome.extract_parent_using_fitness(genes)
        mother = Chromosome.extract_parent_using_fitness(genes)
        index = random.randint(1, len(father.data) - 2)
        child1 = Gene(data=father.data[:index] + mother.data[index:])
        child2 = Gene(data=mother.data[:index] + father.data[index:])

        return child1, child2

    @staticmethod
    def mutate(g: Gene, mutation_rate: float):
        for i in range(len(g.data)):
            if random.random() < mutation_rate:
                g.data[i] = random.choice(range(0, 10))
                g.fitness = Chromosome.get_fitness(g.data, Chromosome.answer)


def main():
    answer = random.sample(range(0, 10), 4)  # get random answer
    # answer = [5, 4, 2, 6]
    gene_size = 4
    population_size = 10
    mutate_rate = 0.2
    Chromosome.answer = answer
    chromosome = Chromosome(gene_size, population_size)
    chromosome.sort()
    count = 1

    print(f'{count} Generation')
    print(chromosome)

    while len([i.fitness for i in chromosome.genes if i.fitness >= 600]) < 1:
        new_genes = []
        for _ in range(population_size // 2):
            gene_1, gene_2 = Chromosome.crossover(chromosome.genes)
            new_genes.append(gene_1)
            new_genes.append(gene_2)

        chromosome = Chromosome(genes=new_genes)

        for g in chromosome.genes:
            Chromosome.mutate(g, mutate_rate)

        chromosome.sort()
        count += 1

        print(f'{count} Generation')
        print(chromosome)
    print(f'Answer : {"".join(map(str, answer))}')


if __name__ == '__main__':
    main()
