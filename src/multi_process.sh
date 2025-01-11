#!/bin/bash

# Parameters
WD="/home/hirama/Downloads/Glob_Env_Metrology-main/assignment/"          # Working directory
YEAR="2023"                                      # Year (e.g., 2023 or 2024)
START_MONTH="05"                                 # Start month (e.g., 05)
START_DAY="10"                                   # Start day (e.g., 10)
END_MONTH="05"                                   # End month (e.g., 05)
END_DAY="15"                                     # End day (e.g., 15)

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
        FILE_NAME="GC1SG1_${YEAR}${MONTH}${DAY}D01D_T${V}${H}_L2SG_RSRFQ_3002.h5"
        URL="https://repo.gportal.jaxa.jp/standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/${YEAR}/${MONTH}/${DAY}/${FILE_NAME}"
        SAVE_DIR="${WD}/data/${YEAR}/${MONTH}${DAY}/"
        SAVE_PATH="${SAVE_DIR}${FILE_NAME}"

        # Check if the file already exists
        if [[ -f "$SAVE_PATH" ]]; then
            echo "File already exists: $SAVE_PATH. Skipping download."
            continue
        fi

        # Create the directory if it doesn't exist
        mkdir -p "$SAVE_DIR"

        # Download the file using wget
        echo "Downloading $FILE_NAME from $URL..."
        wget "$URL" -P "$SAVE_DIR" --quiet

        # Check if the download was successful
        if [[ $? -eq 0 ]]; then
            echo "Download completed: ${SAVE_PATH}"
        else
            echo "Error: Failed to download $FILE_NAME from $URL"
        fi
    done

    # Move to the next day
    current_date=$(date -d "$current_date + 1 day" +%Y-%m-%d)
done
