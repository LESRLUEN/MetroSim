import time


class Simulation:
    """Motor principal de simulación de MetroSim."""

    def __init__(self):
        self.current_time = 0.0
        self.running = False
        self.lines = []
        self.tick_duration = 1.0

    def add_line(self, line):
        self.lines.append(line)

    def update(self):
        """Actualiza el estado de todos los elementos durante un intervalo de tiempo."""
        self.current_time += self.tick_duration

        for line in self.lines:
            # Actualizar afluencia de pasajeros en estaciones
            for station in line.stations:
                station.update()

            # Actualizar movimiento y FSM de trenes
            for train in line.trains:
                train.update()

    def start(self):
        self.running = True
        print("Simulación iniciada.")
        while self.running:
            start_time = time.time()

            self.update()

            elapsed_time = time.time() - start_time
            sleep_time = self.tick_duration - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self):
        self.running = False
        print("Simulación detenida.")