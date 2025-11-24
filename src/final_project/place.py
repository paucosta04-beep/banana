import random

class Place:
    """
    Representa una propiedad (listing) en la cuadrícula.
    """
    def __init__(self, place_id: int, host_id: int, city):
        self.place_id = place_id
        self.host_id = host_id
        self.city = city

        # atributos inicializados en setup()
        self.neighbours = []
        self.area = None
        self.rate = None
        self.price = {}      # historial de precios: {step: price}
        self.occupancy = 0

    def setup(self):
        """
        Calcular x,y, vecinos, área (cuadrante), tarifa inicial y precio inicial.
        """
        n = self.city.size
        x = self.place_id % n
        y = self.place_id // n

        # vecinos en 8 direcciones (si existen dentro del grid)
        neighbours = [
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y  ),           (x+1, y  ),
            (x-1, y+1), (x, y+1), (x+1, y+1)
        ]
        valid = [(i, j) for i, j in neighbours if 0 <= i < n and 0 <= j < n]
        self.neighbours = [i + j * n for i, j in valid]

        # area: 0 bottom-left, 1 bottom-right, 2 top-left, 3 top-right
        self.area = (x >= n/2) + 2 * (y >= n/2)

        # tarifa nocturna uniforme dentro del rango del área
        low, high = self.city.area_rates[self.area]
        self.rate = random.uniform(low, high)

        # precio inicial (según enunciado): 900 * rate
        self.price = {0: 900 * self.rate}

    def update_occupancy(self):
        """
        Actualiza self.occupancy según si self.rate > tasa media del área.
        Si rate > media -> ocupación aleatoria 5-15; sino 10-20 (días/mes).
        """
        area_mean = self.city.area_mean_rate(self.area)
        if self.rate > area_mean:
            self.occupancy = random.randint(5, 15)
        else:
            self.occupancy = random.randint(10, 20)