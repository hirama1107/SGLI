import os
import pandas as pd

def fill_missing_dates(df, start_date, end_date):
    all_dates = pd.date_range(start=start_date, end=end_date)
    df = df.set_index("date").reindex(all_dates).reset_index()
    df.columns = ["date" if col == "index" else col for col in df.columns]
    if "value" not in df.columns:
        df["value"] = pd.NA
    return df

def subtract_csv_files(total_dir, over_dir, under_dir, year):
    os.makedirs(under_dir, exist_ok=True)

    total_files = [f for f in os.listdir(total_dir) if f.endswith("_timeseries.csv")]

    for file_name in total_files:
        total_file_path = os.path.join(total_dir, file_name)
        over_file_path = os.path.join(over_dir, file_name)
        under_file_path = os.path.join(under_dir, file_name)

        if not os.path.exists(over_file_path):
            continue

        total_df = pd.read_csv(total_file_path)
        over_df = pd.read_csv(over_file_path)

        if "date" in total_df.columns and "value" in total_df.columns and "date" in over_df.columns and "value" in over_df.columns:
            total_df["date"] = pd.to_datetime(total_df["date"], format='%Y%m%d', errors="coerce")
            over_df["date"] = pd.to_datetime(over_df["date"], format='%Y%m%d', errors="coerce")

            total_df = total_df.dropna(subset=["date"])
            over_df = over_df.dropna(subset=["date"])

            start_date = pd.Timestamp(year=year, month=1, day=1)
            end_date = pd.Timestamp(year=year, month=12, day=31)

            total_df = fill_missing_dates(total_df, start_date, end_date)
            over_df = fill_missing_dates(over_df, start_date, end_date)

            result_df = total_df.copy()
            result_df["value_total"] = total_df["value"]
            result_df["value_over"] = over_df["value"]

            result_df["value"] = result_df.apply(
                lambda row: row["value_total"] - row["value_over"] if pd.notna(row["value_total"]) and pd.notna(row["value_over"]) else pd.NA,
                axis=1
            )

            result_df = result_df[["date", "value"]]

            result_df.to_csv(under_file_path, index=False)

if __name__ == "__main__":
    for year in range(2019, 2024):
        #year = 2018
        total_dir = f"../output/total/{year}/"
        over_dir = f"../output/over/{year}/"
        under_dir = f"../output/under/{year}/"

        subtract_csv_files(total_dir, over_dir, under_dir, year)
