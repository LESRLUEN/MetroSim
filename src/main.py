import sys
from PySide6.QtWidgets import QApplication

from core.station import Station
from core.train import Train, TrainState
from core.line import Line
from core.simulation import Simulation
from ui.main_window import MainWindow


class ScheduledSimulation(Simulation):
    """Extensión de Simulation para despachar trenes en intervalos programados."""

    def __init__(self, train2_ref, tick_duration=1.0):
        super().__init__(tick_duration)
        self.train2 = train2_ref
        self.dispatched = False

    def update(self):
        # Despachar M-002 cuando el tiempo alcance los 40 segundos (Headway)
        if not self.dispatched and self.current_time >= 40.0:
            self.train2.state = TrainState.EN_ESTACION
            self.dispatched = True
            print("🟢 [DESPACHO] Tren M-002 iniciado en Terminal Norte")

        super().update()


def main():
    line = Line("L1", "Línea 1 - MetroSim")

    stations = [
        Station("S01", "Terminal Norte", 0.0, spawn_rate=0.4),
        Station("S02", "Central", 2.5, spawn_rate=1.2),
        Station("S03", "Terminal Sur", 5.0, spawn_rate=0.3)
    ]

    for station in stations:
        line.add_station(station)

    stations[0].add_passengers(250)
    stations[1].add_passengers(400)

    # Tren 1 (M-001) - Sale de inmediato
    train1 = Train("M-001", max_speed=60)
    train1.current_station = stations[0]
    train1.position = stations[0].position
    train1.state = TrainState.EN_ESTACION
    line.add_train(train1)

    # Tren 2 (M-002) - Sale en t=40s
    train2 = Train("M-002", max_speed=70)
    train2.current_station = stations[0]
    train2.position = stations[0].position
    train2.state = TrainState.DETENIDO
    line.add_train(train2)

    # Motor de simulación con despacho automático
    simulation = ScheduledSimulation(train2_ref=train2)
    simulation.add_line(line)

    app = QApplication(sys.argv)
    window = MainWindow(simulation)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()