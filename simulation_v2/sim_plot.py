import matplotlib.pyplot as plt
import _thread
from sim_data import sim_data
import multiprocessing


def plot_on_thread():
    pool = multiprocessing.Pool()
    host_alive = [sim_data.timestamps, sim_data.hosts_alive, "time", "hosts_alive", "time_hosts_alive",
                  "time_hosts_alive.png"]
    host_dead = [sim_data.timestamps, sim_data.hosts_dead, "time", "hosts_dead", "time_hosts_dead",
                 "time_hosts_dead.png"]
    food = [sim_data.timestamps, sim_data.foods, "time", "food", "time_food", "time_food.png"]
    carriers = [sim_data.timestamps, sim_data.carriers, "time", "carriers", "time_carriers", "time_carriers.png"]
    pool.starmap(SimPlot.plot, [host_alive, host_dead, food, carriers])


class SimPlot:

    def plot_all(self):
        _thread.start_new_thread(plot_on_thread, ())

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
