# 1.农气站点TXT文件批量转shp


```python
#数据类型：农气数据.txt
#实验目的：1.农气站点TXT文件批量转shp
#          1.1将农气站点TXT数据批量转成csv格式
#          1.2提取农气站点TXT数据中某个类别数据批量转成csv格式
#          1.3将csv站点数据批量转成shp数据
#          1.4shp数据批量投影
```


```python
#-*-coding:utf-8-*-
#导入os和pandas库
import os
import pandas as pd
import shapefile as shp
import csv
import codecs
import os
from osgeo import osr
```


```python
#设置输入输出路径
input_dir=(r'G:\数据恢复\2021工作\0325_野外实验设计\4_第二届数字地球大会\3_实验处理\3.1_生育期预测\0_data')#存放TXT文件路径
output_csvdir=(r'G:\数据恢复\2021工作\0325_野外实验设计\4_第二届数字地球大会\3_实验处理\3.1_生育期预测\1_csv')#存放csv文件路径
output_shpdir=(r'G:\数据恢复\2021工作\0325_野外实验设计\4_第二届数字地球大会\3_实验处理\3.1_生育期预测\2_shp')#存放shp文件路径
```


```python
#修改当前工作路径
os.chdir(input_dir)
os.getcwd()
```

## 1.1将txt格式直接转换成csv格式


```python
#读取input_dir文件夹下所有TXT文件
for root, dirs, files in os.walk(input_dir):
    print(files)
```


```python
#创建列表存放数据
data = []#存放原始TXT文件数据
filename = []#存放文件名
wheatdata=[]#存放小麦类别数据
```


```python
#读取数据
for i in range (len(files)):
    data.append(pd.read_table(files[i],sep='\s+'))
#     data.append(pd.read_table(files[i],sep='\s+',header=None))
    filename.append(files[i].split('.'))
print('END!')
```


```python
#写入数据到csv
for i in range (len(data)):  
    data[i].to_csv(output_csvdir+ os.sep +filename[i][0]+'.csv',encoding="utf_8_sig")
```

## 1.2提取小麦类别数据转为csv


```python
for i in range (len(data)):  
    wheatdata.append(data[i][(data[i]['Crop_Name']==10301) | (data[i]['Crop_Name']==10302) | (data[i]['Crop_Name']==10303)])
```


```python
#写入数据到csv
for i in range (len(wheatdata)):  
    wheatdata[i].to_csv(output_csvdir+ os.sep +filename[i][0]+'winterwheat.csv',encoding="utf_8_sig")
```


```python
#提取指定行列数据转为csv
# a =wheatdata[2].iloc[0:3506,:]
# a.to_csv(output_csvdir+ os.sep +filename[i][0]+'winterwheat222.csv',encoding="utf_8_sig")
```

## 1.3根据经纬度转换csv格式为shp格式


```python
for root, dirs, files in os.walk(output_csvdir):
    print(files)
```


```python
for i in range(len(files)):
    fnn = files[i].split('.')[0]
#     print(files[i])
    if files[i].split('.')[0].find('wheat') != (-1):  #不包含‘wheat’,返回-1
        print(files[i])
        #创建shp文件
        output_shp = shp.Writer(output_shpdir+ os.sep + "%s.shp" % fnn.split('.')[0], shp.POINT, encoding='utf-8')
        # for every record there must be a corresponding geometry.
        output_shp.autoBalance = 1
        #字符：'c';数字：'N';浮点：'F';逻辑：'L';日期：'D'
        output_shp.field('Province', 'C', 50) # string
        output_shp.field('City', 'C', 50) # string
        output_shp.field('Cnty', 'C', 50) # string
        output_shp.field('Town_Station_Id_C', 'F', 10, 8) # int
        output_shp.field('Lat', 'F', 10, 8) # float
        output_shp.field('Lon', 'F', 10, 8) # float
        output_shp.field('Alti', 'F', 10, 8) # float
        output_shp.field('Admin_Code_CHN', 'F', 10, 8) # float
        output_shp.field('Year', 'F', 10, 8) # int
        output_shp.field('Mon', 'F', 10, 8) # int
        output_shp.field('Day', 'F', 10, 8) # int
        output_shp.field('Crop_Name',  'F', 10, 8) # int
        output_shp.field('GroPer_Name_Ten',  'F', 10, 8) # int
        # access the CSV file
        with codecs.open(output_csvdir+ os.sep + fnn + '.csv', 'rb', 'utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # skip the header
            next(reader, None)
            #loop through each of the rows and assign the attributes to variables
            for row in reader:
                Province = row[2]
                print(Province)
                City = row[3]
                Cnty = row[4]
                Town_Station_Id_C = float(row[5])
                Lat = float(row[6])
                Lon = float(row[7])
                Alti = float(row[8])
                Admin_Code_CHN = float(row[9])
                Year = float(row[10])
                Mon = float(row[11])
                Day = float(row[12])
                Crop_Name = float(row[13])
                GroPer_Name_Ten = float(row[14])
                #print(type(Province),type(City),type(Cnty),type(Town_Station_Id_C),type(Lat))
                # create the point geometry
                output_shp.point(Lon, Lat)
                output_shp.record(Province, City, Cnty,Town_Station_Id_C,Lat,Lon,Alti,Admin_Code_CHN,Year,Mon,Day,Crop_Name,GroPer_Name_Ten)
```

## 1.4定义投影


```python
# 定义投影
proj = osr.SpatialReference() 
proj.ImportFromEPSG(4326) # 4326-GCS_WGS_1984; 4490- GCS_China_Geodetic_Coordinate_System_2000
wkt = proj.ExportToWkt()
for root, dirs, files in os.walk(output_shpdir):
    print(root)
for i in range (len(files)):
    if files[i].split('.')[1] == 'shp':
        # 写入投影
        print(files[i])
        f = open((root+os.sep+files[i]).replace(".shp", ".prj"), 'w') 
        f.write(wkt)#写入投影信息
        f.close()#关闭操作流
```
