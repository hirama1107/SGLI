# This program?
以下のことをしてくれます．
1. 事前に設定したLAI観測サイトの緯度経度情報から，適切なタイルのGCOM-C SGLIのLevel2プロダクトのHDF5ファイル(LAI)を取得
2. hdf5ファイルgeotiffに変換
3. EPSG:4326(WGS84)に変換
4. 1km解像度にBicubicでリサンプリング
5. 観測サイトに該当するピクセルの時系列データを作成

# Environment
- Rocky Linux 8.8 (Green Obsidian)
- python 3.6.8
- h5py 3.1.0
- numpy 1.19.5
- gdal 3.0.4

# Usage
