import requests
import json

def download_tles():
    url = "https://celestrak.org/NORAD/elements/gps.txt"
    response = requests.get(url)
    lines = response.text.strip().split('\n')
    tle_data = []

    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i+1].strip()
        line2 = lines[i+2].strip()
        sat_id = line1.split()[1]
        tle_data.append({
            "name": name,
            "id": sat_id,
            "line1": line1,
            "line2": line2
        })

    with open("tle_data.json", "w") as f:
        json.dump(tle_data, f)
