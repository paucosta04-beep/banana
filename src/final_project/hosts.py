class Host:
    """
    Representa un propietario de uno o más anuncios.
    """

    def __init__(self, host_id, place, city, profits=0):
        self.host_id = host_id
        self.city = city
        self.profits = profits
        self.area = place.area           # área de origen
        self.assets = set([place.place_id])  # IDs de propiedades que posee

    def update_profits(self):
        """
        Suma a self.profits los ingresos de todas sus propiedades
        en la iteración actual: rate * occupancy.
        """
        for pid in self.assets:
            place = self.city.places[pid]
            self.profits += place.rate * place.occupancy

    def make_bids(self):
        """
        Genera ofertas para comprar propiedades vecinas.

        Devuelve una lista de diccionarios con:
        - place_id
        - seller_id
        - buyer_id
        - spread
        - bid_price
        """
        opportunities = set()

        # oportunidades: vecinos de cualquiera de sus propiedades
        for pid in self.assets:
            place = self.city.places[pid]
            for neigh in place.neighbours:
                if neigh not in self.assets:
                    opportunities.add(neigh)

        bids = []
        for pid in opportunities:
            place = self.city.places[pid]

            # precio de venta actual = último valor del historial
            last_step = max(place.price.keys())
            ask_price = place.price[last_step]

            if self.profits >= ask_price:
                spread = self.profits - ask_price
                bids.append({
                    "place_id": pid,
                    "seller_id": place.host_id,
                    "buyer_id": self.host_id,
                    "spread": spread,
                    "bid_price": self.profits,
                })

        return bids