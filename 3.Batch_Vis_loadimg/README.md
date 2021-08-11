# 1.批量计算本地遥感图像植被指数


```python
import os
from PIL import Image
import numpy as np
from osgeo import gdal
import glob
# import cv2
import math
```


```python
def BatchVis(in_path,out_path):
    list_tif = glob.glob(in_path+os.sep+"*.tif")#筛选符合条件的栅格数据
    out_path =out_path
    print(list_tif)
    for tif in list_tif:
        in_ds = gdal.Open(tif)
        # 获取文件所在路径以及不带后缀的文件名
        (filepath, fullname) = os.path.split(tif)
        (prename, suffix) = os.path.splitext(fullname)
        x_size = in_ds.RasterXSize  # 图像列数
        y_size = in_ds.RasterYSize  # 图像行数
        proj = in_ds.GetProjection()  # 返回的是WKT格式的字符串
        trans = in_ds.GetGeoTransform()  # 返回的是六个参数的tuple
        if in_ds is None:
            print('Could not open the file ' + tif)
        else:
            # 将原始数据类型转化为反射率
            blue = in_ds.GetRasterBand(1).ReadAsArray() * 0.0001
            green = in_ds.GetRasterBand(2).ReadAsArray() * 0.0001
            red = in_ds.GetRasterBand(3).ReadAsArray() * 0.0001
            re1 = in_ds.GetRasterBand(4).ReadAsArray() * 0.0001
            re2 = in_ds.GetRasterBand(5).ReadAsArray() * 0.0001
            re3 = in_ds.GetRasterBand(6).ReadAsArray() * 0.0001
            nir = in_ds.GetRasterBand(7).ReadAsArray() * 0.0001
            swir1 = in_ds.GetRasterBand(8).ReadAsArray() * 0.0001
            swir2 = in_ds.GetRasterBand(9).ReadAsArray() * 0.0001
            blue[blue == 0] = np.NAN #将反射率为0的像元设置为NAN，防止计算植被指数过程，除法报错
            green[green == 0] = np.NAN
            red[red == 0] = np.NAN
            re1[re1 == 0] = np.NAN
            re2[re2 == 0] = np.NAN
            re3[re3 == 0] = np.NAN
            nir[nir == 0] = np.NAN
            swir1[swir1 == 0] = np.NAN
            swir2[swir2 == 0] = np.NAN
            blue = blue.astype(np.float32)
            green = green.astype(np.float32)
            red = red.astype(np.float32)
            re1 = re1.astype(np.float32)
            re2 = re2.astype(np.float32)
            re3 = re3.astype(np.float32)
            nir = nir.astype(np.float32)
            swir1 = swir1.astype(np.float32)
            swir2 = swir2.astype(np.float32)
            # hang = red.shape[0];
            # lie = red.shape[1];
             #ndvi = red
            #for x in range(0,hang):
                #for y in range(0,lie):
                   #if red[x][y] == 0 :
                      #ndvi[x][y] = 0
                   #else:
                      #ndvi[x][y] = (nir[x][y] - red[x][y]) / (nir[x][y] + red[x][y])

            #植被指数
            ndvi = (nir - red) / (nir + red)
            ndvi1 = (nir -re1)/(nir+re1)
            ndvi2 = (nir -re2)/(nir+re2)
            ndvi3 = (nir -re3)/(nir+re3)
            nredi1 = (re2 - re1)/(re2 + re1)
            nredi2 = (re3 - re1)/(re3 + re1)
            nredi3 = (re3 - re2)/(re3 + re2)
            psri1 = (red - green)/re1
            psri2 = (red - green)/re2
            psri3 = (red - green)/re3
            ari1 =(1 / green)- (1 / re1)
            ari2 =(1 / green)- (1 / re2)
            ari3 =(1 / green)- (1 / re3)
            dvi = nir - red
            #evi = 2.5*(nir - red)/(nir + 6*red -7.5*green)#注意
            evi = 2.5*(nir - red)/(nir + 6*red -0.5*blue+1)#注意
            sr = nir/red
            sipi = (nir - blue)/(nir + blue)
            redsi = ((705 - 665)*(re3 - red) - (783-665)*(re1 - red)) / (2 * red)#注意
            vari = (re2-red)/(re2 + red)
            dswi = (nir + green)/(swir1+red)
            siwsi = (nir - swir1)/(nir + swir1)
            osavi = (nir - red)/(nir + red + 0.16)
            msr = (nir/red - 1)/(np.sqrt(nir/red) + 1)
            tvi = 0.5*(120*(nir - green) - 200*(red - green))
            gndvi = (nir - green)/(nir + green)
            rdvi = (nir - green)/(np.sqrt(nir + green))
            rgb = red / green


            # 将NAN转化为0值
            # nan_index = np.isnan(ndvi)
            # ndvi[nan_index] = 0
            #green = green.astype(np.float32)

            # 将计算好的NDVI保存为GeoTiff文件
            gtiff_driver = gdal.GetDriverByName('GTiff')

            #批量处理需要注意文件名是变量，这里截取对应原始文件的不带后缀的文件名
            #导出每个原始波段
            out_blue = gtiff_driver.Create(prename + 'blue' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_blue.SetProjection(in_ds.GetProjection())
            out_blue.SetGeoTransform(in_ds.GetGeoTransform())
            out_blueband = out_blue.GetRasterBand(1)
            out_blueband.WriteArray(blue)
            out_blueband.FlushCache()

            out_green = gtiff_driver.Create(prename + 'green' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_green.SetProjection(in_ds.GetProjection())
            out_green.SetGeoTransform(in_ds.GetGeoTransform())
            out_greenband = out_green.GetRasterBand(1)
            out_greenband.WriteArray(green)
            out_greenband.FlushCache()

            out_red = gtiff_driver.Create(prename + 'red' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_red.SetProjection(in_ds.GetProjection())
            out_red.SetGeoTransform(in_ds.GetGeoTransform())
            out_redband = out_red.GetRasterBand(1)
            out_redband.WriteArray(red)
            out_redband.FlushCache()


            out_re1 = gtiff_driver.Create(prename + 're1' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_re1.SetProjection(in_ds.GetProjection())
            out_re1.SetGeoTransform(in_ds.GetGeoTransform())
            out_re1band = out_re1.GetRasterBand(1)
            out_re1band.WriteArray(re1)
            out_re1band.FlushCache()

            out_re2 = gtiff_driver.Create(prename + 're2' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_re2.SetProjection(in_ds.GetProjection())
            out_re2.SetGeoTransform(in_ds.GetGeoTransform())
            out_re2band = out_re2.GetRasterBand(1)
            out_re2band.WriteArray(re2)
            out_re2band.FlushCache()

            out_re3 = gtiff_driver.Create(prename + 're3' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_re3.SetProjection(in_ds.GetProjection())
            out_re3.SetGeoTransform(in_ds.GetGeoTransform())
            out_re3band = out_re3.GetRasterBand(1)
            out_re3band.WriteArray(re3)
            out_re3band.FlushCache()

            out_nir = gtiff_driver.Create(prename + 'nir' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_nir.SetProjection(in_ds.GetProjection())
            out_nir.SetGeoTransform(in_ds.GetGeoTransform())
            out_nirband = out_nir.GetRasterBand(1)
            out_nirband.WriteArray(nir)
            out_nirband.FlushCache()

            out_swir1 = gtiff_driver.Create(prename + 'swir1' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_swir1.SetProjection(in_ds.GetProjection())
            out_swir1.SetGeoTransform(in_ds.GetGeoTransform())
            out_swir1band = out_swir1.GetRasterBand(1)
            out_swir1band.WriteArray(swir1)
            out_swir1band.FlushCache()

            out_swir2 = gtiff_driver.Create(prename + 'swir2' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_swir2.SetProjection(in_ds.GetProjection())
            out_swir2.SetGeoTransform(in_ds.GetGeoTransform())
            out_swir2band = out_swir2.GetRasterBand(1)
            out_swir2band.WriteArray(swir2)
            out_swir2band.FlushCache()


            #导出植被指数
            out_ndvi = gtiff_driver.Create(prename + 'ndvi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ndvi.SetProjection(in_ds.GetProjection())
            out_ndvi.SetGeoTransform(in_ds.GetGeoTransform())
            out_ndviband = out_ndvi.GetRasterBand(1)
            out_ndviband.WriteArray(ndvi)
            out_ndviband.FlushCache()

            out_ndvi1 = gtiff_driver.Create(prename + 'ndvi1' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ndvi1.SetProjection(in_ds.GetProjection())
            out_ndvi1.SetGeoTransform(in_ds.GetGeoTransform())
            out_ndvi1band = out_ndvi1.GetRasterBand(1)
            out_ndvi1band.WriteArray(ndvi1)
            out_ndvi1band.FlushCache()

            out_ndvi2 = gtiff_driver.Create(prename + 'ndvi2' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ndvi2.SetProjection(in_ds.GetProjection())
            out_ndvi2.SetGeoTransform(in_ds.GetGeoTransform())
            out_ndvi2band = out_ndvi2.GetRasterBand(1)
            out_ndvi2band.WriteArray(ndvi2)
            out_ndvi2band.FlushCache()

            out_ndvi3 = gtiff_driver.Create(prename + 'ndvi3' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ndvi3.SetProjection(in_ds.GetProjection())
            out_ndvi3.SetGeoTransform(in_ds.GetGeoTransform())
            out_ndvi3band = out_ndvi3.GetRasterBand(1)
            out_ndvi3band.WriteArray(ndvi3)
            out_ndvi3band.FlushCache()

            out_nredi1 = gtiff_driver.Create(prename + 'nredi1' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_nredi1.SetProjection(in_ds.GetProjection())
            out_nredi1.SetGeoTransform(in_ds.GetGeoTransform())
            out_nredi1band = out_nredi1.GetRasterBand(1)
            out_nredi1band.WriteArray(nredi1)
            out_nredi1band.FlushCache()

            out_nredi2 = gtiff_driver.Create(prename + 'nredi2' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_nredi2.SetProjection(in_ds.GetProjection())
            out_nredi2.SetGeoTransform(in_ds.GetGeoTransform())
            out_nredi2band = out_nredi2.GetRasterBand(1)
            out_nredi2band.WriteArray(nredi2)
            out_nredi2band.FlushCache()

            out_nredi3 = gtiff_driver.Create(prename + 'nredi3' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_nredi3.SetProjection(in_ds.GetProjection())
            out_nredi3.SetGeoTransform(in_ds.GetGeoTransform())
            out_nredi3band = out_nredi3.GetRasterBand(1)
            out_nredi3band.WriteArray(nredi3)
            out_nredi3band.FlushCache()

            out_psri1 = gtiff_driver.Create(prename + 'psri1' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_psri1.SetProjection(in_ds.GetProjection())
            out_psri1.SetGeoTransform(in_ds.GetGeoTransform())
            out_psri1band = out_psri1.GetRasterBand(1)
            out_psri1band.WriteArray(psri1)
            out_psri1band.FlushCache()

            out_psri2 = gtiff_driver.Create(prename + 'psri2' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_psri2.SetProjection(in_ds.GetProjection())
            out_psri2.SetGeoTransform(in_ds.GetGeoTransform())
            out_psri2band = out_psri2.GetRasterBand(1)
            out_psri2band.WriteArray(psri2)
            out_psri2band.FlushCache()

            out_psri3 = gtiff_driver.Create(prename + 'psri3' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_psri3.SetProjection(in_ds.GetProjection())
            out_psri3.SetGeoTransform(in_ds.GetGeoTransform())
            out_psri3band = out_psri3.GetRasterBand(1)
            out_psri3band.WriteArray(psri3)
            out_psri3band.FlushCache()

            out_ari1 = gtiff_driver.Create(prename + 'ari1' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ari1.SetProjection(in_ds.GetProjection())
            out_ari1.SetGeoTransform(in_ds.GetGeoTransform())
            out_ari1band = out_ari1.GetRasterBand(1)
            out_ari1band.WriteArray(ari1)
            out_ari1band.FlushCache()

            out_ari2 = gtiff_driver.Create(prename + 'ari2' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ari2.SetProjection(in_ds.GetProjection())
            out_ari2.SetGeoTransform(in_ds.GetGeoTransform())
            out_ari2band = out_ari2.GetRasterBand(1)
            out_ari2band.WriteArray(ari2)
            out_ari2band.FlushCache()

            out_ari3 = gtiff_driver.Create(prename + 'ari3' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ari3.SetProjection(in_ds.GetProjection())
            out_ari3.SetGeoTransform(in_ds.GetGeoTransform())
            out_ari3band = out_ari3.GetRasterBand(1)
            out_ari3band.WriteArray(ari3)
            out_ari3band.FlushCache()

            out_dvi = gtiff_driver.Create(prename + 'dvi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_dvi.SetProjection(in_ds.GetProjection())
            out_dvi.SetGeoTransform(in_ds.GetGeoTransform())
            out_dviband = out_dvi.GetRasterBand(1)
            out_dviband.WriteArray(dvi)
            out_dviband.FlushCache()

            out_evi = gtiff_driver.Create(prename + 'evi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_evi.SetProjection(in_ds.GetProjection())
            out_evi.SetGeoTransform(in_ds.GetGeoTransform())
            out_eviband = out_evi.GetRasterBand(1)
            out_eviband.WriteArray(evi)
            out_eviband.FlushCache()

            out_sr = gtiff_driver.Create(prename + 'sr' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_sr.SetProjection(in_ds.GetProjection())
            out_sr.SetGeoTransform(in_ds.GetGeoTransform())
            out_srband = out_sr.GetRasterBand(1)
            out_srband.WriteArray(sr)
            out_srband.FlushCache()

            out_sipi = gtiff_driver.Create(prename + 'sipi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_sipi.SetProjection(in_ds.GetProjection())
            out_sipi.SetGeoTransform(in_ds.GetGeoTransform())
            out_sipiband = out_sipi.GetRasterBand(1)
            out_sipiband.WriteArray(sipi)
            out_sipiband.FlushCache()

            out_redsi = gtiff_driver.Create(prename + 'redsi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_redsi.SetProjection(in_ds.GetProjection())
            out_redsi.SetGeoTransform(in_ds.GetGeoTransform())
            out_redsiband = out_redsi.GetRasterBand(1)
            out_redsiband.WriteArray(redsi)
            out_redsiband.FlushCache()

            out_vari = gtiff_driver.Create(prename + 'vari' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_vari.SetProjection(in_ds.GetProjection())
            out_vari.SetGeoTransform(in_ds.GetGeoTransform())
            out_variband = out_vari.GetRasterBand(1)
            out_variband.WriteArray(vari)
            out_variband.FlushCache()

            out_dswi = gtiff_driver.Create(prename + 'dswi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_dswi.SetProjection(in_ds.GetProjection())
            out_dswi.SetGeoTransform(in_ds.GetGeoTransform())
            out_dswiband = out_dswi.GetRasterBand(1)
            out_dswiband.WriteArray(dswi)
            out_dswiband.FlushCache()

            out_siwsi = gtiff_driver.Create(prename + 'siwsi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_siwsi.SetProjection(in_ds.GetProjection())
            out_siwsi.SetGeoTransform(in_ds.GetGeoTransform())
            out_siwsiband = out_siwsi.GetRasterBand(1)
            out_siwsiband.WriteArray(siwsi)
            out_siwsiband.FlushCache()

            out_osavi = gtiff_driver.Create(prename + 'osavi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_osavi.SetProjection(in_ds.GetProjection())
            out_osavi.SetGeoTransform(in_ds.GetGeoTransform())
            out_osaviband = out_osavi.GetRasterBand(1)
            out_osaviband.WriteArray(osavi)
            out_osaviband.FlushCache()

            out_msr = gtiff_driver.Create(prename + 'msr' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_msr.SetProjection(in_ds.GetProjection())
            out_msr.SetGeoTransform(in_ds.GetGeoTransform())
            out_msrband = out_msr.GetRasterBand(1)
            out_msrband.WriteArray(msr)
            out_msrband.FlushCache()

            out_tvi = gtiff_driver.Create(prename + 'tvi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_tvi.SetProjection(in_ds.GetProjection())
            out_tvi.SetGeoTransform(in_ds.GetGeoTransform())
            out_tviband = out_tvi.GetRasterBand(1)
            out_tviband.WriteArray(tvi)
            out_tviband.FlushCache()

            out_gndvi = gtiff_driver.Create(prename + 'gndvi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_gndvi.SetProjection(in_ds.GetProjection())
            out_gndvi.SetGeoTransform(in_ds.GetGeoTransform())
            out_gndviband = out_gndvi.GetRasterBand(1)
            out_gndviband.WriteArray(gndvi)
            out_gndviband.FlushCache()

            out_rdvi = gtiff_driver.Create(prename + 'rdvi' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_rdvi.SetProjection(in_ds.GetProjection())
            out_rdvi.SetGeoTransform(in_ds.GetGeoTransform())
            out_rdviband = out_rdvi.GetRasterBand(1)
            out_rdviband.WriteArray(rdvi)
            out_rdviband.FlushCache()

            out_rgb = gtiff_driver.Create(prename + 'rgb' + '.tif',
                             x_size, y_size, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_rgb.SetProjection(in_ds.GetProjection())
            out_rgb.SetGeoTransform(in_ds.GetGeoTransform())
            out_rgbband = out_rgb.GetRasterBand(1)
            out_rgbband.WriteArray(rgb)
            out_rgbband.FlushCache()
```


```python
if __name__ == '__main__':
    in_path = r'K:\编程学习视频\GEE培训\GEE_python_RC\3.Batch_Vis_loadimg\data' 
    out_path = r'K:\编程学习视频\GEE培训\GEE_python_RC\3.Batch_Vis_loadimg'
    BatchVis(in_path,out_path)
```

    ['K:\\编程学习视频\\GEE培训\\GEE_python_RC\\3.Batch_Vis_loadimg\\data\\SXNQS20180303.tif', 'K:\\编程学习视频\\GEE培训\\GEE_python_RC\\3.Batch_Vis_loadimg\\data\\SXNQS220171203.tif']
    


```python

```
