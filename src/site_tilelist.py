import math
import sglicod as sgli
import gen_new_sitedata as gen_ns
import csv
import os


def generate_tile_data(num_pix, site_list, lat_list, lon_list):
    tile_data = []
    for site, lat, lon in zip(site_list, lat_list, lon_list):
        V, H, _, _ = sgli.sgli_ll2tile_B0(num_pix, float(lon), float(lat))
        tile_data.append({
            "site_name": site,
            "latitude": float(lat),
            "longitude": float(lon),
            "V": V,
            "H": H
        })
    return tile_data


if __name__ == '__main__':
    site, lat, lon = gen_ns.load_sitedata()
    num_pix = 4800
    tile_data = generate_tile_data(num_pix, site, lat, lon)
    
    os.makedirs("../siteinfo",exist_ok=True)
    output_file = "../siteinfo/tile_data.csv"
    with open(output_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["site_name", "latitude", "longitude", "V", "H"])
        writer.writeheader()
        writer.writerows(tile_data)

    print(f"タイルデータを {output_file} に保存しました。")
