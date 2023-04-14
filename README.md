# GEE_Python
Google Earth Engine(GEE) for Python

# 0.GEE.Environment

在python中配置GEE

方法1.安装官方库ee

方法2.安装geemap（推荐）

# 1.Module
建立自己的library函数库,直接调用函数批量进行GEE数据处理

method：
导入Module
```python
from RC_module import general
general.函数名
```

```python
funoutline(roi)#在geemap.Map()中显示roi边界
```

```python
funIDW(shp,property,range)#利用ee库进行IDW反距离权重插值
```

```python
S2Cloud(image)#利用ee库调用Sentinel-2数据
```

```python
S2Img(startdate, enddate,geometry,cloud)#获取Sentinel2影像数据
```

```python
S2Vis(img)#计算指数并且添加为对应波段
```

# 2.Upload and download
矢量和栅格数据的上传（本地上传到Python中进行数据处理）和下载（下载到本地和Google Drive）

# 3.Batch_Vis_loadimg
批量计算本地栅格数据的植被指数

# 4.Cropstation_tocsv_toshp
农气站点TXT文件批量转shp

# 5.WeatherStation.txt_ToCsv_ToShp_ByDay
中国地面气候资料日值数据集(V3.0).txt转成矢量数据.shp

# 6.VIs_mean&std_bar_err
绘制不同类别植被指数均值标准差直方图

# 7.Define function&derivatives&picture
定义函数及其导数，绘制双Y轴曲线
