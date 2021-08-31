#!/usr/bin/env python
# coding: utf-8

# 目的：将一些常用的功能写成函数，方便日常工作中直接调用。后续的代码中也会直接调用这些函数，如：sentinel2影像获取、时间区域云量筛选、云掩膜、植被指数计算，直接利用模块下函数:general.S2Img(startdate, enddate,geometry,cloud,m,n)即可实现

# 使用方法:

# 1.将1.RC_module文件夹改为RC_module(不能加数字)放在代码同级目录下；

# 2.导入模块：from RC_module import general；

# 3.使用模块下的函数：general.函数名；general.funoutline(roi)

# 备注：如果RC_module文件夹不在代码的同级目录下，需要添加python搜索模块的目录，即添加RC_module文件夹所在目录

# In[ ]:


'''
import sys
import os
# print(sys.path) #python会去哪些目录下找模块，是一个列表
#添加RC_module模块存放路径
Module_path = r'K:\编程学习视频\GEE培训\0_GEE_python_RC'
Module_Dir = os.path.dirname(os.path.dirname(os.path.abspath(Module_path)))  #获取到模块目录
sys.path.append(Module_Dir)#把模块目录加到sys.path列表中
from RC_module import general
'''


# # 1.常规算法

# ## 1.1 显示矢量边界

# GEE的官方模块名为ee，推荐结合吴秋生老师发布的geemap模块搭配使用，geemap将GEE的很多功能以更少的代码实现了

# 如：Python版本GEE中没有Map功能，无法直接展示动态地图，使用geemap.Map()函数可以实现JS_GEE中的Map中的功能

# In[2]:


# Map = geemap.Map()
# Map


# In[ ]:


# 导入gee相关库，设置自己电脑端口，我的为‘7890’，初始化gee
import ee
import geemap
import os
#设置端口可以使用os模块，也可以使用geemap模块
#os模块方法
os.environ ['HTTP_PROXY'] ='http://127.0.0.1:7890'
os.environ ['HTTPS_PROXY'] ='http://127.0.0.1:7890'
#geeemap方法
# geemap.set_proxy(port=7890)
ee.Initialize()


# In[ ]:


#GEE中直接显示矢量区域时，矢量边界和整个区域都会显示，funoutline(roi)可以只显示矢量边界
def funoutline(roi):
  output = ee.Image().toByte().paint(featureCollection = roi, color = 0, width = 2)
  return output


# ## 1.2 植被指数计算

# ### 1.2.1 归一化函数

# In[ ]:


def ND(image,b1,b2,bName):
  VI = image.normalizedDifference([b1,b2]).rename(bName)
  return VI.updateMask(VI.gt(-1).And(VI.lt(1)))


# ### 1.2.2 植被指数

# In[ ]:


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

# In[ ]:


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


# ## 1.4 显示影像数据信息

# In[7]:


'''
funimgprop：显示单个影像信息
参数：item：img，单个影像
输出：影像的ID和Time
funimgcprop：显示影像数据集信息
参数：imgc：影像数据集
*imgc_len：输出的长度，默认为全部输出
输出：影像集合的ID和Time
'''
def funimgprop(item):
    img = ee.Image(item)
    img_ID = img.id()
    img_time = ee.Date(img.get('system:time_start')).format('yyyy-MM-dd')
    return {'image':img_ID,'system:time_start':img_time}
def funimgcprop(imgc,*imgc_len):
    if imgc_len ==():
        imgc_len = int(imgc.size().getInfo())
    else:
        imgc_len = imgc_len[0]
    imgc_list = imgc.toList(imgc.size())
    imgc_prop = imgc_list.map(funimgprop)
    imgc_prop_info = imgc_prop.getInfo()
    for i in range(imgc_len):
        print(imgc_prop_info[i])


# # 2 Sentinel数据处理

# ## 2.1 Sentinel2去云

# In[4]:


def S2Cloud(image):
    qa = image.select('QA60')
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.select().addBands(image.updateMask(mask).divide(10000))


# ## 2.2 计算指数并且添加为对应波段

# In[2]:


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


# ## 2.3 获取Sentinel2影像数据

# In[9]:


#直接获取Sentinel2影像数据，同时实现时间区域云量筛选、云掩膜、植被指数计算
#参数：#startdate，enddate影像起始和终止时间
    #geometry：获取的影像区域
    #cloud:按云量筛选影像,0-100
    #m:是否做云掩膜，0表示不做，！0表示做
    #n:是否计算植被指数，0表示不做，！0表示做
#return：Imgcollection
def S2Img(startdate, enddate,geometry,cloud=100,m=0,n=0):
    S2= ee.ImageCollection('COPERNICUS/S2').filterDate(startdate, enddate).filterBounds(geometry).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud))
    def Reflec(image):
        return image.select().addBands(image.divide(10000))
    if (m==0 and n==0):
        return S2.map(Reflec)
    elif (m!=0 and n==0):
        return S2.map(S2Cloud)
    elif (m==0 and n!=0):
        return S2.map(Reflec).map(S2Vis)
    else:
        return S2.map(S2Cloud).map(S2Vis)


# In[ ]:




