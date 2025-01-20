from datetime import datetime
import json
from pathlib import Path
from time import sleep
import urllib
from tqdm import tqdm

def collect_data(num_samples:int, delta:int, out_path:str|Path):
    """
    Collects `num_samples` data for every `delta` and writes it to `out_path`
    """

    with open("keys.json", 'r') as f:
        um_waw_api = json.load(f)['um_waw_api']
    um_waw_url = "https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey="
    url = um_waw_url + um_waw_api + "&type=2"

    with open(out_path + f"data_{datetime.now().strftime("%d%m%Y_%H")}.csv", 'w') as f:
        f.write("VehicleNumber,Lines,Lat,Lon,Time\n")
        for _ in tqdm(range(num_samples)):
            response = urllib.request.urlopen(url)
            result = json.loads(response.read())['result']
            for frame in result:
                time = datetime.strptime(frame['Time'], "%Y-%m-%d %H:%M:%S")
                if datetime.now() - time > timedelta(minutes=2):
                    continue
                num = frame['VehicleNumber']
                lat = float(frame['Lat'])
                lon = float(frame['Lon'])
                line = frame['Lines']
                f.write(f"{num},{line},{lat},{lon},{time}\n")

            sleep(delta)
    print("Done collecting data")


from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def get_random_vehicle_line_data(line:int, file_path:str):
    df = pd.read_csv(file_path)
    df = df[df.Lines == line]
    df.Time = df.Time.apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    df = df[df['VehicleNumber'] == np.random.choice(np.unique(df['VehicleNumber']))]
    df.sort_values('Time', inplace=True)
    
    lats = list(df.Lat)
    lons = list(df.Lon)
    times = list(df.Time)
    return (lats, lons, times)