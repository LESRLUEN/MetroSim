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
        """Agrega un tren a la línea."""

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

    def __str__(self):
        return (
            f"Línea {self.line_id} - {self.name} | "
            f"Estaciones: {len(self.stations)} | "
            f"Trenes: {len(self.trains)}"
        )