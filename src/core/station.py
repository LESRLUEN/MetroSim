class Station:
    """
    Representa una estación dentro de la red ferroviaria.
    """

    def __init__(self, station_id, name, position, spawn_rate=0.0):
        self.station_id = station_id
        self.name = name
        self.position = position

        # Pasajeros esperando en el andén
        self.passengers_waiting = 0

        # Generación dinámica de demanda
        self.spawn_rate = spawn_rate  # Pasajeros/segundo (ej. 0.5 = 1 pasajero cada 2s)
        self._passenger_accumulator = 0.0

    def update(self):
        """Genera pasajeros dinámicamente según la tasa de afluencia."""
        if self.spawn_rate <= 0:
            return

        self._passenger_accumulator += self.spawn_rate
        new_passengers = int(self._passenger_accumulator)

        if new_passengers > 0:
            self.passengers_waiting += new_passengers
            self._passenger_accumulator -= new_passengers

    def add_passengers(self, amount):
        """Agrega pasajeros esperando en la estación."""
        self.passengers_waiting += amount

    def remove_passengers(self, amount):
        """Retira pasajeros de la estación."""
        amount = min(amount, self.passengers_waiting)
        self.passengers_waiting -= amount
        return amount

    def __str__(self):
        return (
            f"{self.station_id} - {self.name} | "
            f"Posición: {self.position:.2f} km | "
            f"Pasajeros en andén: {self.passengers_waiting} | "
            f"Afluencia: {self.spawn_rate:.2f} pas/s"
        )