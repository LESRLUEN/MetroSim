from src.core.station import Station
from src.core.train import Train, TrainState
from src.core.line import Line
from src.core.simulation import Simulation
from src.core.incident import Incident

def main():
    line = Line("L1", "Línea de Prueba")

    stations = [
        Station("S01", "Terminal Norte", 0.0, spawn_rate=0.5),
        Station("S02", "Central", 2.5, spawn_rate=1.0),
        Station("S03", "Terminal Sur", 5.0, spawn_rate=0.2)
    ]

    for station in stations:
        line.add_station(station)

    # Tren 1
    train1 = Train("M-001", max_speed=60)
    train1.current_station = stations[0]
    train1.position = stations[0].position
    train1.state = TrainState.EN_ESTACION
    line.add_train(train1)

    # Tren 2
    train2 = Train("M-002", max_speed=70)
    train2.current_station = stations[0]
    train2.position = stations[0].position
    train2.state = TrainState.DETENIDO
    line.add_train(train2)

    simulation = Simulation()
    simulation.add_line(line)

    # Crear incidencia: Palanca de emergencia accionada en M-001 por 40 segundos
    emergency_incident = Incident(
        incident_id="INC-01",
        description="Palanca de emergencia accionada por usuario",
        train=train1,
        duration=40,
        state=TrainState.EMERGENCIA
    )
    simulation.add_incident(emergency_incident)

    for tick in range(1, 400):
        if tick == 20:
            train2.state = TrainState.EN_ESTACION

        # Inyectar la incidencia en el segundo 120
        if tick == 120:
            emergency_incident.trigger()

        simulation.update()

        print(f"Tiempo: {simulation.current_time:.0f}s | {train1}")
        print(f"Tiempo: {simulation.current_time:.0f}s | {train2}")
        print("-" * 80)


if __name__ == "__main__":
    main()