import requests
import zipfile
import os
DATA_DIR = "data"
GTFS_URL = "https://gtfsrt.api.translink.com.au/GTFS/SEQ_GTFS.zip"

def download_gtfs():
    print("Downloading Brisbane GTFS data....")
    os.makedirs(os.path.join(DATA_DIR,"gtfs"), exist_ok=True )
    response = requests.get(GTFS_URL,timeout=60)
    zip_path = os.path.join(DATA_DIR, "SEQ_GTFS.zip")
    with open(zip_path, "wb") as f:f.write(response.content)
    print(f"saved to {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(os.path.join(DATA_DIR, "gtfs"))
        print("Extracted gtfs files.")

if __name__ == "__main__":
            download_gtfs()

