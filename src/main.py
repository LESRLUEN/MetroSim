from core.station import Station
from core.train import Train
from core.line import Line


def main():

    # Crear línea
    line = Line(
        line_id="L1",
        name="Línea de Prueba"
    )

    # Crear estaciones
    stations = [
        Station("S01", "Terminal Norte", 0.0),
        Station("S02", "Central", 2.5),
        Station("S03", "Reforma", 4.8),
        Station("S04", "Centro", 7.2),
        Station("S05", "Universidad", 9.6),
        Station("S06", "Sur", 12.1),
        Station("S07", "Aeropuerto", 14.7),
        Station("S08", "Terminal Sur", 17.5)
    ]

    # Agregar estaciones a la línea
    for station in stations:
        line.add_station(station)

    # Crear tren
    train = Train(
        train_id="M-001",
        capacity=1200,
        max_speed=60
    )

    # Agregar tren a la línea
    line.add_train(train)

    # Mostrar información
    print("=== METROSIM ===")
    print()
    print(line)

    print()
    print("ESTACIONES:")

    for station in line.stations:
        print(station)

    print()
    print("TRENES:")

    for train in line.trains:
        print(train)


if __name__ == "__main__":
    main()