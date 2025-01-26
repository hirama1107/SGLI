import os
import sys
import csv
from datetime import datetime
import subprocess


def extract_pixel_from_geotiff(geotiff_path, lon, lat):
    try:
        if not os.path.isfile(geotiff_path):
            return None
        result = subprocess.run(
            ["gdallocationinfo", "-valonly", "-geoloc", geotiff_path, str(lon), str(lat)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True 
        )
        if result.returncode != 0:
            print(f"Error in gdallocationinfo: {result.stderr.strip()}")
            return None
        value = result.stdout.strip()
        if value in ("65535.0", "65534.0"):
            return None
        return float(value) if value else None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python extract_pixel.py <working_directory>")
        sys.exit(1)

    wd = sys.argv[1]
    year = sys.argv[2]
    siteinfo_csv = "../siteinfo/tile_data.csv"
    output_dir = os.path.join(wd, "output", "over", year)
    os.makedirs(output_dir, exist_ok=True)
    wd = os.path.join(wd, "Geotiff", "over")

    site_data = {}

    with open(siteinfo_csv, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            site_name = row["site_name"]
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])
            V = int(row["V"])
            H = int(row["H"])
            if site_name not in site_data:
                site_data[site_name] = {"entries": [], "latitude": latitude, "longitude": longitude, "V": V, "H": H}

    for year in os.listdir(wd):
        if year != sys.argv[2]:
            continue
        year_dir = os.path.join(wd, year)
        if not os.path.isdir(year_dir) or not year.isdigit():
            continue

        for mmdd in os.listdir(year_dir):
            subdir = os.path.join(year_dir, mmdd)
            if not os.path.isdir(subdir) or not mmdd.isdigit():
                continue

            date_str = f"{year}{mmdd}"
            try:
                datetime.strptime(date_str, "%Y%m%d")
            except ValueError:
                continue

            for site_name, data in site_data.items():
                latitude, longitude, V, H = (
                    data["latitude"],
                    data["longitude"],
                    data["V"],
                    data["H"]
                )

                input_f = f"GC1SG1_{date_str}D01D_T{V:02d}{H:02d}_L2SG_LAI_Q_3000_over.tif"
                target_f = os.path.join(subdir, input_f)

                if not os.path.exists(target_f):
                    print(f"File not found: {target_f}")
                    continue

                print(f"Processing file: {target_f} for site: {site_name} at ({latitude}, {longitude})")

                try:
                    value = extract_pixel_from_geotiff(target_f, longitude, latitude)
                    if value is None:
                        print(f"No valid value found for site {site_name} at ({latitude}, {longitude}) in {target_f}")
                        continue
                    data["entries"].append({"date": date_str, "value": value})
                    print(f"Extracted value: {value} for site: {site_name} on {date_str}")
                except Exception as e:
                    print(f"Error extracting value for site {site_name} from {target_f}: {e}")

    for site_name, data in site_data.items():
        output_file = os.path.join(output_dir, f"{site_name}_timeseries.csv")
        with open(output_file, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "value"])
            writer.writeheader()
            writer.writerows(data["entries"])

        print(f"Saved timeseries data for site: {site_name} to {output_file}")
