from math import inf
from timeit import default_timer


class Simulation:
    def print(self, datum):
        print(', '.join('{}: {}'.format(key, value) for key, value in datum.items()))

    def append(self, data, datum):
        for key, value in datum.items():
            if key not in data:
                data[key] = []
            data[key].append(value)

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

                if repeat and (max_iter is None or iteration < max_iter):
                    iteration += 1
                else:
                    break

            end_each = default_timer()
            self.after_each(repetition, iteration, end_each - start_each)

            if repetition < times:
                repetition += 1
            else:
                break

        end_all = default_timer()
        self.after_all(repetition, end_all - start_all)

        return self.summarize()
