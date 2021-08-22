# 1.矢量和栅格数据的上传和下载

## 1.1 从本地导入栅格和矢量数据到GEE_Python


```python
#导入gee相关库
import ee
import geemap
import os
```


```python
#设置端口，7890为电脑端口
geemap.set_proxy(port=7890)
```


```python
#生成底图
Map = geemap.Map()
Map
```


### 1.1.1 本地导入栅格(windows暂不支持导入raster)

### 1.1.2 本地导入矢量(windows暂不支持导入raster)


```python
shp_path=('K:/编程学习视频/GEE培训/GEE_python_RC/data/20210416.shp')
shp_local = geemap.shp_to_ee(shp_path)
```


```python
Map.centerObject(shp_local)
Map.addLayer(shp_local)
Map
```



## 1.2 从GEE导入栅格和矢量

### 1.2.1 导入栅格


```python
shp_GEE = ee.FeatureCollection("users/rc474048903/qishan2021_wheat_rust/qishan20210416_wheatrust_point")
```

### 1.2.2 导入矢量


```python
raster_GEE = ee.Image("users/rc474048903/qishan2021_wheat_rust/qishan_wheatarea_decisiontree")
```

## 1.3 从GEE_Python导出矢量和栅格到GEE DRIVE

### 1.3.1 利用ee库函数导出矢量


```python
#创建上传任务
task_shp= ee.batch.Export.table.toDrive(collection= shp_GEE, 
                                        description = "shp_GEE",
                                        folder= "GEE_python",
                                        fileNamePrefix= "shp_GEE",
                                        fileFormat=  "SHP")
```


```python
#开始上传
task_shp.start()
```


```python
#查看上传状态
task_shp.status()
```

### 1.3.2 利用ee库函数导出栅格


```python
China_country = ee.FeatureCollection("users/rc474048903/region_boundry/china2019_xianji")
roi = China_country.filterMetadata('NAME', 'equals', '岐山县')
#创建上传任务
task_raster=ee.batch.Export.image.toDrive(image= raster_GEE, 
                                          description= "raster_GEE",
                                          folder= "GEE_python",
                                          region= roi.geometry(),
                                          scale= 10,crs= "EPSG:4326",
                                          maxPixels= 1e13)
```


```python
#开始上传
task_raster.start()
```


```python
#查看上传状态
task_raster.status()
```

### 1.3.3 利用geemap函数导出矢量


```python
geemap.ee_export_vector_to_drive(ee_object =shp_GEE, description= "shp_GEE", folder="GEE_python", file_format='shp')
```

### 1.3.4 利用geemap函数导出栅格


```python
geemap.ee_export_image_to_drive(ee_object=raster_GEE, description="raster_GEE", folder="GEE_python",
                                region=roi.geometry(), scale=10, crs="EPSG:4326", 
                                max_pixels=1e13, file_format='GeoTIFF')
```

## 1.4 从GEE_Python导出矢量和栅格到本地

### 1.4.1 利用ee库函数导出栅格


```python
geemap.ee_export_image(ee_object=raster_GEE, filename='K:/编程学习视频/GEE培训/GEE_python_RC/raster_GEE.tif', 
                       scale=10, crs="EPSG:4326", region=roi.geometry(), file_per_band=False)
```

### 1.4.2 利用ee库函数导出矢量


```python
#方法1
geemap.ee_export_vector(ee_object=shp_GEE, filename='K:/编程学习视频/GEE培训/GEE_python_RC/shp_GEE.shp')
```


```python
#方法2
geemap.ee_to_shp(ee_object=shp_GEE, filename='K:/编程学习视频/GEE培训/GEE_python_RC/shp_GEE.shp')
```
