import random
import numpy as np
import matplotlib.pyplot as plt

from final_project.city import City

# Reproducibility
random.seed(123)
np.random.seed(123)

# Price ranges for each area
area_rates = {
    0: (100, 200),
    1: (50, 250),
    2: (250, 350),
    3: (150, 450),
}

# -----------------------------
# Run simulation
# -----------------------------
def run_simulation(n_steps=180):
    """Run the simulation for n_steps months."""
    city = City(size=10, area_rates=area_rates)
    city.initialize()
    for _ in range(n_steps):
        city.iterate()
    return city

# -----------------------------
# Compute final host wealth
# -----------------------------
def compute_wealth(city):
    """Compute wealth = profits + current market value of all owned assets."""
    wealth = []
    for host in city.hosts:
        total = host.profits
        for pid in host.assets:
            place = city.places[pid]
            last_price = place.price[max(place.price.keys())]
            total += last_price
        wealth.append((host.host_id, host.area, total))
    return wealth


# -----------------------------
# Main script
# -----------------------------
if __name__ == "__main__":

    # -------------------------
    # 1) ORIGINAL RULE SIMULATION
    # -------------------------
    city = run_simulation()
    wealth = compute_wealth(city)

    # Sort hosts by wealth
    wealth_sorted = sorted(wealth, key=lambda x: x[2])
    ids, areas, values = zip(*wealth_sorted)

    # Colors by area
    palette = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    bar_colors = [palette[a] for a in areas]

    # -------------------------
    # GRAPH 1 — Wealth distribution
    # -------------------------
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(values)), values, color=bar_colors)
    plt.xlabel("Hosts (sorted by wealth)")
    plt.ylabel("Total Wealth")
    plt.title("Wealth Distribution after 180 Months")
    plt.tight_layout()
    plt.savefig("reports/graph1.png")
    plt.close()

    # -------------------------
    # GRAPH 2_v0 — Original rule asset distribution
    # -------------------------
    assets_original = [len(h.assets) for h in city.hosts]

    plt.figure(figsize=(8, 5))
    plt.hist(assets_original, bins=range(0, 15), edgecolor="black")
    plt.xlabel("Number of Properties Owned")
    plt.ylabel("Number of Hosts")
    plt.title("Asset Distribution — Original Rule (v0)")
    plt.tight_layout()
    plt.savefig("reports/graph2_v0.png")
    plt.close()

    # --------------------------------------------------------
    # 2) MODIFIED RULE SIMULATION
    # --------------------------------------------------------
    # Si quieres que v1 use una regla distinta,
    # cambia la función approve_bids en city.py
    # (por ejemplo, ordenar por "bid_price" en lugar de "spread").
    city_mod = run_simulation()

    assets_modified = [len(h.assets) for h in city_mod.hosts]

    # -------------------------
    # GRAPH 2_v1 — Modified rule asset distribution
    # -------------------------
    plt.figure(figsize=(8, 5))
    plt.hist(assets_modified, bins=range(0, 15), edgecolor="black")
    plt.xlabel("Number of Properties Owned")
    plt.ylabel("Number of Hosts")
    plt.title("Asset Distribution — Modified Rule (v1)")
    plt.tight_layout()
    plt.savefig("reports/graph2_v1.png")
    plt.close()

    print("Graphs generated successfully:")
    print("- reports/graph1.png")
    print("- reports/graph2_v0.png")
    print("- reports/graph2_v1.png")