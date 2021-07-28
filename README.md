# GEE
Google Earth Engine(GEE) for Python
# 1.Module
# 1.常规数据处理
建立library函数库,直接调用函数批量进行GEE数据处理
method：#直接运行模块里的函数
        from RC_module import general
        general.函数名
## 1.1显示矢量边界
在geemap.Map()中显示roi边界
```python
funoutline(roi)
```
## 1.2植被指数计算

## 1.3IDW反距离权重插值
利用ee库进行插值
```python
funIDW(shp,property,range)
```

# 2.Sentinel-2数据处理
利用ee库调用Sentinel-2数据
## 2.1Sentinel去云
```python
S2Cloud(image)
```
## 2.2获取Sentinel2影像数据
```python
S2Img(startdate, enddate,geometry,cloud)
```
## 2.3计算指数并且添加为对应波段
```python
S2Vis(img)
```
# 2.Upload and download
矢量和栅格数据的上传（本地上传到Python中进行数据处理）和下载（下载到本地和Google Drive）

