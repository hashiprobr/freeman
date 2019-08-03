import pandas as pd

from math import inf
from timeit import default_timer


class Simulation:
    def append(self, lists, xs):
        for key, x in xs.items():
            if key in lists:
                lists[key].append(x)
            else:
                lists[key] = [x]

    def convert(self, data):
        return pd.DataFrame(data)

    def save(self, data, path):
        df = self.convert(data)
        df.to_csv(path)

    def before_all(self):
        pass

    def before_each(self):
        pass

    def before_iter(self):
        pass

    def iterate(self):
        return False

    def after_iter(self, iteration, elapsed):
        pass

    def after_each(self, repetition, iteration, elapsed):
        pass

    def after_all(self, repetition, elapsed):
        pass

    def summarize(self):
        return None

    def run(self, times=1, max_iter=inf):
        self.before_all()
        start_all = default_timer()

        repetition = 1
        while repetition <= times:
            self.before_each()
            start_each = default_timer()

            iteration = 1
            while True:
                self.before_iter()
                start_iter = default_timer()

                repeat = self.iterate()

                end_iter = default_timer()
                self.after_iter(iteration, end_iter - start_iter)

                if repeat and (max_iter is None or iteration < max_iter):
                    iteration += 1
                else:
                    break

            end_each = default_timer()
            self.after_each(repetition, iteration, end_each - start_each)

            repetition += 1

        end_all = default_timer()
        self.after_all(repetition, end_all - start_all)

        return self.summarize()
