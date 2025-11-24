import os
import random
import matplotlib.pyplot as plt
from final_project.city import City

# reproducibilidad
SEED = 12345
random.seed(SEED)

def ensure_reports():
    os.makedirs("reports", exist_ok=True)

def run_simulation(area_rates, size=10, steps=180, seed=SEED):
    random.seed(seed)
    city = City(size=size, area_rates=area_rates)
    city.initialize()
    for i in range(steps):
        city.iterate()
    return city

def save_graph1(city, filename="reports/graph1.png"):
    wealths = city.compute_wealths()
    wealths_sorted = sorted(wealths, key=lambda x: x[1])
    heights = [w for (_, w, _) in wealths_sorted]
    areas = [a for (_, _, a) in wealths_sorted]

    plt.figure(figsize=(12,6))
    # coloreamos por area (0-3) usando cmap básico
    cmap = plt.get_cmap('tab10')
    colors = [cmap(a) for a in areas]
    plt.bar(range(len(heights)), heights, color=colors)
    plt.title("Wealth per Host (sorted)")
    plt.xlabel("Host (ordenado por riqueza)")
    plt.ylabel("Wealth (profits + último precio de assets)")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def save_graph2_compare(original_city, modified_city, filename_v0="reports/graph2_v0.png", filename_v1="reports/graph2_v1.png"):
    # Distribución del número de assets por host
    def assets_counts(city):
        return [len(h.assets) for h in city.hosts]

    ac0 = assets_counts(original_city)
    ac1 = assets_counts(modified_city)

    plt.figure(figsize=(12,5))
    plt.hist(ac0, bins=range(0, max(ac0)+2))
    plt.title("Distribución número de assets — versión 0 (original)")
    plt.xlabel("Número de assets")
    plt.ylabel("Número de hosts")
    plt.tight_layout()
    plt.savefig(filename_v0)
    plt.close()

    plt.figure(figsize=(12,5))
    plt.hist(ac1, bins=range(0, max(ac1)+2))
    plt.title("Distribución número de assets — versión 1 (modificación)")
    plt.xlabel("Número de assets")
    plt.ylabel("Número de hosts")
    plt.tight_layout()
    plt.savefig(filename_v1)
    plt.close()

if __name__ == "__main__":
    ensure_reports()

    area_rates = {
        0: (100,200),
        1: (50,250),
        2: (250,350),
        3: (150,450),
    }

    # --- corremos versión original (v0) ---
    city_v0 = run_simulation(area_rates, size=10, steps=180, seed=SEED)
    save_graph1(city_v0, filename="reports/graph1.png")

    # --- versión modificada (v1): cambio de regla de puja ---
    # En tu clase tu estilo fue manipular data; aquí vamos a modificar la regla de make_bids
    # de forma sencilla: en v1 el host oferta el ask_price (no todas sus profits).
    import types
    from final_project.hosts import Host

    def make_bids_modified(self):
        opportunities = set()
        for pid in self.assets:
            p = self.city.places[pid]
            for neigh in p.neighbours:
                if neigh not in self.assets:
                    opportunities.add(neigh)

        bids = []
        for pid in opportunities:
            place = self.city.places[pid]
            if len(place.price) == 0:
                ask_price = 0.0
            else:
                last_step = max(place.price.keys())
                ask_price = place.price[last_step]

            if self.profits >= ask_price and ask_price > 0:
                bids.append({
                    'place_id': pid,
                    'seller_id': place.host_id,
                    'buyer_id': self.host_id,
                    'spread': self.profits - ask_price,
                    'bid_price': ask_price  # aqui pujamos solo el ask_price
                })
        return bids

    # creamos city_v1 e "injertamos" make_bids_modified en cada host
    random.seed(SEED)
    city_v1 = City(size=10, area_rates=area_rates)
    city_v1.initialize()
    for h in city_v1.hosts:
        h.make_bids = types.MethodType(make_bids_modified, h)

    for _ in range(180):
        city_v1.iterate()

    save_graph2_compare(city_v0, city_v1,
                        filename_v0="reports/graph2_v0.png",
                        filename_v1="reports/graph2_v1.png")

    print("Simulaciones completadas. Archivos en reports/: graph1.png, graph2_v0.png, graph2_v1.png")