![og_image](https://github.com/user-attachments/assets/39f51c33-271c-4e4a-ac7f-3c2c98a4bd70)

# SGLI LAI Process Tool

以下のことができます．
1. 事前に設定した緯度経度情報から，適切なタイルのGCOM-C SGLI L2プロダクトのHDF5ファイル(LAI)を取得
2. hdf5ファイルをgeotiff(EPSG:4326)に変換．<= 30 arc-sec(1km解像度)にBicubic法でリサンプリング
3. 指定した緯度経度の時系列データを作成(total, over-story, under-story)


# Environment
- Rocky Linux 8.8 (Green Obsidian)
- python 3.6.8
- h5py 3.1.0
- numpy 1.19.5
- gdal 3.0.4


# Configuration
```
SGLI
├── siteinfo
│   └── tile_data.csv
└── src
    ├── create_understory_LAI.py
    ├── extract_pixel.py
    ├── extract_pixel_over.py
    ├── gen_new_sitedata.py
    ├── h5_2_tiff.py
    ├── initialize.py
    ├── multi_process_LAI.sh
    ├── multi_process_LAI_over.sh
    ├── sglicod.py
    ├── site_tilelist.py
    └── tile_calculator.py
```

## tile_data.csv  
site_tilelist.pyで作成されるcsvです．gen_new_sitedata.py内の`load_sitedata`に記述されているデータをもとに，タイル番号を計算しています．

## create_understory_LAI.py  
total, overのLAIデータから下層植生のLAIの時系列データを作成します．使用する場合は対象とする年を自分で設定する必要があります．

## extract_pixel.py  
tile_data.csvの情報をもとにtotal LAIの時系列データを作成します．

## extract_pixel_over.py  
tile_data.csvの情報をもとにover-story LAIの時系列データを作成します．

## gen_new_sitedata.py
sitedataの初期化に使用します．処理をいろいろ行っていますが，ほかのプロジェクトで使用しているものですので，使用，変更は不要です．`load_sitedata()`の設定にのみ使用します．

## h5_2_tiff.py
[TTY6335様のスクリプト](https://github.com/TTY6335/SGLI_L2)を一部改変し作成させていただきました．処理については[こちら](https://tty6335.hatenablog.com/entry/2020/12/26/222429)

## multi_process_LAI.sh
total LAIを作成する際のメインスクリプトです．Working directoryおよび入手したいデータの期間を入力し，使用します．
> [!CAUTION]
> JAXA G-portalからデータを取得するため，メンテナンス中はデータダウンロードに失敗します．
> データダウンロードに失敗した場合はG-portalの状況を確認してください．

## multi_process_LAI_over.sh
over-story LAIを作成する際のメインスクリプトです．Working directoryおよび入手したいデータの期間を入力し，使用します．
multi_process_LAIと同様にG-potalの状況を確認し，使用してください．

## sglicod.py
タイル番号の計算に使用しているスクリプトです．

## site_tilelist.py
tile_data.csvの作成に使用するスクリプトです．

## tile_calculator.py
データダウンロードの際に必要になる，重複のないタイル番号のリストを作成する際に使用されるスクリプトです．

<br>

# Usage
1. gen_new_sitedata.py内の`load_sitedata()`のサイト情報を任意のものに変更．
2. site_tilelist.pyを実行
3. multi_process_LAI.sh もしくは multi_process_LAI_overのWorking directory，期間などの`Parameters`を適切に変更．
4. multi_process_LAI.sh もしくは multi_process_LAI_overを実行．前者はtotal, 後者はover-storyのLAIを取得する．
> [!CAUTION]
> 同じディレクトリにダウンロードする仕様となっているため，同時に動かすとうまくいかない可能性があります．対象のディレクトリを変更するか順番に実行してください．
> なお，デフォルトではファイルが存在している場合処理をスキップするので，二度目は比較的早く処理が終わります．
5. 必要であればcreate_understory_LAI.pyを実行し，下層植生のLAIを作成する．なお，スクリプト内で対象とする年を自分で設定する必要がある．

# その他
- 重大なエラー，修正点等ありましたら，お気軽にPRしてください！　できる限り改善します！
