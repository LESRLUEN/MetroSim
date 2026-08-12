from enum import Enum, auto


class TrainState(Enum):
    """Estados posibles de la máquina de estados del tren."""
    DETENIDO = auto()
    ACELERANDO = auto()
    EN_MARCHA = auto()
    FRENANDO = auto()
    EN_ESTACION = auto()
    ABRIENDO_PUERTAS = auto()
    PUERTAS_ABIERTAS = auto()
    CERRANDO_PUERTAS = auto()
    ESPERANDO_SALIDA = auto()


class Train:
    def __init__(
            self,
            train_id,
            capacity=1200,
            max_speed=60.0
    ):
        self.train_id = train_id

        # Capacidad y pasajeros
        self.capacity = capacity
        self.passengers = 0

        # Movimiento
        self.position = 0.0
        self.speed = 0.0

        # Parámetros de operación
        self.max_speed = max_speed
        self.acceleration = 1.0
        self.braking = 2.0

        # Tiempos de operación (en ticks/segundos)
        self.dwell_time = 10.0  # Tiempo que duran las puertas abiertas
        self.dwell_timer = 0.0

        # Estado inicial
        self.state = TrainState.DETENIDO

        # Estaciones y Línea
        self.line = None
        self.current_station = None
        self.next_station = None

    def update(self):
        """Máquina de estados finita (FSM)."""

        # 1. Si el tren está realizando la secuencia de estación
        if self.state in (
                TrainState.EN_ESTACION,
                TrainState.ABRIENDO_PUERTAS,
                TrainState.PUERTAS_ABIERTAS,
                TrainState.CERRANDO_PUERTAS,
                TrainState.ESPERANDO_SALIDA
        ):
            self._handle_station_sequence()
            return

        # 2. Conducción hacia la siguiente estación
        distance = self.distance_to_next_station()

        if distance is None:
            return

        # Llegada a estación
        if distance <= 0.001:
            self.position = self.next_station.position
            self.speed = 0.0
            self.current_station = self.next_station
            self.state = TrainState.EN_ESTACION
            return

        # Distancia teórica física de frenado (km)
        braking_distance = (self.speed ** 2) / (2 * self.braking * 3600)
        safety_braking_distance = (braking_distance * 1.1) + 0.001

        if self.speed > 0 and distance <= safety_braking_distance:
            self.brake()
            self.state = TrainState.FRENANDO
        elif self.speed < self.max_speed:
            self.accelerate()
            self.state = TrainState.ACELERANDO
        else:
            self.state = TrainState.EN_MARCHA

        self.update_position()

    def _handle_station_sequence(self):
        """Gestiona la secuencia temporal dentro de la estación."""

        if self.state == TrainState.EN_ESTACION:
            self.state = TrainState.ABRIENDO_PUERTAS

        elif self.state == TrainState.ABRIENDO_PUERTAS:
            self.state = TrainState.PUERTAS_ABIERTAS
            self.dwell_timer = self.dwell_time

        elif self.state == TrainState.PUERTAS_ABIERTAS:
            self.dwell_timer -= 1.0
            if self.dwell_timer <= 0:
                self.state = TrainState.CERRANDO_PUERTAS

        elif self.state == TrainState.CERRANDO_PUERTAS:
            self.state = TrainState.ESPERANDO_SALIDA

        elif self.state == TrainState.ESPERANDO_SALIDA:
            # Calcular siguiente estación si estamos asignados a una línea
            if self.line:
                next_st = self.line.get_next_station(self.current_station)
                if next_st:
                    self.next_station = next_st
                    self.accelerate()
                    self.state = TrainState.ACELERANDO
                else:
                    # Fin de terminal / Fin de línea
                    self.state = TrainState.DETENIDO

    def accelerate(self):
        self.speed += self.acceleration
        if self.speed >= self.max_speed:
            self.speed = self.max_speed

    def brake(self):
        self.speed -= self.braking
        if self.speed <= 0:
            self.speed = 0.0

    def update_position(self):
        distance = self.speed / 3600
        self.position += distance

    def distance_to_next_station(self):
        if self.next_station is None:
            return None
        distance = self.next_station.position - self.position
        return max(distance, 0.0)

    def board_passengers(self, amount):
        available_space = self.capacity - self.passengers
        boarded = min(amount, available_space)
        self.passengers += boarded
        return boarded

    def leave_passengers(self, amount):
        leaving = min(amount, self.passengers)
        self.passengers -= leaving
        return leaving

    def __str__(self):
        next_station = self.next_station.station_id if self.next_station else "N/A"
        distance = self.distance_to_next_station()
        distance_text = f"{distance:.3f} km" if distance is not None else "N/A"

        return (
            f"Tren {self.train_id} | "
            f"Velocidad: {self.speed:.1f} km/h | "
            f"Posición: {self.position:.3f} km | "
            f"Destino: {next_station} | "
            f"Distancia: {distance_text} | "
            f"Estado: {self.state.name}"
        )