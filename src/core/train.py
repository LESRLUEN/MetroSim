from enum import Enum, auto

class TrainState(Enum):
    """Estados posibles de la máquina de estados del tren."""
    DETENIDO = auto()
    ACELERANDO = auto()
    EN_MARCHA = auto()
    FRENANDO = auto()
    EN_ESTACION = auto()

class Train:
    """
    Representa un tren dentro del sistema MetroSim.
    """
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

        # Estado inicial usando Enum
        self.state = TrainState.DETENIDO

        # Estaciones
        self.current_station = None
        self.next_station = None

    def update(self):
        """
        Máquina de estados finita (FSM).
        Se ejecuta en cada tick de la simulación.
        """
        distance = self.distance_to_next_station()

        if distance is None:
            return

        # Si estamos a menos de 1 metro (0.001 km), consideramos llegada exitosa
        if distance <= 0.001:
            self.position = self.next_station.position
            self.speed = 0.0
            self.state = TrainState.EN_ESTACION
            return

        # Distancia teórica física de frenado (km)
        braking_distance = (self.speed ** 2) / (2 * self.braking * 3600)

        # Margen dinámico: 10% adicional por seguridad física + 1 metro de tolerancia
        safety_braking_distance = (braking_distance * 1.1) + 0.001

        # Solo frena si el tren está en movimiento y la distancia es crítica
        if self.speed > 0 and distance <= safety_braking_distance:
            self.brake()
            self.state = TrainState.FRENANDO
        elif self.speed < self.max_speed:
            self.accelerate()
            self.state = TrainState.ACELERANDO
        else:
            self.state = TrainState.EN_MARCHA

        self.update_position()

    def accelerate(self):
        """Aumenta la velocidad del tren."""
        self.speed += self.acceleration
        if self.speed >= self.max_speed:
            self.speed = self.max_speed

    def brake(self):
        """Reduce la velocidad del tren."""
        self.speed -= self.braking
        if self.speed <= 0:
            self.speed = 0.0

    def update_position(self):
        """Actualiza la posición del tren."""
        distance = self.speed / 3600
        self.position += distance

    def distance_to_next_station(self):
        """Calcula la distancia restante hasta la siguiente estación."""
        if self.next_station is None:
            return None
        distance = self.next_station.position - self.position
        return max(distance, 0.0)

    # ... (mantén tus métodos board_passengers, leave_passengers intactos)

    def __str__(self):
        # Actualizamos el print para mostrar el nombre del Enum (ej. "EN_MARCHA" en vez de <TrainState.EN_MARCHA: 3>)
        next_station = self.next_station.station_id if self.next_station else "N/A"
        distance = self.distance_to_next_station()
        distance_text = f"{distance:.3f} km" if distance is not None else "N/A"

        return (
            f"Tren {self.train_id} | "
            f"Velocidad: {self.speed:.1f} km/h | "
            f"Posición: {self.position:.3f} km | "
            f"Destino: {next_station} | "
            f"Distancia: {distance_text} | "
            f"Pasajeros: {self.passengers}/{self.capacity} | "
            f"Estado: {self.state.name}"
        )