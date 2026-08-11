from core.station import Station


def main():
    station = Station(
        station_id="S01",
        name="Terminal Norte",
        position=0.0
    )

    station.add_passengers(250)

    print("=== METROSIM ===")
    print(station)

    boarded = station.remove_passengers(80)

    print()
    print(f"Pasajeros que abordaron: {boarded}")
    print(station)


if __name__ == "__main__":
    main()