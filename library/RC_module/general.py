#!/usr/bin/env python
# coding: utf-8

# # 1.常规算法

# ## 1.1 显示矢量边界

# 导入gee相关库，设置端口‘7890’，初始化gee

# In[1]:


import ee
import geemap
import os
os.environ ['HTTP_PROXY'] ='http://127.0.0.1:7890'
os.environ ['HTTPS_PROXY'] ='http://127.0.0.1:7890'
ee.Initialize()


# In[3]:


def funoutline(roi):
  output = ee.Image().toByte().paint(featureCollection = roi, color = 0, width = 2)
  return output


# ## 1.2 植被指数计算

# ### 1.2.1 归一化函数

# In[7]:


def ND(image,b1,b2,bName):
  VI = image.normalizedDifference([b1,b2]).rename(bName)
  return VI.updateMask(VI.gt(-1).And(VI.lt(1)))


# ### 1.2.2 植被指数

# In[20]:


#DVI
def funDVI(image,B1,B2):
  VI = image.expression('nir - red',{'nir':  image.select(B1),   'red':  image.select(B2)}).rename('DVI')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));

#DSWI
def funDSWI(image,B1,B2,B3,B4,bname):
  VI = image.expression('(nir + green) / (swir + red)',{'nir':  image.select(B1),   'green':image.select(B2),'swir': image.select(B3),'red':  image.select(B4)}).rename(bname)
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));

#EVI 计算
def funEVI(image,B1,B2,B3):
  VI = image.expression('2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)',{ 'blue': image.select(B1),'red': image.select(B2),'nir': image.select(B3)}).rename('EVI')
  return VI.updateMask(VI.gt(-1).And(VI.lt(1)))


#MSR
def funMSR(image,B1,B2):
  VI = image.expression('(nir / red - 1)/(sqrt(nir+red)+1)',{'red':  image.select(B1),   'nir':  image.select(B2)}).rename('MSR')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


#OSAVI
def funOSAVI(image,B1,B2):
  VI = image.expression('(nir - red)/(nir + red + 0.16)',{'nir':  image.select(B1),   'red':  image.select(B2)}).rename('OSAVI')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


#PSRI
def funPSRI(image,B1,B2,B3,bname):
  VI = image.expression('(red - green)/re',{'red':  image.select(B1),   'green':  image.select(B2),'re':   image.select(B3)}).rename(bname)
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


#RGB
def funRGB(image,B1,B2):
  VI = image.expression('red / green',{'red':  image.select(B1),   'green':  image.select(B2)}).rename('RGB')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


#RDVI
def funRDVI(image,B1,B2):
  VI = image.expression('(nir - red )/(sqrt(nir+red))',{'nir':  image.select(B1),   'red':  image.select(B2)}).rename('RDVI')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


#REDSI
def funREDSI(image,B1,B2,B3):
  VI = image.expression('((705 - 665)*(re3 - red) - (783-665) * (re1 - red))/ (2 * red)',{'re3':  image.select(B1),   'red':  image.select(B2),'re1':   image.select(B3)}).rename('REDSI')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


#SR
def funSR(image,B1,B2):
  VI = image.expression('nir / red',{ 'nir':  image.select(B1),   'red':  image.select(B2)}).rename('SR')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


#TVI
def funTVI(image,B1,B2,B3):
  VI = image.expression('0.5 * (120 * (nir - green) - 200 * (red - green))',{'nir':  image.select(B1),   'green':  image.select(B2),'red':   image.select(B3)}).rename('TVI')
  return VI#.updateMask(VI.gt(-1).and(VI.lt(1)));


# ## 1.3 插值

# In[26]:


#IDW
def funIDW(shp,property,range):
    #get mean
    mean_value = shp.reduceColumns(ee.Reducer.mean(),[property])
    #print(mean_value)
    #get stdev
    sd_value = shp.reduceColumns(ee.Reducer.stdDev(),[property])
    #print(sd_value)
    img = shp.inverseDistance(range = range, propertyName = property,mean = mean_value.getInfo()['mean'],stdDev=sd_value.getInfo()['stdDev'], reducer = ee.Reducer.mean())
    return img


# # 2 Sentinel数据处理

# ## 2.1 Sentinel2去云

# In[ ]:


def S2Cloud(image):
  qa = image.select('QA60')
  cloudBitMask = 1 << 10
  cirrusBitMask = 1 << 11
  mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
  return image.updateMask(mask).divide(10000)


# ## 2.2 获取Sentinel2影像数据

# In[ ]:


def S2Img(startdate, enddate,geometry,cloud):
  S2= ee.ImageCollection('COPERNICUS/S2').filterDate(startdate, enddate).filterBounds(geometry).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud)).map(S2Cloud)
  return S2


# ## 2.3 计算指数并且添加为对应波段

# In[21]:


def S2Vis(img):
    NDVI = ND(img,'B8','B4','NDVI')
    NDVIre1 = ND(img,'B5','B4','NDVIre1')
    NDVIre2 = ND(img,'B6','B4','NDVIre2')
    NDVIre3 = ND(img,'B7','B4','NDVIre3')
    GNDVI = ND(img,'B8','B3','GNDVI')
    LSWI = ND(img,'B8','B11','LSWI')
    NDWI = ND(img,'B3','B8','NDWI')
    mNDWI = ND(img,'B3','B11','mNDWI')
    SIPI = ND(img,'B8','B2','SIPI')
    SIWSI1 = ND(img,'B8','B11','SIWSI1')
    SIWSI2 = ND(img,'B8','B12','SIWSI2')
    EVI = funEVI(img,'B2','B4','B8')
    RGB = funRGB(img,'B4','B3')
    MSR = funMSR(img,'B4','B8')
    SR = funSR(img,'B8','B4')
    RDVI = funRDVI(img,'B8','B4')
    DVI = funDVI(img,'B8','B4')
    OSAVI = funOSAVI(img,'B8','B4')
    PSRI1 = funPSRI(img,'B4','B5','B5','PSRI1')
    PSRI2 = funPSRI(img,'B4','B5','B6','PSRI2')
    PSRI3 = funPSRI(img,'B4','B5','B7','PSRI3')
    REDSI = funREDSI(img,'B7','B4','B5')
    TVI = funTVI(img,'B8','B3','B4')
    DSWI1 = funDSWI(img,'B8','B3','B11','B4','DSWI1')
    DSWI2 = funDSWI(img,'B8','B3','B12','B4','DSWI2')
    output = img.addBands(NDVI).addBands(NDVIre1).addBands(NDVIre2).addBands(NDVIre3).addBands(SIWSI1).addBands(SIWSI2).addBands(GNDVI).addBands(LSWI).addBands(NDWI).addBands(mNDWI).addBands(SIPI).addBands(EVI).addBands(RGB).addBands(MSR).addBands(SR).addBands(RDVI).addBands(DVI).addBands(OSAVI).addBands(PSRI1).addBands(PSRI2).addBands(PSRI3).addBands(REDSI).addBands(TVI).addBands(DSWI1).addBands(DSWI2)
    return output


# In[ ]:




