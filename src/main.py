from core.station import Station
from core.train import Train
from core.train import Train, TrainState
from core.line import Line
from core.simulation import Simulation


def main():

    # Línea
    line = Line(
        line_id="L1",
        name="Línea de Prueba"
    )

    # Estaciones (agregamos S03 para probar la salida de S02)
    # Estaciones con afluencia dinámica (pasajeros/segundo)
    stations = [
        Station("S01", "Terminal Norte", 0.0, spawn_rate=0.2),  # 1 pas. cada 5 seg.
        Station("S02", "Central", 2.5, spawn_rate=1.5),  # 3 pas. cada 2 seg. (Estación de alto flujo)
        Station("S03", "Terminal Sur", 5.0, spawn_rate=0.1)  # 1 pas. cada 10 seg.
    ]



    for station in stations:
        line.add_station(station)

    # Tren
    train = Train(
        train_id="M-001",
        capacity=1200,
        max_speed=70
    )

    train.current_station = stations[0]
    train.position = stations[0].position
    train.state = TrainState.EN_ESTACION

    # Al agregar el tren, Line le asigna automáticamente train.line = line
    line.add_train(train)

    # Simulación
    simulation = Simulation()
    simulation.add_line(line)

    print("=== METROSIM ===")
    print()
    print("Ruta:")
    print("S01 Terminal Norte (0.0 km)")
    print("       ↓ 2.5 km")
    print("S02 Central (2.5 km)")
    print("       ↓ 2.5 km")
    print("S03 Terminal Sur (5.0 km)")
    print()

    # Ejecutamos 800 ticks para ver el trayecto completo S01 -> S02 -> S03
    for _ in range(800):

        simulation.update()

        print(
            f"Tiempo: {simulation.current_time:.0f}s | "
            f"{train}"
        )


if __name__ == "__main__":
    main()