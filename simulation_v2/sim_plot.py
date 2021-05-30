import matplotlib.pyplot as plt
from sim_data import sim_data


class SimPlot:

    @staticmethod
    def plot_all():
        SimPlot.plot(sim_data.timestamps, sim_data.hosts_alive, "time", "hosts_alive", "time_hosts_alive",
                     "time_hosts_alive.png")
        SimPlot.plot(sim_data.timestamps, sim_data.hosts_dead, "time", "hosts_dead", "time_hosts_dead",
                     "time_hosts_dead.png")
        SimPlot.plot(sim_data.timestamps, sim_data.foods, "time", "food", "time_food", "time_food.png")
        SimPlot.plot(sim_data.timestamps, sim_data.carriers, "time", "carriers", "time_carriers", "time_carriers.png")

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
        plt.xticks([])
        ax.set_xticks(xs[::step])
        plt.savefig(f'plt/{file_name}')
        plt.show()
