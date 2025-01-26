import math
import sglicod as sgli
import gen_new_sitedata as gen_ns



def calculate_unique_tiles(num_pix, lat_list, lon_list):
    vh_set = set()
    for lat, lon in zip(lat_list, lon_list):
        V, H, _, _ = sgli.sgli_ll2tile_B0(num_pix, float(lon), float(lat))
        vh_set.add((V, H))

    return list(vh_set)

if __name__ == '__main__':

    site, lat, lon = gen_ns.load_sitedata()

    num_pix = 4800

    # 重複のないタイル番号 (V, H) のリストを生成
    unique_tiles = calculate_unique_tiles(num_pix, lat, lon)

    # 結果を表示
    print("Unique tiles (V, H):")
    for vh in unique_tiles:
        print(f"{vh[0]:02d} {vh[1]:02d}")
