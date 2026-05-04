import pandas as pd
import os

GTFS_DIR = "data/gtfs"

def load_and_merge():
    print("Loading GTFS files...")

    stop_times = pd.read_csv(os.path.join(GTFS_DIR, "stop_times.txt"))
    trips = pd.read_csv(os.path.join(GTFS_DIR, "trips.txt"))
    routes = pd.read_csv(os.path.join(GTFS_DIR, "routes.txt"))
    stops = pd.read_csv(os.path.join(GTFS_DIR, "stops.txt"))

    stop_times["stop_id"] = stop_times["stop_id"].astype(str)
    stops["stop_id"] = stops["stop_id"].astype(str)

    # Merge everything into one flat table
    df = stop_times.merge(trips, on="trip_id")
    df = df.merge(routes, on="route_id")
    df = df.merge(stops, on="stop_id")

    # Keep only the columns we need
    df = df[["route_short_name", "route_long_name",
             "trip_id", "stop_id", "stop_name",
             "arrival_time", "departure_time",
             "stop_sequence"]]

    # Parse times (GTFS uses HH:MM:SS but can exceed 24:00:00 for overnight)
    def parse_gtfs_time(t):
        try:
            parts = str(t).split(":")
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            return h * 3600 + m * 60 + s  # convert to seconds from midnight
        except:
            return None

    df["arrival_sec"] = df["arrival_time"].apply(parse_gtfs_time)
    df["departure_sec"] = df["departure_time"].apply(parse_gtfs_time)
    df.dropna(subset=["arrival_sec", "departure_sec"], inplace=True)

    print(f"Merged dataset: {len(df):,} rows")
    df.to_csv("data/cleaned.csv", index=False)
    print("Saved to data/cleaned.csv")
    return df

if __name__ == "__main__":
    load_and_merge()