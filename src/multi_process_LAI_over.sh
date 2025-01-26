#!/bin/bash

# Parameters
WD="/data01/people/hirama/LAI/SGLI"              # Working directory
YEAR="2022"                                      # Year (e.g., 2023 or 2024)
START_MONTH="01"                                 # Start month (e.g., 05)
START_DAY="01"                                   # Start day (e.g., 10)
END_MONTH="12"                                   # End month (e.g., 05)
END_DAY="31"                                     # End day (e.g., 15)

# Get tile information using Python script
TILES=$(python3 tile_calculator.py)

# Convert dates to a format that `date` can process
START_DATE="${YEAR}-${START_MONTH}-${START_DAY}"
END_DATE="${YEAR}-${END_MONTH}-${END_DAY}"

# Loop over each day in the range
current_date="$START_DATE"
while [[ "$current_date" < "$END_DATE" ]] || [[ "$current_date" == "$END_DATE" ]]; do
    # Extract the current month and day
    MONTH=$(date -d "$current_date" +%m)
    DAY=$(date -d "$current_date" +%d)

    # Loop over each tile (V, H) pair
    echo "$TILES" | while read -r V H; do
        # Log processing information
        echo "Processing date: $current_date, Tile: V=$V, H=$H"

        # Construct URL and file paths
        FILE_NAME="GC1SG1_${YEAR}${MONTH}${DAY}D01D_T${V}${H}_L2SG_LAI_Q_3000.h5"
        URL="https://repo.gportal.jaxa.jp/standard/GCOM-C/GCOM-C.SGLI/L2.LAND.LAI_/3/${YEAR}/${MONTH}/${DAY}/${FILE_NAME}"
        SAVE_DIR="${WD}/hdf5/${YEAR}/${MONTH}${DAY}/"
        SAVE_PATH="${SAVE_DIR}${FILE_NAME}"

        # Create Geotiff directory
        GEOTIFF_DIR="${WD}/Geotiff/over/${YEAR}/${MONTH}${DAY}/"
        mkdir -p "$GEOTIFF_DIR"

        # Define output GeoTIFF file path
        OUTPUT_TIFF="${GEOTIFF_DIR}${FILE_NAME%.h5}_over.tif"

        # Check if the GeoTIFF file already exists
        if [[ -f "$OUTPUT_TIFF" ]]; then
            echo "GeoTIFF already exists: $OUTPUT_TIFF. Skipping."
            continue
        fi

        # Check if the HDF5 file already exists
        if [[ ! -f "$SAVE_PATH" ]]; then
            echo "File does not exist locally. Downloading: $FILE_NAME"
            mkdir -p "$SAVE_DIR"
            wget "$URL" -P "$SAVE_DIR" --quiet

            # Check if the download was successful
            if [[ $? -ne 0 ]]; then
                echo "Error: Failed to download $FILE_NAME from $URL"
                continue
            fi
            echo "Download completed: $SAVE_PATH"
        else
            echo "File already exists: $SAVE_PATH"
        fi

        # Convert HDF5 to GeoTIFF using Python script
        echo "Converting $SAVE_PATH to GeoTIFF..."
        python3 h5_2_tiff.py "$SAVE_PATH" "Overstory_LAI" "$OUTPUT_TIFF"

        if [[ $? -eq 0 ]]; then
            echo "GeoTIFF created: $OUTPUT_TIFF"
        else
            echo "Error: Failed to convert $SAVE_PATH to GeoTIFF."
        fi
    done

    # Move to the next day
    current_date=$(date -d "$current_date + 1 day" +%Y-%m-%d)
done


python3 extract_pixel_over.py $WD $YEAR
