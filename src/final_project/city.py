import pandas as pd
from final_project.hosts import Host
from final_project.place import Place

class City:
    """
    Ciudad: entorno de simulación con grid size x size y reglas de mercado.
    """
    def __init__(self, size: int, area_rates: dict):
        self.size = size
        self.area_rates = area_rates
        self.step = 0
        self.places = []
        self.hosts = []

    def initialize(self):
        """
        Crea todos los Place y Host iniciales. Cada place lo posee un host con mismo id.
        """
        n = self.size
        places = [Place(place_id=x, host_id=x, city=self) for x in range(n*n)]
        for p in places:
            p.setup()
        self.places = places

        hosts = [Host(host_id=x, place=places[x], city=self) for x in range(n*n)]
        self.hosts = hosts

    def area_mean_rate(self, area: int):
        """
        Calcula la media de tarifas nightly rate en el área dada.
        """
        rates = [p.rate for p in self.places if p.area == area]
        return 0.0 if len(rates) == 0 else sum(rates) / len(rates)

    def update_profits(self):
        """
        Llama a update_profits de cada host.
        """
        for h in self.hosts:
            h.update_profits()

    def make_all_bids(self):
        """
        Recoge todas las bids de todos los hosts.
        """
        bids = []
        for h in self.hosts:
            bids.extend(h.make_bids())
        return bids

    def approve_bids(self, bids):
        """
        Convierte bids a DataFrame, ordena por 'spread' desc y aprueba:
         - un buyer puede comprar a lo sumo 1 place por iteración
         - cada place puede venderse a lo sumo 1 vez por iteración
        Devuelve lista de transacciones aprobadas.
        """
        if not bids:
            return []

        df = pd.DataFrame(bids)
        if df.empty:
            return []

        df_sorted = df.sort_values('spread', ascending=False)
        bought = set()
        sold = set()
        approved = []

        for _, row in df_sorted.iterrows():
            pid = int(row['place_id'])
            buyer = int(row['buyer_id'])
            seller = int(row['seller_id'])

            # buyer compra a lo sumo 1; place se vende una sola vez; evitar self-trade
            if (buyer not in bought) and (pid not in sold) and (buyer != seller):
                approved.append({
                    'place_id': pid,
                    'seller_id': seller,
                    'buyer_id': buyer,
                    'bid_price': float(row['bid_price']),
                    'spread': float(row['spread'])
                })
                bought.add(buyer)
                sold.add(pid)
        return approved

    def execute_transactions(self, transactions):
        """
        Realiza transferencia de dinero y propiedad para cada transacción aprobada.
        """
        for t in transactions:
            pid = t['place_id']
            buyer_id = t['buyer_id']
            seller_id = t['seller_id']
            bid_price = float(t['bid_price'])

            buyer = self.hosts[buyer_id]
            seller = self.hosts[seller_id]
            place = self.places[pid]

            # transferir fondos
            buyer.profits -= bid_price
            seller.profits += bid_price

            # actualizar assets
            buyer.assets.add(pid)
            if pid in seller.assets:
                seller.assets.remove(pid)

            # actualizar owner y historial de precio
            place.host_id = buyer_id
            place.price[self.step] = bid_price

    def clear_market(self):
        """
        Recolecta bids, aprueba y ejecuta transacciones.
        """
        bids = self.make_all_bids()
        approved = self.approve_bids(bids)
        if approved:
            self.execute_transactions(approved)
        return approved

    def iterate(self):
        """
        Avanza una iteración mensual:
         - incrementar step
         - actualizar occupancies
         - actualizar profits
         - limpiar mercado
        """
        self.step += 1

        for p in self.places:
            p.update_occupancy()

        # update profits después de occupancy actualizada
        for h in self.hosts:
            h.update_profits()

        transactions = self.clear_market()
        return transactions

    def compute_wealths(self):
        """
        Calcula la riqueza de cada host = profits actuales + último precio de todas sus propiedades.
        Devuelve lista de tuplas (host_id, wealth, area).
        """
        wealths = []
        for h in self.hosts:
            assets_value = 0.0
            for pid in h.assets:
                place = self.places[pid]
                latest = place.price[max(place.price.keys())] if place.price else 0.0
                assets_value += latest
            wealth = h.profits + assets_value
            wealths.append((h.host_id, wealth, h.area))
        return wealths