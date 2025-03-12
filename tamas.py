import numpy as np
import random

# 🎵 Valid chord transitions
valid_progression = {
    "I": ["I", "ii", "iii", "IV", "V", "vi", "vii"],
    "ii": ["V", "IV", "iii", "vii"],
    "iii": ["I", "ii", "IV", "vi", "vii"],
    "IV": ["I", "iii", "V", "vi", "vii"],
    "V": ["I", "IV", "vi", "vii"],
    "vi": ["I", "ii", "IV", "V", "vii"],
    "vii": ["I", "iii", "vi"]  # vii typically resolves to I or iii in major keys
}

# 🎶 Popular progressions (for fitness bonus)
POPULAR_PROGRESSIONS = [
    ["I", "V", "vi", "vii"],
    ["I", "V", "vi", "iii", "IV"],
    ["vi", "V", "IV", "vii"],
    ["I", "vi", "IV", "vii"],
    ["I", "IV", "vi", "vii"],
    ["vii", "I", "V", "vi"]  # New progression showcasing vii resolution
]

# 🎸 Individual (Chord Progression)
class Individual:
    def __init__(self, notes=None, mutation_rate=0.7):
        self.fitness = 0
        self.mutation_rate = mutation_rate
        self.notes = notes if notes else self.random_progression()

    def random_progression(self, length=16):
        return [random.choice(list(valid_progression.keys())) for _ in range(length)]

    def mutate(self):
        """Mutate the chord progression (switch chords or replace with new)"""
        if random.random() < self.mutation_rate:
            i = np.random.randint(len(self.notes))
            self.notes[i] = random.choice(list(valid_progression.keys()))

    def calculate_fitness(self):
        """Evaluate how well the chord progression follows music theory"""
        self.fitness = 0
        for i in range(len(self.notes) - 1):
            if self.notes[i + 1] in valid_progression[self.notes[i]]:
                self.fitness += 5  # Good transition
            else:
                self.fitness -= 2  # Bad transition

        # Bonus for popular chord progressions
        for progression in POPULAR_PROGRESSIONS:
            if progression[:len(self.notes)] == self.notes[:len(progression)]:
                self.fitness += 10

        return self.fitness

# 🎼 Population (Genetic Algorithm)
class Population:
    def __init__(self, size=20, length=8):
        self.size = size
        self.length = length
        self.population = [Individual() for _ in range(size)]
        self.best_individual = None

    def select_best(self):
        """Find the best individual based on fitness"""
        self.population.sort(key=lambda ind: ind.calculate_fitness(), reverse=True)
        self.best_individual = self.population[0]

    def crossover(self, parent1, parent2):
        """Combine two individuals to create a new one"""
        split = np.random.randint(1, self.length - 1)
        child_notes = parent1.notes[:split] + parent2.notes[split:]
        return Individual(child_notes)

    def next_generation(self):
        """Create a new generation through selection, crossover, and mutation"""
        self.select_best()
        new_population = [self.best_individual]  # Preserve the best
        while len(new_population) < self.size:
            parent1, parent2 = random.sample(self.population[:10], 2)
            child = self.crossover(parent1, parent2)
            child.mutate()
            new_population.append(child)
        self.population = new_population

    def evolve(self, generations=50):
        """Run the genetic algorithm for a given number of generations"""
        for gen in range(generations):
            self.next_generation()
            print(f"Gen {gen+1}: Best Fitness = {self.best_individual.fitness}")
            if self.best_individual.fitness > 100:  # Stop early if we reach good fitness
                break
        return self.best_individual.notes
