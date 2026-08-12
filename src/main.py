from core.station import Station
from core.train import Train
from core.line import Line
from core.simulation import Simulation


def main():

    # Línea
    line = Line(
        line_id="L1",
        name="Línea de Prueba"
    )

    # Estaciones
    stations = [
        Station("S01", "Terminal Norte", 0.0),
        Station("S02", "Central", 2.5)
    ]

    for station in stations:
        line.add_station(station)

    # Tren
    train = Train(
        train_id="M-001",
        capacity=1200,
        max_speed=60
    )

    train.current_station = stations[0]
    train.next_station = stations[1]

    line.add_train(train)

    # Simulación
    simulation = Simulation()
    simulation.add_line(line)

    print("=== METROSIM ===")
    print()
    print("Ruta:")
    print("S01 Terminal Norte")
    print("       ↓")
    print("       ↓ 2.5 km")
    print("       ↓")
    print("S02 Central")
    print()

    # Simulación
    for _ in range(300):

        simulation.update()

        print(
            f"Tiempo: "
            f"{simulation.current_time:.0f}s | "
            f"{train}"
        )

        if train.state == "EN ESTACIÓN":
            print()
            print("¡El tren llegó a S02!")
            break


if __name__ == "__main__":
    main()