class Simulation:
    def __init__(self, tick_duration=1.0):
        self.tick_duration = tick_duration
        self.current_time = 0.0
        self.lines = []
        self.incidents = []  # <-- Lista de incidencias

    def add_line(self, line):
        self.lines.append(line)

    def add_incident(self, incident):
        self.incidents.append(incident)

    def update(self):
        """Actualiza el estado global de la simulación."""
        self.current_time += self.tick_duration

        # Actualizar incidencias
        for incident in self.incidents:
            if incident.active:
                incident.update()

        for line in self.lines:
            for station in line.stations:
                station.update()

            for train in line.trains:
                train.update()