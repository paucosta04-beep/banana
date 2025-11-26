import pandas as pd

from final_project.hosts import Host
from final_project.place import Place


class City:
    """
    Entorno de simulación de la ciudad.
    """

    def __init__(self, size, area_rates, bid_spend_fraction=1.0, cheap_only=False):
        self.size = size
        self.area_rates = area_rates
        self.bid_spend_fraction = bid_spend_fraction
        self.cheap_only = cheap_only
        self.step = 0
        # media de rate por área (constante durante la simulación)
        self.area_mean_rates = {
            k: (low + high) / 2 for k, (low, high) in self.area_rates.items()
        }

    def initialize(self):
        """
        Crea todos los Place y Host y realiza el setup inicial.
        """
        n = self.size

        self.places = [
            Place(place_id=x, host_id=x, city=self)
            for x in range(n * n)
        ]
        for p in self.places:
            p.setup()

        self.hosts = [
            Host(
                host_id=x,
                place=self.places[x],
                city=self,
                bid_spend_fraction=self.bid_spend_fraction,
                cheap_only=self.cheap_only,
            )
            for x in range(n * n)
        ]

    def approve_bids(self, bids):
        """
        Ordena las bids por spread y acepta como máximo:
        - una propiedad por comprador
        - una venta por propiedad
        """
        if not bids:
            return []

        df = pd.DataFrame(bids).sort_values("spread", ascending=False)

        used_buyers = set()
        used_places = set()
        approved = []

        for _, row in df.iterrows():
            buyer = row["buyer_id"]
            pid = row["place_id"]

            if buyer not in used_buyers and pid not in used_places:
                approved.append({
                    "place_id": int(pid),
                    "seller_id": int(row["seller_id"]),
                    "buyer_id": int(buyer),
                    "spread": float(row["spread"]),
                    "bid_price": float(row["bid_price"]),
                })
                used_buyers.add(buyer)
                used_places.add(pid)

        return approved

    def execute_transactions(self, transactions):
        """
        Ejecuta las transacciones aprobadas: mueve dinero, propiedades y
        actualiza el historial de precios.
        """
        for t in transactions:
            buyer = self.hosts[t["buyer_id"]]
            seller = self.hosts[t["seller_id"]]
            place = self.places[t["place_id"]]

            amount = t["bid_price"]

            # movimiento de dinero
            buyer.profits -= amount
            seller.profits += amount

            # movimiento de propiedad
            seller.assets.remove(place.place_id)
            buyer.assets.add(place.place_id)
            place.host_id = buyer.host_id

            # registrar nuevo precio de venta
            place.price[self.step] = amount

    def clear_market(self):
        """
        Recoge todas las bids, selecciona las aprobadas y ejecuta
        las transacciones.
        """
        all_bids = []
        for h in self.hosts:
            all_bids.extend(h.make_bids())

        transactions = self.approve_bids(all_bids)
        if transactions:
            self.execute_transactions(transactions)

        return transactions

    def iterate(self):
        """
        Avanza un mes:
        - incrementa el contador de step
        - actualiza la ocupación de todos los Place
        - actualiza profits de todos los Host
        - limpia el mercado (compra-ventas)
        """
        self.step += 1

        for p in self.places:
            p.update_occupancy()

        for h in self.hosts:
            h.update_profits()

        return self.clear_market()
