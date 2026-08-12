class Line:
    """
    Representa una línea ferroviaria dentro de MetroSim.
    """

    def __init__(self, line_id, name):
        self.line_id = line_id
        self.name = name

        self.stations = []
        self.trains = []

    def add_station(self, station):
        """Agrega una estación a la línea."""

        self.stations.append(station)

    def add_train(self, train):
        """Agrega un tren a la línea y le asigna la referencia de la línea."""
        train.line = self
        self.trains.append(train)

    def remove_station(self, station_id):
        """Elimina una estación utilizando su ID."""

        self.stations = [
            station
            for station in self.stations
            if station.station_id != station_id
        ]

    def remove_train(self, train_id):
        """Elimina un tren utilizando su ID."""

        self.trains = [
            train
            for train in self.trains
            if train.train_id != train_id
        ]

    def get_station(self, station_id):
        """Busca una estación por su ID."""

        for station in self.stations:
            if station.station_id == station_id:
                return station

        return None

    def get_train(self, train_id):
        """Busca un tren por su ID."""

        for train in self.trains:
            if train.train_id == train_id:
                return train

        return None

    def get_next_station(self, current_station):
        """
        Dada una estación actual, retorna la siguiente estación en la línea.
        Retorna None si es la terminal final.
        """
        if current_station not in self.stations:
            return None

        current_index = self.stations.index(current_station)
        if current_index + 1 < len(self.stations):
            return self.stations[current_index + 1]

        return None

    def __str__(self):
        return (
            f"Línea {self.line_id} - {self.name} | "
            f"Estaciones: {len(self.stations)} | "
            f"Trenes: {len(self.trains)}"
        )