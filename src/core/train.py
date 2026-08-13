from enum import Enum, auto


class TrainState(Enum):
    DETENIDO = auto()
    ACELERANDO = auto()
    EN_MARCHA = auto()
    FRENANDO = auto()
    EN_ESTACION = auto()
    ABRIENDO_PUERTAS = auto()
    PUERTAS_ABIERTAS = auto()
    CERRANDO_PUERTAS = auto()
    ESPERANDO_SALIDA = auto()
    FALLA = auto()  # <-- Avería mecánica / traba de puertas
    EMERGENCIA = auto()  # <-- Frenado de emergencia por usuario u obstrucción


class Train:
    def __init__(
            self,
            train_id,
            capacity=1200,
            max_speed=60.0
    ):
        self.train_id = train_id
        self.capacity = capacity
        self.passengers = 0

        self.position = 0.0
        self.speed = 0.0
        self.direction = 1  # 1: Ida (ascendente), -1: Vuelta (descendente)

        self.max_speed = max_speed
        self.acceleration = 1.0
        self.braking = 2.0

        self.dwell_time = 10.0
        self.dwell_timer = 0.0

        self.state = TrainState.DETENIDO
        self.line = None
        self.current_station = None
        self.next_station = None

    def update(self):

        """Máquina de estados finita (FSM) con control de incidencias."""
        # Si el tren está en falla o emergencia, frena completamente y congela su estado
        if self.state in (TrainState.FALLA, TrainState.EMERGENCIA):
            self.brake()
            return

        """Máquina de estados finita (FSM) con control de distancia de seguridad."""
        if self.state in (
            TrainState.EN_ESTACION,
            TrainState.ABRIENDO_PUERTAS,
            TrainState.PUERTAS_ABIERTAS,
            TrainState.CERRANDO_PUERTAS,
            TrainState.ESPERANDO_SALIDA
        ):
            self._handle_station_sequence()
            return

        # 1. Distancia a la estación objetiva
        dist_station = self.distance_to_next_station()

        # 2. Distancia al tren que circula adelante (si existe)
        dist_train_ahead = None
        if self.line:
            ahead = self.line.get_train_ahead(self)
            if ahead:
                # Se aplica un margen de seguridad rígido de 0.050 km (50 metros)
                dist_train_ahead = max(abs(ahead.position - self.position) - 0.050, 0.0)

        # 3. Determinar la distancia restrictiva más próxima
        distances = [d for d in (dist_station, dist_train_ahead) if d is not None]
        if not distances:
            return

        effective_distance = min(distances)

        # 4. Condición de llegada a estación
        if dist_station is not None and effective_distance == dist_station and dist_station <= 0.001:
            self.position = self.next_station.position
            self.speed = 0.0
            self.current_station = self.next_station
            self.state = TrainState.EN_ESTACION
            return

        # 5. Cálculo de distancia de frenado
        braking_distance = (self.speed ** 2) / (2 * self.braking * 3600)
        safety_braking_distance = (braking_distance * 1.1) + 0.001

        # 6. Toma de decisiones cinemáticas
        if self.speed > 0 and effective_distance <= safety_braking_distance:
            self.brake()
            self.state = TrainState.FRENANDO
        elif self.speed < self.max_speed:
            self.accelerate()
            self.state = TrainState.ACELERANDO
        else:
            self.state = TrainState.EN_MARCHA

        self.update_position()

    def _handle_station_sequence(self):
        """Gestiona la secuencia temporal dentro de la estación e inversión en terminales."""
        if self.state == TrainState.EN_ESTACION:
            self.state = TrainState.ABRIENDO_PUERTAS

        elif self.state == TrainState.ABRIENDO_PUERTAS:
            self.state = TrainState.PUERTAS_ABIERTAS
            self.dwell_timer = self.dwell_time

            if self.current_station:
                # Si en la dirección actual no hay más estaciones, es terminal (bajan todos)
                next_check = self.line.get_next_station(self.current_station, self.direction) if self.line else None
                leaving_ratio = 1.0 if next_check is None else 0.4

                passengers_leaving = int(self.passengers * leaving_ratio)
                self.leave_passengers(passengers_leaving)

                waiting = self.current_station.passengers_waiting
                if waiting > 0:
                    boarded = self.board_passengers(waiting)
                    self.current_station.remove_passengers(boarded)

        elif self.state == TrainState.PUERTAS_ABIERTAS:
            self.dwell_timer -= 1.0
            if self.dwell_timer <= 0:
                self.state = TrainState.CERRANDO_PUERTAS

        elif self.state == TrainState.CERRANDO_PUERTAS:
            self.state = TrainState.ESPERANDO_SALIDA

        elif self.state == TrainState.ESPERANDO_SALIDA:
            if self.line:
                next_st = self.line.get_next_station(self.current_station, self.direction)

                # Inversión de marcha si alcanzamos la terminal
                if next_st is None:
                    self.direction *= -1
                    next_st = self.line.get_next_station(self.current_station, self.direction)

                if next_st:
                    self.next_station = next_st
                    self.accelerate()
                    self.state = TrainState.ACELERANDO
                else:
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
        """Actualiza la posición avanzando o retrocediendo según la dirección."""
        distance_step = (self.speed / 3600) * self.direction
        self.position += distance_step

    def distance_to_next_station(self):
        """Calcula la distancia absoluta restante a la siguiente estación."""
        if self.next_station is None:
            return None
        distance = abs(self.next_station.position - self.position)
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
        dir_text = "→" if self.direction == 1 else "←"

        return (
            f"Tren {self.train_id} {dir_text} | "
            f"Velocidad: {self.speed:.1f} km/h | "
            f"Posición: {self.position:.3f} km | "
            f"Destino: {next_station} | "
            f"Distancia: {distance_text} | "
            f"Pasajeros: {self.passengers}/{self.capacity} | "
            f"Estado: {self.state.name}"
        )