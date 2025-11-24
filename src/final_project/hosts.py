class Host:
    """
    Representa un host (propietario) que posee uno o más Place.
    """
    def __init__(self, host_id: int, place, city, profits: float = 0.0):
        self.host_id = host_id
        self.city = city
        self.profits = float(profits)

        # area inicial y activos (assets) a partir del place inicial
        self.area = place.area
        self.assets = set([place.place_id])

    def update_profits(self):
        """
        Suma a self.profits la renta generada por cada asset en el paso actual:
        rate * occupancy
        """
        total = 0.0
        for pid in list(self.assets):
            place = self.city.places[pid]
            total += place.rate * place.occupancy
        self.profits += total

    def make_bids(self):
        """
        Identifica oportunidades (vecinos de cualquiera de sus assets no poseídos)
        y crea bids si tiene suficiente 'profits' para pagar el ask_price.
        El ask_price es el último valor en place.price (precio de venta actual).
        Devuelve lista de dicts con las pujas.
        """
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

            # condición de compra: profits >= ask_price y ask_price > 0
            if self.profits >= ask_price and ask_price > 0:
                bids.append({
                    'place_id': pid,
                    'seller_id': place.host_id,
                    'buyer_id': self.host_id,
                    'spread': self.profits - ask_price,
                    'bid_price': self.profits  # en la versión original ofertan todo su dinero
                })
        return bids