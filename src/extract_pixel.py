import subprocess
import os
import glob

def extract_pixel_from_geotiff(geotiff_path, lon, lat):
    """
    Extracts the pixel value from a GeoTIFF file at a specified geographic coordinate.

    Parameters:
        geotiff_path (str): Path to the GeoTIFF file.
        lon (float): Longitude of the target location.
        lat (float): Latitude of the target location.

    Returns:
        float: The pixel value at the given coordinate.
        None: If the extraction fails or the coordinate is outside the data range.
    """
    try:
        # Step 1: Check if the GeoTIFF file exists
        if not os.path.isfile(geotiff_path):
            print(f"GeoTIFF file not found: {geotiff_path}")
            return None

        # Step 2: Extract pixel value using gdallocationinfo
        print(f"Extracting pixel value from GeoTIFF: {geotiff_path}")
        gdallocationinfo_cmd = [
            "gdallocationinfo",
            "-valonly",
            "-geoloc",
            geotiff_path,
            str(lon),
            str(lat)
        ]
        result = subprocess.run(gdallocationinfo_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error in gdallocationinfo for file {geotiff_path}: {result.stderr.strip()}")
            return None

        # Parse the pixel value
        value = result.stdout.strip()
        if value in ("65535.0", "65534.0"):  # NoData values
            print(f"NoData value found at ({lon}, {lat}) in {geotiff_path}")
            return None
        return float(value) if value else None

    except Exception as e:
        print(f"Exception occurred while processing {geotiff_path}: {e}")
        return None


# Main script
# Path to the directory containing GeoTIFF files
input_dir = "/home/hirama/Downloads/Glob_Env_Metrology-main/assignment/LAI_tiff/2023/0811/"
longitude = 116.2542  # Longitude of the target location
latitude = -32.5983   # Latitude of the target location

# Collect all GeoTIFF files in the input directory
geotiff_files = glob.glob(os.path.join(input_dir, "*.tif"))

for geotiff_file in geotiff_files:
    try:
        # Extract the pixel value from the GeoTIFF
        value = extract_pixel_from_geotiff(geotiff_file, longitude, latitude)
        if value is not None:
            print(f"The pixel value at ({longitude}, {latitude}) in {geotiff_file} is {value}")
        else:
            print(f"No valid data found at ({longitude}, {latitude}) in {geotiff_file}")
    except Exception as e:
        print(f"Skipping file: {geotiff_file}. Error: {e}")
