import numpy as np
import h5py
import os
import rioxarray
import calendar
from multiprocessing import Pool, Array
from logging import getLogger, StreamHandler, DEBUG, Formatter
import gc

def set_logging():
    formatter = Formatter('[%(levelname)s] %(asctime)s - %(message)s (%(filename)s)')
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(formatter)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    return logger

logger = set_logging()

def load_sitedata():
    site = ['Australia_Camerons', 'Australia_Gnangara', 'China_Zhang_Bei', 'China_Honghe_A',\
        'China_Honghe_B', 'China_Honghe_C', 'China_Honghe_D', 'China_Honghe_E', \
        'China_Hailun_A', 'China_Hailun_B', 'China_Hailun_C', 'China_Hailun_D', \
        'China_Hailun_E', 'China_BJ_wheat_1', 'China_BJ_wheat_2', 'China_BJ_wheat_3', \
        'China_BJ_wheat_8', 'China_HN_wheat_2', 'China_HN_wheat_5', 'China_HN_wheat_6', \
        'China_HN_wheat_8', 'China_HN_wheat_14', 'China_HN_wheat_16', 'China_HLJ_barley_1', \
        'China_HLJ_barley_2', 'China_HLJ_barley_3', 'China_HLJ_barley_4', \
        'China_HLJ_barley_8', 'China_HLJ_barley_13', 'China_HLJ_barley_14', \
        'China_HLJ_barley_16', 'China_HLJ_barley_19', 'China_HLJ_wheat_1', \
        'China_HLJ_wheat_2', 'China_HLJ_wheat_3', 'China_HLJ_wheat_6', 'China_HLJ_wheat_8', \
        'China_HLJ_wheat_14', 'China_HLJ_wheat_15', 'China_HLJ_wheat_16', 'China_AH_wheat_1',\
        'China_AH_wheat_3', 'China_AH_wheat_5', 'China_AH_wheat_12', 'URY', 'TOS', 'TMM', \
        'WTR', 'MBN', 'DGT', 'KYM', 'TKY', 'FJY', 'FHK']
        # , 'RUHa2', 'RUHa1', 'RUHa3', 'SKT', 'KBU', 'LSH', 'TSE', \'MBF', 'MMF', 'SAP', 'TMK', , 'CBS', 'API', 'SMK', 'GDK', 'GCK', 'HBG', 'QHB', 'YCS', 'TKC','MSE','SMF', 'KEW', 'YMS', 'HFK', 'KHW', 'QYZ', 'CLM', 'BNS', 'MKL', 'SKR', 'IRI-NFL', 'IRI-FL', 'PSO', 'BKS', 'PUF', 'PDB', 'PDF', 'LHP']
    lat = ['-32.5983', '-31.5338', '41.2788', '47.667', '47.663', '47.653', '47.637', '47.637', '47.41', '47.405',\
           '47.401', '47.409', '47.429', '40.2273', '40.1718', '40.2046', '40.1729', '35.1403', '33.8126', '35.1162',\
           '34.9561', '33.7398', '33.7197', '46.8021', '46.7954', '46.7873', '46.7859', '46.7402', '46.7137', '46.7504',\
           '46.7253', '46.7012', '46.9679', '46.9621', '46.939', '46.8983', '46.7919', '46.7641', '46.7589', '46.7366',\
           '33.151', '33.116', '33.1', '33.087', '44.3996', '42.7082', '43.5614', '36.2658', '47.7981', '46.2489',\
           '47.6705', '36.146167', '35.4546', '35.443528']
           #, '54.77310181', '54.72529984', '54.7045517', '48.351861', '47.213972', '45.279839', '45.055833',\'44.386937', '44.333672', '42.9868', '42.734657', '42.4025', '40.0017', '37.93889', '37.75', '37.74853', '37.66',\'37.607432', '36.95','36.139722','36.069082',, '35.261663', '34.963611',\'34.7948', '34.55', '33.137', '26.7415', '24.590126', '21.95037', '14.589564', '14.492361', '14.144223', '14.14103',\'2.973213', '-0.861389', '-2.323614694', '-2.340796006', '-2.346070697', '4.201733'
    lon = ['116.2542', '115.8824', '114.6878', '133.515', '133.532', '133.523', '133.515', '133.534', '126.838', '126.838',\
           '126.805', '126.798', '126.801', '116.8109', '116.5722', '116.3577', '116.581', '113.0238', '114.6329', '112.9933',\
           '112.7627', '114.6906', '114.3753', '131.8055', '131.8955', '131.8865', '131.9766', '131.7591', '131.715', '131.8392',\
           '131.8995', '131.8671', '131.9728', '131.989', '131.9743', '131.9819', '131.9067', '131.7421', '131.8473', '131.7147',\
           '116.772', '116.804', '116.865', '116.899', '142.2033', '141.5553', '143.1557', '139.6831', '108.331', '106.4953',\
           '112.0764',  '137.423111','138.7623','138.764722']
            # '89.95670319', '90.00219727', '89.07785034', '108.654333', '108.737333', '127.578206', '142.107222',\'142.318583', '142.257729', '141.3853', '141.518326', '128.8333333', '140.9375', '126.95471', '127.15','127.16294',\'101.33', '101.332', '116.6', '137.370833', '140.022697', '137.07875',\'135.994444', '135.8462', '126.57', '130.7095', '115.0748','121.41106', '101.200047', '98.84388', '101.916306',\'121.262686', '121.265264','102.299827', '117.044722', '113.9043575', '114.0378994', '114.036408', '114.0293'
    return site, lat, lon


def load_data(file_path, dtype, shape, scale_factor=1, repeat_factor=1):
    try:
        data = np.memmap(file_path, dtype=dtype, mode='r').reshape(shape) / scale_factor
        if repeat_factor > 1:
            data = np.repeat(np.repeat(data, repeat_factor, axis=0), repeat_factor, axis=1)
        return data
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}")
        return None

def load_ahi_data(mon, d, h, m):
    infile_b3 = f'/data03/GEO/SRDATA/2018/{mon:02d}/{d:02d}/H08_2018{mon:02d}{d:02d}_{h:02d}{m:02d}_B03_SR.dat'
    infile_b4 = f'/data03/GEO/SRDATA/2018/{mon:02d}/{d:02d}/H08_2018{mon:02d}{d:02d}_{h:02d}{m:02d}_B04_SR.dat'
    infile_b5 = f'/data03/GEO/SRDATA/2018/{mon:02d}/{d:02d}/H08_2018{mon:02d}{d:02d}_{h:02d}{m:02d}_B05_SR.dat'
    infile_sz = f'/data01/GEO/INPUT/ANGLE/sun/Solar_Zenith_Angle_u2/AHI_SZA_2018{mon:02d}{d:02d}{h:02d}{m + 5:02d}.dat'
    infile_sa = f'/data01/GEO/INPUT/ANGLE/sun/Solar_Azimuth_Angle_u2/AHI_SAA_2018{mon:02d}{d:02d}{h:02d}{m + 5:02d}.dat'
    infile_cloud = f'/data01/GEO/AHI_CloudMask/2018{mon:02d}/AHIcm.v0.2018{mon:02d}{d:02d}{h:02d}{m:02d}.dat'
    infile_vaa = '/data01/GEO/INPUT/ANGLE/Viewer_Azimuth_Angle/AHI_VAA_10.dat'
    infile_vza = '/data01/GEO/INPUT/ANGLE/Viewer_Zenith_Angle/AHI_VZA_10.dat'

    ahi_b3 = load_data(infile_b3, np.int16, (12000, 12000), scale_factor=10000)
    ahi_b3[(ahi_b3 < 0) | (ahi_b3 > 1)] = np.nan
    ahi_b4 = load_data(infile_b4, np.int16, (12000, 12000), scale_factor=10000)
    ahi_b4[(ahi_b4 < 0) | (ahi_b4 > 1)] = np.nan
    ahi_b5 = load_data(infile_b5, np.int16, (6000, 6000), scale_factor=10000, repeat_factor=2)
    ahi_b5[(ahi_b5 < 0) | (ahi_b5 > 1)] = np.nan
    sz = load_data(infile_sz, np.uint16, (3000, 3000), scale_factor=100, repeat_factor=4)
    sa = load_data(infile_sa, np.uint16, (3000, 3000), scale_factor=100, repeat_factor=4)
    cloud = load_data(infile_cloud, np.float32, (6000, 6000), repeat_factor=2)
    va = load_data(infile_vaa, np.uint16, (12000, 12000), scale_factor=100)
    vz = load_data(infile_vza, np.uint16, (12000, 12000), scale_factor=100)
    
    return ahi_b3, ahi_b4, ahi_b5, sz, sa, cloud, va, vz

def load_ortho_data():
    lin = rioxarray.open_rasterio('/geoland02/share/people/liwei/Data/AHI_GEO_correction/ahi_grid_pixpos_0.010d_Lsurf-Ellip_lin.tif')
    col = rioxarray.open_rasterio('/geoland02/share/people/liwei/Data/AHI_GEO_correction/ahi_grid_pixpos_0.010d_Lsurf-Ellip_col.tif')
    lin_off = np.round(lin.values, 0).astype(int).reshape(12000, 12000)
    col_off = np.round(col.values, 0).astype(int).reshape(12000, 12000)
    return lin_off, col_off

def init_worker(shared_lin, shared_col):
    global lin_off, col_off
    lin_off = np.ctypeslib.as_array(shared_lin).reshape((12000, 12000))
    col_off = np.ctypeslib.as_array(shared_col).reshape((12000, 12000))

def extract_pixel(data_array, target_lat, target_lon):
    start_lon = 85
    end_lat = 60
    target_lon_pixel = int(np.round((target_lon - start_lon) / 0.01))
    target_lat_pixel = int(np.round((end_lat - target_lat) / 0.01))
    i_off, j_off = lin_off[target_lat_pixel, target_lon_pixel], col_off[target_lat_pixel, target_lon_pixel]
    row, col = target_lat_pixel + i_off, target_lon_pixel + j_off
    if 0 <= row < data_array.shape[0] and 0 <= col < data_array.shape[1]:
        return data_array[row, col]
    else:
        logger.warning(f"Out of bounds for pixel: row={row}, col={col}")
        return np.nan

def create_sitedata(args):
    sitename, lat, lon, wd = args
    logger.debug(f"Processing site: {sitename}")
    data = {
        "time": [],
        "b3": [],
        "b4": [],
        "b5": [],
        "sz": [],
        "sa": [],
        "cloud": [],
        "va": [],
        "vz": [],
        "ra": [],
    }
    for mon in range(1, 13):
        _, days_in_month = calendar.monthrange(2018, mon)
        for d in range(1, days_in_month + 1): #days_in_month + 1
            for h in range(0, 9):
                for m in range(0, 60, 10):
                    try:
                        ahi_b3, ahi_b4, ahi_b5, sz, sa, cloud, va, vz = load_ahi_data(mon, d, h, m)
                        if all(data is None for data in [ahi_b3, ahi_b4, ahi_b5, sz, sa, cloud, va, vz]):
                            logger.debug(f"Skipping processing for {mon:02d}/{d:02d} {h:02d}:{m:02d} as all data is None")
                            continue
                        data["time"].append(f"{mon:02d}{d:02d}{h:02d}{m:02d}")
                        data["b3"].append(extract_pixel(ahi_b3, lat, lon))
                        data["b4"].append(extract_pixel(ahi_b4, lat, lon))
                        data["b5"].append(extract_pixel(ahi_b5, lat, lon))
                        data["sz"].append(extract_pixel(sz, lat, lon))
                        data["sa"].append(extract_pixel(sa, lat, lon))
                        data["cloud"].append(extract_pixel(cloud, lat, lon))
                        data["va"].append(extract_pixel(va, lat, lon))
                        data["vz"].append(extract_pixel(vz, lat, lon))
                        data["ra"].append(abs(data["sa"][-1] - data["va"][-1]))
                        del ahi_b3, ahi_b4, ahi_b5, sz, sa, cloud, va, vz
                        gc.collect()
                    except Exception as e:
                        logger.error(f"Error processing {sitename}: {e}")
    with h5py.File(f'{wd}/{sitename}.h5', 'w') as hf:
        for key, values in data.items():    
            if key == "time":
                dt = h5py.special_dtype(vlen=bytes)  # Variable-length byte string
                hf.create_dataset(key, data=np.array(values, dtype=object), dtype=dt)
            else:
                hf.create_dataset(key, data=np.array(values))
    logger.debug(f"Completed site: {sitename}")

def view_hdf5_content_and_values(hdf5_file_path, preview_count=10):
    try:
        with h5py.File(hdf5_file_path, 'r') as hdf:
            print(f"HDF5 file: {hdf5_file_path}")
            print("-" * 60)
            # Recursive function to explore groups and datasets
            def explore_group(group, prefix=""):
                for key in group:
                    item = group[key]
                    if isinstance(item, h5py.Dataset):
                        print(f"{prefix}/{key} - Shape: {item.shape}, Dtype: {item.dtype}")
                        # Display dataset preview
                        data_preview = item[:preview_count] if item.size > preview_count else item[:]
                        print(f"    Preview: {data_preview}")
                    elif isinstance(item, h5py.Group):
                        print(f"{prefix}/{key}/ (Group)")
                        explore_group(item, prefix=f"{prefix}/{key}")
            # Start exploring from the root
            explore_group(hdf)
            print("-" * 60)
            print("Content exploration complete.")
    except FileNotFoundError:
        print(f"Error: File not found: {hdf5_file_path}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    wd = "/data01/people/hirama/LAI/ortho_ref_dat/data"
    os.makedirs(wd, exist_ok=True)
    site, lat, lon = load_sitedata()
    lin_off_data, col_off_data = load_ortho_data()
    shared_lin = Array('i', lin_off_data.flatten(), lock=False)
    shared_col = Array('i', col_off_data.flatten(), lock=False)
    args = [(site[i], float(lat[i]), float(lon[i]), wd) for i in range(len(site))]
    with Pool(processes=19, initializer=init_worker, initargs=(shared_lin, shared_col)) as pool:
        pool.map(create_sitedata, args)

if __name__ == '__main__':
    main()
    #view_hdf5_content_and_values("/data01/people/hirama/LAI/ortho_ref_dat/data1/Australia_Camerons.h5")
