class Station:
    """
    Representa una estación dentro de la red ferroviaria.
    """

    def __init__(self, station_id, name, position):
        self.station_id = station_id
        self.name = name
        self.position = position

        # Pasajeros esperando en el andén
        self.passengers_waiting = 0

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
            f"Pasajeros: {self.passengers_waiting}"
        )