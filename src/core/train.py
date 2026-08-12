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

        # Estado del tren
        self.state = "DETENIDO"

        # Estaciones
        self.current_station = None
        self.next_station = None

    def accelerate(self):
        """
        Aumenta la velocidad del tren.
        """

        self.speed += self.acceleration

        if self.speed >= self.max_speed:
            self.speed = self.max_speed

        self.state = "EN MARCHA"

    def brake(self):
        """
        Reduce la velocidad del tren.
        """

        self.speed -= self.braking

        if self.speed <= 0:
            self.speed = 0.0
            self.state = "DETENIDO"

    def update_position(self):
        """
        Actualiza la posición del tren.

        La velocidad está expresada en km/h.
        La simulación considera una actualización equivalente
        a un segundo.
        """

        distance = self.speed / 3600

        self.position += distance

    def board_passengers(self, amount):
        """
        Permite que pasajeros suban al tren.
        """

        available_space = self.capacity - self.passengers

        boarded = min(amount, available_space)

        self.passengers += boarded

        return boarded

    def leave_passengers(self, amount):
        """
        Permite que pasajeros bajen del tren.
        """

        leaving = min(amount, self.passengers)

        self.passengers -= leaving

        return leaving

    def __str__(self):
        return (
            f"Tren {self.train_id} | "
            f"Velocidad: {self.speed:.1f} km/h | "
            f"Posición: {self.position:.3f} km | "
            f"Pasajeros: {self.passengers}/{self.capacity} | "
            f"Estado: {self.state}"
        )