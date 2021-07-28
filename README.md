# GEE
Google Earth Engine(GEE) for Python
# 1.Module
建立library函数库,直接调用函数批量进行GEE数据处理

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

