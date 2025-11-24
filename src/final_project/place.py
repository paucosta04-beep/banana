import random
import numpy as np

class Place:
    """
    Representa un anuncio tipo Airbnb en el grid de la ciudad.
    """

    def __init__(self, place_id, host_id, city):
        self.place_id = place_id
        self.host_id = host_id
        self.city = city

    def setup(self):
        """
        Define vecinos, área, precio inicial (rate) e historial de precios.
        """
        n = self.city.size

        # coordenadas en el grid
        x = self.place_id % n
        y = self.place_id // n

        # posibles vecinos (8 celdas alrededor)
        neighbours_xy = [
            (x - 1, y - 1), (x,     y - 1), (x + 1, y - 1),
            (x - 1, y    ),               (x + 1, y    ),
            (x - 1, y + 1), (x,     y + 1), (x + 1, y + 1),
        ]

        # filtramos los que están dentro del grid y los pasamos a place_id
        self.neighbours = [
            i + j * n
            for (i, j) in neighbours_xy
            if 0 <= i < n and 0 <= j < n
        ]

        # cuadrante (0 abajo-izq, 1 abajo-dcha, 2 arriba-izq, 3 arriba-dcha)
        self.area = (x >= n / 2) + 2 * (y >= n / 2)

        # precio por noche según área
        low, high = self.city.area_rates[self.area]
        self.rate = random.uniform(low, high)

        # historial de precios de compraventa
        self.price = {0: 900 * self.rate}

        # ocupación del mes (días alquilados)
        self.occupancy = 0

    def update_occupancy(self):
        """
        Actualiza la ocupación según si su rate está por encima o por debajo
        de la media de precios de su área.
        """
        area_rates = [p.rate for p in self.city.places if p.area == self.area]
        mean_rate = float(np.mean(area_rates))

        if self.rate > mean_rate:
            # más caro que la media → menos días ocupados
            self.occupancy = random.randint(5, 15)
        else:
            # más barato o igual → más días ocupados
            self.occupancy = random.randint(10, 20)