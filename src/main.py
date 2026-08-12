from core.station import Station
from core.train import Train, TrainState
from core.line import Line
from core.simulation import Simulation


def main():
    line = Line("L1", "Línea de Prueba")

    stations = [
        Station("S01", "Terminal Norte", 0.0, spawn_rate=0.5),
        Station("S02", "Central", 2.5, spawn_rate=1.0),
        Station("S03", "Terminal Sur", 5.0, spawn_rate=0.2)
    ]

    for station in stations:
        line.add_station(station)

    # Tren 1 (M-001)
    train1 = Train("M-001", max_speed=60)
    train1.current_station = stations[0]
    train1.position = stations[0].position
    train1.state = TrainState.EN_ESTACION
    line.add_train(train1)

    # Tren 2 (M-002) - Inicia en S01 detenido
    train2 = Train("M-002", max_speed=70)
    train2.current_station = stations[0]
    train2.position = stations[0].position
    train2.state = TrainState.DETENIDO
    line.add_train(train2)

    simulation = Simulation()
    simulation.add_line(line)

    for tick in range(600):
        # A los 30 segundos despachamos a M-002 desde S01
        if tick == 30:
            train2.state = TrainState.EN_ESTACION

        simulation.update()

        print(f"Tiempo: {simulation.current_time:.0f}s | {train1}")
        print(f"Tiempo: {simulation.current_time:.0f}s | {train2}")
        print("-" * 80)


if __name__ == "__main__":
    main()