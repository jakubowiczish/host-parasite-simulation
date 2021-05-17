import matplotlib.pyplot as plt


class SimPlot:

    @staticmethod
    def plot(xs, ys, xlabel, ylabel, title, file_name, step=1):
        plt.figure(figsize=(12, 10))
        plt.grid(linestyle='-', linewidth=1)
        plt.plot(xs, ys, linestyle='--')
        plt.scatter(xs, ys)
        plt.ylim(0)
        plt.ylabel(ylabel, size=14)
        plt.xlabel(xlabel, size=14)
        plt.title(title, size=16)
        ax = plt.gca()
        plt.xticks(xs, rotation=60)
        ax.set_xticks(xs[::step])
        plt.savefig(f'plt/{file_name}')
        plt.show()
