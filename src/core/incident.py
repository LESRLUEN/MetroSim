from .train import TrainState


class Incident:
    """
    Representa una incidencia temporal que afecta la operación de un tren o tramo.
    """

    def __init__(self, incident_id, description, train, duration, state=TrainState.FALLA):
        self.incident_id = incident_id
        self.description = description
        self.train = train
        self.duration = duration  # Duración en segundos (ticks)
        self.remaining_time = duration
        self.target_state = state
        self.previous_state = None
        self.active = False

    def trigger(self):
        """Activa la incidencia en el tren afectado."""
        self.active = True
        self.previous_state = self.train.state
        self.train.state = self.target_state
        print(f"\n [INCIDENCIA ACTIVADA] {self.train.train_id}: {self.description} ({self.duration}s)\n")

    def update(self):
        """Disminuye el tiempo restante y resuelve la incidencia al finalizar."""
        if not self.active:
            return

        self.remaining_time -= 1.0

        if self.remaining_time <= 0:
            self.resolve()

    def resolve(self):
        """Restaura el estado operativo del tren."""
        self.active = False
        # Si el tren estaba en estación al fallar, retorna a EN_ESTACION; si no, a ESPERANDO_SALIDA
        if self.previous_state in (TrainState.PUERTAS_ABIERTAS, TrainState.ABRIENDO_PUERTAS, TrainState.EN_ESTACION):
            self.train.state = TrainState.EN_ESTACION
        else:
            self.train.state = TrainState.ESPERANDO_SALIDA

        print(f"\n [INCIDENCIA RESUELTA] {self.train.train_id}: Servicio normalizado.\n")