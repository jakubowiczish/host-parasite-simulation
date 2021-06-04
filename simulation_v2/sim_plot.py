import matplotlib.pyplot as plt
import _thread
from sim_data import sim_data
import multiprocessing
from ctx import ctx


def plot_on_thread():
    pool = multiprocessing.Pool()
    description = ctx.get_description()
    host_dead = [sim_data.timestamps, sim_data.hosts_dead, "Czas [s]", "Liczba martwych żywicieli",
                 f"Śmierć żywicieli w czasie\n{ctx}",
                 f"time_hosts_dead_{description}.png", ["Martwi żywiciele"]]
    food = [sim_data.timestamps, sim_data.foods, "Czas [s]", "Ilość pożywienia",
            f"Zmiana ilości pożywienia w czasie\n{ctx}",
            f"time_food_{description}.png", ["Pożywienie"]]
    carriers = [sim_data.timestamps, sim_data.carriers, "Czas [s]", "Liczba nosicieli",
                f"Zmiana liczby nosicieli w czasie\n{ctx}", f"time_carriers_{description}.png", ["Nosiciele"]]
    SimPlot.plot_sub_plot(sim_data.timestamps, (sim_data.hosts_alive, sim_data.parasites, sim_data.foods), "Czas [s]",
                          "Liczba żywicieli",
                          f"Populacja żywicieli w czasie {ctx}",
                          f"time_hosts_alive_{description}.png", ["Żywiciele", "Pasożyty", "Pożywienie"])
    pool.starmap(SimPlot.plot, [host_dead, food, carriers])


def plot_gen(xs, ys, xlabel, ylabel, title):
    plt.figure(figsize=(18, 15))
    plt.style.use('ggplot')
    plt.grid(linestyle='dashdot', linewidth=2)
    plt.plot(xs, ys, linestyle='--', marker='o')
    plt.xlabel(xlabel, size=16)
    plt.ylabel(ylabel, size=16)
    plt.title(title, size=20)


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
        host, parasite, food = ys
        plot_gen(xs, host, xlabel, ylabel, title)
        plt.plot(xs, parasite, linestyle='--', marker='o')
        plt.plot(xs, food, linestyle='--', marker='o')
        plt.legend(legend)
        plt.savefig(f'plt/{file_name}')
        plt.show()
