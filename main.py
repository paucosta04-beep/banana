# main.py
import random
import numpy as np
import matplotlib.pyplot as plt

from final_project.city import City

# reproducibilidad
random.seed(123)
np.random.seed(123)

area_rates = {
    0: (100, 200),
    1: (50, 250),
    2: (250, 350),
    3: (150, 450),
}


def run_simulation(n_steps=180):
    """Ejecuta la simulación durante n_steps meses."""
    city = City(size=10, area_rates=area_rates)
    city.initialize()
    for _ in range(n_steps):
        city.iterate()
    return city


def compute_wealth(city):
    """
    Calcula la riqueza de cada host:
    profits actuales + valor actual de todas sus propiedades
    (último precio registrado).
    """
    wealth = []
    for host in city.hosts:
        value = host.profits
        for pid in host.assets:
            place = city.places[pid]
            last_price = place.price[max(place.price.keys())]
            value += last_price
        wealth.append((host.host_id, host.area, value))
    return wealth


if __name__ == "__main__":
    city = run_simulation()
    wealth = compute_wealth(city)

    # ordenar de menor a mayor riqueza
    wealth_sorted = sorted(wealth, key=lambda x: x[2])
    ids, areas, values = zip(*wealth_sorted)

    # colores por área de origen
    palette = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    bar_colors = [palette[a] for a in areas]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(values)), values, color=bar_colors)
    plt.xlabel("Hosts (ordenados por riqueza)")
    plt.ylabel("Riqueza total")
    plt.title("Distribución de riqueza de los hosts tras 180 meses")
    plt.tight_layout()
    plt.savefig("reports/graph1.png")