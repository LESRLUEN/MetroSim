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

    def get_next_station(self, current_station, direction=1):
        """
        Dada una estación actual y una dirección (1: ida, -1: vuelta),
        retorna la siguiente estación en la línea.
        Retorna None si se alcanzó la terminal en esa dirección.
        """
        if current_station not in self.stations:
            return None

        current_index = self.stations.index(current_station)
        next_index = current_index + direction

        if 0 <= next_index < len(self.stations):
            return self.stations[next_index]

        return None

    def get_train_ahead(self, train):
        """
        Retorna el tren que circula inmediatamente adelante en el mismo sentido,
        o None si no hay ningún tren adelante.
        """
        trains_ahead = []

        for other in self.trains:
            if other.train_id == train.train_id:
                continue

            # Mismo sentido de circulación
            if other.direction == train.direction:
                # Sentido Ida (1): El otro está en una posición mayor
                if train.direction == 1 and other.position > train.position:
                    dist = other.position - train.position
                    trains_ahead.append((dist, other))

                # Sentido Vuelta (-1): El otro está en una posición menor
                elif train.direction == -1 and other.position < train.position:
                    dist = train.position - other.position
                    trains_ahead.append((dist, other))

        if not trains_ahead:
            return None

        # Ordenar por cercanía y retornar el más próximo
        trains_ahead.sort(key=lambda x: x[0])
        return trains_ahead[0][1]

    def __str__(self):
        return (
            f"Línea {self.line_id} - {self.name} | "
            f"Estaciones: {len(self.stations)} | "
            f"Trenes: {len(self.trains)}"
        )