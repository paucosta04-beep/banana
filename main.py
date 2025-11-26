# main.py
import os
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

# permitir import del paquete desde src/ sin instalar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

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


def run_simulation(n_steps=180, bid_spend_fraction=1.0, cheap_only=False, seed=123):
    """Ejecuta la simulación durante n_steps meses."""
    random.seed(seed)
    np.random.seed(seed)

    city = City(
        size=10,
        area_rates=area_rates,
        bid_spend_fraction=bid_spend_fraction,
        cheap_only=cheap_only,
    )
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
    # versión original: puja con 100% del cash, sin filtro de “propiedad barata”
    city = run_simulation(bid_spend_fraction=1.0, cheap_only=False, seed=123)
    wealth = compute_wealth(city)

    # ordenar de menor a mayor riqueza
    wealth_sorted = sorted(wealth, key=lambda x: x[2])
    ids, areas, values = zip(*wealth_sorted)

    # colores por área de origen
    palette = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    bar_colors = [palette[a] for a in areas]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(values)), values, color=bar_colors)
    plt.xlabel("Hosts (sorted by wealth)")
    plt.ylabel("Total wealth")
    plt.title("Host wealth after 180 months")
    plt.tight_layout()
    plt.savefig("reports/graph1.png")
    plt.close()

    # Gráfico adicional: distribución de activos con regla original
    asset_counts_v0 = [len(h.assets) for h in city.hosts]
    max_assets = max(asset_counts_v0)
    plt.figure(figsize=(8, 4))
    plt.hist(asset_counts_v0, bins=range(0, max_assets + 2), edgecolor="black")
    plt.xlabel("Properties per host")
    plt.ylabel("Number of hosts")
    plt.ylim(0, 55)  # same y-axis across versions
    plt.title("Asset distribution (original: spend 100%, any neighbor)")
    plt.figtext(
        0.99,
        0.01,
        "Rule: bids use all profits, no price filter",
        ha="right",
        va="bottom",
        fontsize=8,
    )
    plt.tight_layout()
    plt.savefig("reports/graph2_v0.png")
    plt.close()

    # Versión modificada: solo compra si el rate del vecino <= media del área
    city_v1 = run_simulation(bid_spend_fraction=1.0, cheap_only=True, seed=123)
    asset_counts_v1 = [len(h.assets) for h in city_v1.hosts]
    max_assets_v1 = max(asset_counts_v1)
    plt.figure(figsize=(8, 4))
    plt.hist(asset_counts_v1, bins=range(0, max_assets_v1 + 2), edgecolor="black")
    plt.xlabel("Properties per host")
    plt.ylabel("Number of hosts")
    plt.ylim(0, 55)  # same y-axis across versions
    plt.title("Asset distribution (modified: buy only below area-average rate)")
    plt.figtext(
        0.99,
        0.01,
        "Rule: only bid if place rate <= area average",
        ha="right",
        va="bottom",
        fontsize=8,
    )
    plt.tight_layout()
    plt.savefig("reports/graph2_v1.png")
    plt.close()
