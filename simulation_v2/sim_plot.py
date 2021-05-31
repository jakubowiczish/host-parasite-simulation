import matplotlib.pyplot as plt
import _thread
from sim_data import sim_data
import multiprocessing


def plot_on_thread():
    pool = multiprocessing.Pool()
    host_dead = [sim_data.timestamps, sim_data.hosts_dead, "Czas [s]", "Liczba martwych żywicieli",
                 "Śmierć żywicieli w czasie",
                 "time_hosts_dead.png", ["Martwi żywiciele"]]
    food = [sim_data.timestamps, sim_data.foods, "Czas [s]", "Ilość pożywienia", "Zmiana ilości pożywienia w czasie",
            "time_food.png", ["Pożywienie"]]
    carriers = [sim_data.timestamps, sim_data.carriers, "Czas [s]", "Liczba nosicieli",
                "Zmiana liczby nosicieli w czasie", "time_carriers.png", ["Żywiciele"]]
    SimPlot.plot_sub_plot(sim_data.timestamps, (sim_data.hosts_alive, sim_data.parasites), "Czas [s]",
                          "Liczba żywicieli",
                          "Populacja żywicieli w czasie",
                          "time_hosts_alive.png", ["Żywiciele", "Pasożyty"])
    pool.starmap(SimPlot.plot, [host_dead, food, carriers])


def plot_gen(xs, ys, xlabel, ylabel, title):
    plt.figure(figsize=(12, 10))
    plt.grid(linestyle='-', linewidth=1)
    plt.plot(xs, ys, linestyle='--', marker='o')
    plt.ylim(0)
    plt.ylabel(ylabel, size=14)
    plt.xlabel(xlabel, size=14)
    plt.title(title, size=16)


class SimPlot:

    def plot_all(self):
        _thread.start_new_thread(plot_on_thread, ())

    @staticmethod
    def plot(xs, ys, xlabel, ylabel, title, file_name, legend):
        plot_gen(xs, ys, xlabel, ylabel, title)
        plt.legend(legend)
        plt.savefig(f'plt/{file_name}')
        plt.show()

    @staticmethod
    def plot_sub_plot(xs, ys, xlabel, ylabel, title, file_name, legend):
        host, parasite = ys
        plot_gen(xs, host, xlabel, ylabel, title)
        plt.plot(xs, parasite, linestyle='--', marker='o')
        plt.legend(legend)
        plt.savefig(f'plt/{file_name}')
        plt.show()
