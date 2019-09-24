import pandas as pd

from math import inf
from timeit import default_timer
from abc import ABC, abstractmethod


class Simulation(ABC):
    def print(self, data, condition=True):
        if condition:
            print(', '.join('{}: {}'.format(key, value) for key, value in data.items()))

    def print_every(self, data, counter, interval):
        self.print(data, counter % interval == 0)

    def append(self, data):
        for key, value in data.items():
            if key not in self.data:
                self.data[key] = []
            self.data[key].append(value)

    def before_each(self):
        pass

    def before_iter(self):
        pass

    @abstractmethod
    def iterate(self):
        return False

    def after_iter(self, iteration, elapsed):
        pass

    def after_each(self, repetition, iterations, elapsed):
        pass

    def run(self, times=1, max_iter=inf):
        self.data = {}

        repetition = 1
        while True:
            self.before_each()
            start_each = default_timer()

            iteration = 1
            while True:
                self.before_iter()
                start_iter = default_timer()

                repeat = self.iterate()

                end_iter = default_timer()
                self.after_iter(iteration, end_iter - start_iter)

                if repeat and iteration < max_iter:
                    iteration += 1
                else:
                    break

            end_each = default_timer()
            self.after_each(repetition, iteration, end_each - start_each)

            if repetition < times:
                repetition += 1
            else:
                break

        return pd.DataFrame(self.data)
