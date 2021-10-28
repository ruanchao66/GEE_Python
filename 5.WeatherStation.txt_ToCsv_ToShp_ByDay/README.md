# 1. 中国地面气候资料日值数据集(V3.0).txt转成矢量数据.shp


```python
#数据类型：气象站点数据.txt(中国地面气候资料日值数据集(V3.0))
#实验目的：1.气象站点TXT文件批量转shp
#          1.1将气象站点TXT数据批量转成csv格式
#          1.2提取气象站点TXT数据逐日数据批量转成csv格式
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
from rich.progress import track

#设置输入输出路径
input_dir=(r'K:\全国气象数据（2000-2018年）\2021年\0_data')#存放TXT文件路径
output_csvdir=(r'K:\全国气象数据（2000-2018年）\2021年\5_逐日数据处理\ss')#存放csv文件路径
output_shpdir=(r'K:\全国气象数据（2000-2018年）\2021年\5_逐日数据处理\sss')#存放shp文件路径

#修改当前工作路径
os.chdir(input_dir)
os.getcwd()
```

## 1.1 剔除txt中异常值


```python
# 读取路径下所有文件
for root, dirs, files in os.walk(input_dir):
    print(files[1])
# 存放路径下数据和文件名
dataTEM = []
dataGST = []
dataSSD = []
dataRHU = []
dataPRE = []
filenameTEM = []
filenameGST = []
filenameSSD = []
filenameRHU = []
filenamePRE = []
# 将不同类型的数据单独存放
for i in range(len(files)):
    io = files[i]
    if os.path.splitext(files[i])[1] == '.txt':
        if files[i].split('-')[1] == 'TEM':
            dataTEM.append(pd.read_table(io, sep='\s+', header=None))
            filenameTEM.append(files[i].split('.')[0])
            # print(filenameTEM[0])
        if files[i].split('-')[1] == 'GST':
            dataGST.append(pd.read_table(io, sep='\s+', header=None))
            filenameGST.append(files[i].split('.')[0])
            # print(filenameTEM[0])
        if files[i].split('-')[1] == 'RHU':
            dataRHU.append(pd.read_table(io, sep='\s+', header=None))
            filenameRHU.append(files[i].split('.')[0])
            # print(filenameTEM[0])
        if files[i].split('-')[1] == 'PRE':
            dataPRE.append(pd.read_table(io, sep='\s+', header=None))
            filenamePRE.append(files[i].split('.')[0])
            # print(filenameTEM[0])
        if files[i].split('-')[1] == 'SSD':
            dataSSD.append(pd.read_table(io, sep='\s+', header=None))
            filenameSSD.append(files[i].split('.')[0])
            # print(filenameTEM[0])

# 剔除异常值：1.其中整月全部日数据都为异常值，则删除该站点；2.个别异常值则用相邻日数据替代
# 注：原始站点数据个别站点缺失某些日数据，未处理；
# 剔除整月全部为异常值的站点
def DelectErrorstation(dataset):
    for i in range(len(dataset)):
        a = dataset[i].groupby([0], as_index=False)[7].mean()  # 求每个站点月平均值，提取整月都为异常值的站点
        b = a[(a[7] == 32766) | (a[7] == 999990)][0]  # 提取整月都为异常值的站点
        b.index.name = None  # 去行名称
        dataset[i] = dataset[i][~dataset[i][0].isin(b)]  # 删除包含异常站点的数据
        if dataset[i].shape[1] == 13:
            a = dataset[i].groupby([0], as_index=False)[8].mean()  # 求每个站点月平均值，提取整月都为异常值的站点
            b = a[(a[8] == 32766) | (a[8] == 999990)][0]  # 提取整月都为异常值的站点
            b.index.name = None  # 去行名称
            dataset[i] = dataset[i][~dataset[i][0].isin(b)]  # 删除包含异常站点的数据
            a = dataset[i].groupby([0], as_index=False)[9].mean()  # 求每个站点月平均值，提取整月都为异常值的站点
            b = a[(a[9] == 32766) | (a[9] == 999990)][0]  # 提取整月都为异常值的站点
            b.index.name = None  # 去行名称
            dataset[i] = dataset[i][~dataset[i][0].isin(b)]  # 删除包含异常站点的数据

DelectErrorstation(dataTEM)
DelectErrorstation(dataGST)
DelectErrorstation(dataRHU)
DelectErrorstation(dataPRE)
DelectErrorstation(dataSSD)

# 个别异常值则用相邻日数据替代
def ReplaceErrorvalue(data_month):
    print('异常值去除')
    for i in range(len(data_month)):
        #     nodata = dataTEM[i][(dataTEM[i][7] > 30000)|(dataTEM[i][8] > 30000)|(dataTEM[i][9] > 30000)]
        nodata1 = data_month[i][(data_month[i][7] > 30000)].index
        for j in range(len(nodata1)):
            if data_month[i].loc[nodata1[j],6] > 1:
                data_month[i].loc[nodata1[j],7] = data_month[i].loc[nodata1[j]-1,7]
            elif (data_month[i].loc[nodata1[j],6] <= 1) & (data_month[i].loc[nodata1[j]+1,7] > 30000):
                datastation = data_month[i][data_month[i][0] == data_month[i].loc[nodata1[j],0]]
                datamean = datastation[datastation[7] < 30000][7].mean()
                data_month[i].loc[nodata1[j],7] = datamean
            else:
                data_month[i].loc[nodata1[j],7] = data_month[i].loc[nodata1[j]+1,7]
        if data_month[i].shape[1] == 13:
            nodata2 = data_month[i][(data_month[i][8] > 30000)].index
#             print(nodata2)
            nodata3 = data_month[i][(data_month[i][9] > 30000)].index
#             print(nodata3)
            for j in range(len(nodata2)):
                if data_month[i].loc[nodata2[j],6] > 1:
                    data_month[i].loc[nodata2[j],8] = data_month[i].loc[nodata2[j]-1,8]
                elif (data_month[i].loc[nodata2[j],6] <= 1) & (data_month[i].loc[nodata2[j]+1,8] > 30000):
                    datastation = data_month[i][data_month[i][0] == data_month[i].loc[nodata2[j],0]]
                    datamean = datastation[datastation[8] < 30000][8].mean()
                    data_month[i].loc[nodata2[j], 8] = datamean
                else:
                    data_month[i].loc[nodata2[j],8] = data_month[i].loc[nodata2[j]+1,8]
            for j in range(len(nodata3)):
                if data_month[i].loc[nodata3[j],6] > 1:
                    data_month[i].loc[nodata3[j],9] = data_month[i].loc[nodata3[j]-1,9]
                elif (data_month[i].loc[nodata3[j],6] <= 1) & (data_month[i].loc[nodata3[j]+1,9] > 30000):
                    datastation = data_month[i][data_month[i][0] == data_month[i].loc[nodata3[j],0]]
                    datamean = datastation[datastation[9] < 30000][9].mean()
                    data_month[i].loc[nodata3[j],9] = datamean
                else:
                    data_month[i].loc[nodata3[j],9] = data_month[i].loc[nodata3[j]+1,9]
#检测是否有异常值，验证数据
    for i in range(len(data_month)):
        #     nodata = dataTEM[i][(dataTEM[i][7] > 30000)|(dataTEM[i][8] > 30000)|(dataTEM[i][9] > 30000)]
        nodata1 = data_month[i][(data_month[i][7] > 30000)].index
        if data_month[i].shape[1] == 13:
            nodata2 = data_month[i][(data_month[i][8] > 30000)].index
            nodata3 = data_month[i][(data_month[i][9] > 30000)].index
        else:
            nodata2 = pd.DataFrame([])
            nodata3 = pd.DataFrame([])
        if nodata1.empty & nodata2.empty & nodata3.empty:
            print('无异常值')
        else:
            print('有异常值')

ReplaceErrorvalue(dataTEM)
ReplaceErrorvalue(dataGST)
ReplaceErrorvalue(dataSSD)
ReplaceErrorvalue(dataRHU)
ReplaceErrorvalue(dataPRE)
```

## 1.2 将txt格式转换成csv格式


```python
#保存数据到csv
#提取数据列
#TEM
for i in track(range(len(dataTEM))):
    tem = dataTEM[i][7] *0.1
    htem = dataTEM[i][8] *0.1
    ltem = dataTEM[i][9] *0.1
    #提取站点
    station = dataTEM[i][0]    
    #提取站点经纬度
    locationINT = dataTEM[i].iloc[:,1:3] // 100
    locationPOINT = dataTEM[i].iloc[:,1:3] % 100 / 60
    locationactual = locationINT + locationPOINT
    locationactual.columns = ['Y','X']
    X = locationactual.loc[:,'X']
    Y = locationactual.loc[:,'Y']
    #提取站点海拔高度
    height = dataTEM[i][3] / 10
    #提取日期
    year = dataTEM[i][4]
    month = dataTEM[i][5]
    day = dataTEM[i][6]
    #写出数据
    final_data = pd.DataFrame({'X':X,'Y':Y,'站点':station,'海拔高度':height,'年':year,'月':month,'日':day,'日均气温':tem,'月均最高气温':htem,'月均最低气温':ltem})
    final_data.to_csv(output_csvdir+ os.sep +filenameTEM[i]+'_day.csv',encoding="utf_8_sig")
#     final_data.to_excel(output_csvdir+ os.sep +filenameTEM[i]+'_day.xlsx',encoding="utf_8_sig")
#GST
for i in track(range(len(dataGST))):
    tem = dataGST[i][7] *0.1
    htem = dataGST[i][8] *0.1
    ltem = dataGST[i][9] *0.1
    #提取站点
    station = dataGST[i][0]    
    #提取站点经纬度
    locationINT = dataGST[i].iloc[:,1:3] // 100
    locationPOINT = dataGST[i].iloc[:,1:3] % 100 / 60
    locationactual = locationINT + locationPOINT
    locationactual.columns = ['Y','X']
    X = locationactual.loc[:,'X']
    Y = locationactual.loc[:,'Y']
    #提取站点海拔高度
    height = dataGST[i][3] / 10
    #提取日期
    year = dataGST[i][4]
    month = dataGST[i][5]
    day = dataGST[i][6]
    #写出数据
    final_data = pd.DataFrame({'X':X,'Y':Y,'站点':station,'海拔高度':height,'年':year,'月':month,'日':day,'日均气温':tem,'月均最高气温':htem,'月均最低气温':ltem})
    final_data.to_csv(output_csvdir+ os.sep +filenameGST[i]+'_day.csv',encoding="utf_8_sig")
#     final_data.to_excel(output_csvdir+ os.sep +filenameGST[i]+'_day.xlsx',encoding="utf_8_sig")
#RHU
for i in track(range(len(dataRHU))):
    rhu = dataRHU[i][7]
    #提取站点
    station = dataRHU[i][0]    
    #提取站点经纬度
    locationINT = dataRHU[i].iloc[:,1:3] // 100
    locationPOINT = dataRHU[i].iloc[:,1:3] % 100 / 60
    locationactual = locationINT + locationPOINT
    locationactual.columns = ['Y','X']
    X = locationactual.loc[:,'X']
    Y = locationactual.loc[:,'Y']
    #提取站点海拔高度
    height = dataRHU[i][3] / 10
    #提取日期
    year = dataRHU[i][4]
    month = dataRHU[i][5]
    day = dataRHU[i][6]
    #写出数据
    final_data = pd.DataFrame({'X':X,'Y':Y,'站点':station,'海拔高度':height,'年':year,'月':month,'日':day,'相对湿度':rhu})
    final_data.to_csv(output_csvdir+ os.sep +filenameRHU[i]+'_day.csv',encoding="utf_8_sig")
#     final_data.to_excel(output_csvdir+ os.sep +filenameRHU[i]+'_day.xlsx',encoding="utf_8_sig")
#PRE
for i in track(range(len(dataPRE))):
    dpre = dataPRE[i][7] *0.1
    npre = dataPRE[i][8] *0.1
    pre = dataPRE[i][9] *0.1
    #提取站点
    station = dataPRE[i][0]    
    #提取站点经纬度
    locationINT = dataPRE[i].iloc[:,1:3] // 100
    locationPOINT = dataPRE[i].iloc[:,1:3] % 100 / 60
    locationactual = locationINT + locationPOINT
    locationactual.columns = ['Y','X']
    X = locationactual.loc[:,'X']
    Y = locationactual.loc[:,'Y']
    #提取站点海拔高度
    height = dataPRE[i][3] / 10
    #提取日期
    year = dataPRE[i][4]
    month = dataPRE[i][5]
    day = dataPRE[i][6]
    #写出数据
    final_data = pd.DataFrame({'X':X,'Y':Y,'站点':station,'海拔高度':height,'年':year,'月':month,'日':day,'月白天均降水':dpre,'月夜间均降水':npre,'月均降水':pre})
    final_data.to_csv(output_csvdir+ os.sep +filenamePRE[i]+'_day.csv',encoding="utf_8_sig")
#     final_data.to_excel(output_csvdir+ os.sep +filenamePRE[i]+'_day.xlsx',encoding="utf_8_sig")
#SSD
for i in track(range(len(dataSSD))):
    ssd = dataSSD[i][7]*0.1
    #提取站点
    station = dataSSD[i][0]    
    #提取站点经纬度
    locationINT = dataSSD[i].iloc[:,1:3] // 100
    locationPOINT = dataSSD[i].iloc[:,1:3] % 100 / 60
    locationactual = locationINT + locationPOINT
    locationactual.columns = ['Y','X']
    X = locationactual.loc[:,'X']
    Y = locationactual.loc[:,'Y']
    #提取站点海拔高度
    height = dataSSD[i][3] / 10
    #提取日期
    year = dataSSD[i][4]
    month = dataSSD[i][5]
    day = dataSSD[i][6]
    #写出数据
    final_data = pd.DataFrame({'X':X,'Y':Y,'站点':station,'海拔高度':height,'年':year,'月':month,'日':day,'月均日照时数':ssd})
    final_data.to_csv(output_csvdir+ os.sep +filenameSSD[i]+'_day.csv',encoding="utf_8_sig")
#     final_data.to_excel(output_csvdir+ os.sep +filenameSSD[i]+'_day.xlsx',encoding="utf_8_sig")
print('数据导出到excel已完成！')
```

## 1.3 根据经纬度转换csv格式为shp格式


```python
for root, dirs, files in os.walk(output_csvdir):
#     print(root) #当前目录路径
#     print(dirs) #当前路径下所有子目录
#     print(files) #当前路径下所有非目录子文件
    print('开始转换矢量')
for i in track(range(len(files))):
    if files[i].split('.')[1] == 'csv':
        if files[i].split('-')[1]=='GST':
            fnn = files[i].split('.')[0]
#             print(fnn)
            output_shp = shp.Writer(output_shpdir+ os.sep + "%s.shp" % fnn, shp.POINT, encoding='gbk') #encoding='utf-8'
            # output_shp = shp.Writer(output+ os.sep + "%s.shp" % fnn.split('.')[0], shp.POINT) #encoding='utf-8'
            # for every record there must be a corresponding geometry.
            output_shp.autoBalance = 1
            # create the field names and data type for each.you can omit fields here
            output_shp.field('station', 'F', 10, 8) # float
            output_shp.field('longitude', 'F', 10, 8) # float
            output_shp.field('latitude', 'F', 10, 8) # float
            output_shp.field('height', 'F', 10, 8) # float
            output_shp.field('Year', 'F', 10, 8) # int
            output_shp.field('Mon', 'F', 10, 8) # int
            output_shp.field('Day', 'F', 10, 8) # int            
            output_shp.field('gst', 'F', 10, 8) # string, max-length
            output_shp.field('hgst', 'F', 10, 8) # string, max-length
            output_shp.field('lgst', 'F', 10, 8) # string, max-length
            # access the CSV file
            with codecs.open(output_csvdir+ os.sep + fnn + '.csv', 'rb', 'utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
            # skip the header
                next(reader, None)
                #loop through each of the rows and assign the attributes to variables
                for row in reader:
                    station = row[3]
                    height= row[4]
                    year = row[5]
                    month = row[6]
                    day = row[7]
                    gst= row[8]
                    hgst= row[9]
                    lgst= row[10]
                    lng = float(row[1])
                    lat = float(row[2])
                    # create the point geometry
                    output_shp.point(lng, lat)
                    # add attribute data
                    output_shp.record(station,lng, lat, height,year,month,day,gst,hgst,lgst)
        
        if files[i].split('-')[1]=='TEM':
            fnn = files[i].split('.')[0]
#             print(fnn)
            output_shp = shp.Writer(output_shpdir+ os.sep + "%s.shp" % fnn, shp.POINT, encoding='gbk') #encoding='utf-8'
            # output_shp = shp.Writer(output+ os.sep + "%s.shp" % fnn.split('.')[0], shp.POINT) #encoding='utf-8'
            # for every record there must be a corresponding geometry.
            output_shp.autoBalance = 1
            # create the field names and data type for each.you can omit fields here
            output_shp.field('station', 'F', 10, 8) # float
            output_shp.field('longitude', 'F', 10, 8) # float
            output_shp.field('latitude', 'F', 10, 8) # float
            output_shp.field('height', 'F', 10, 8) # float
            output_shp.field('Year', 'F', 10, 8) # int
            output_shp.field('Mon', 'F', 10, 8) # int
            output_shp.field('Day', 'F', 10, 8) # int            
            output_shp.field('tem', 'F', 10, 8) # string, max-length
            output_shp.field('htem', 'F', 10, 8) # string, max-length
            output_shp.field('ltem', 'F', 10, 8) # string, max-length
            # access the CSV file
            with codecs.open(output_csvdir+ os.sep + fnn + '.csv', 'rb', 'utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
            # skip the header
                next(reader, None)
                #loop through each of the rows and assign the attributes to variables
                for row in reader:
                    station = row[3]
                    height= row[4]
                    year = row[5]
                    month = row[6]
                    day = row[7]
                    tem= row[8]
                    htem= row[9]
                    ltem= row[10]
                    lng = float(row[1])
                    lat = float(row[2])
                    # create the point geometry
                    output_shp.point(lng, lat)
                    # add attribute data
                    output_shp.record(station,lng, lat, height,year,month,day,tem,htem,ltem)  
        
        if files[i].split('-')[1]=='RHU':
            fnn = files[i].split('.')[0]
#             print(fnn)
            output_shp = shp.Writer(output_shpdir+ os.sep + "%s.shp" % fnn, shp.POINT, encoding='gbk') #encoding='utf-8'
            # output_shp = shp.Writer(output+ os.sep + "%s.shp" % fnn.split('.')[0], shp.POINT) #encoding='utf-8'
            # for every record there must be a corresponding geometry.
            output_shp.autoBalance = 1
            # create the field names and data type for each.you can omit fields here
            output_shp.field('station', 'F', 10, 8) # float
            output_shp.field('longitude', 'F', 10, 8) # float
            output_shp.field('latitude', 'F', 10, 8) # float
            output_shp.field('height', 'F', 10, 8) # float
            output_shp.field('Year', 'F', 10, 8) # int
            output_shp.field('Mon', 'F', 10, 8) # int
            output_shp.field('Day', 'F', 10, 8) # int            
            output_shp.field('rhu', 'F', 10, 8) # string, max-length
            # access the CSV file
            with codecs.open(output_csvdir+ os.sep + fnn + '.csv', 'rb', 'utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
            # skip the header
                next(reader, None)
                #loop through each of the rows and assign the attributes to variables
                for row in reader:
                    station = row[3]
                    height= row[4]
                    year = row[5]
                    month = row[6]
                    day = row[7]
                    rhu= row[8]
                    lng = float(row[1])
                    lat = float(row[2])
                    # create the point geometry
                    output_shp.point(lng, lat)
                    # add attribute data
                    output_shp.record(station,lng, lat, height,year,month,day,rhu)  
                    
        if files[i].split('-')[1]=='PRE':
            fnn = files[i].split('.')[0]
#             print(fnn)
            output_shp = shp.Writer(output_shpdir+ os.sep + "%s.shp" % fnn, shp.POINT, encoding='gbk') #encoding='utf-8'
            # output_shp = shp.Writer(output+ os.sep + "%s.shp" % fnn.split('.')[0], shp.POINT) #encoding='utf-8'
            # for every record there must be a corresponding geometry.
            output_shp.autoBalance = 1
            # create the field names and data type for each.you can omit fields here
            output_shp.field('station', 'F', 10, 8) # float
            output_shp.field('longitude', 'F', 10, 8) # float
            output_shp.field('latitude', 'F', 10, 8) # float
            output_shp.field('height', 'F', 10, 8) # float
            output_shp.field('Year', 'F', 10, 8) # int
            output_shp.field('Mon', 'F', 10, 8) # int
            output_shp.field('Day', 'F', 10, 8) # int            
            output_shp.field('dpre', 'F', 10, 8) # string, max-length
            output_shp.field('npre', 'F', 10, 8) # string, max-length
            output_shp.field('pre', 'F', 10, 8) # string, max-length
            # access the CSV file
            with codecs.open(output_csvdir+ os.sep + fnn + '.csv', 'rb', 'utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
            # skip the header
                next(reader, None)
                #loop through each of the rows and assign the attributes to variables
                for row in reader:
                    station = row[3]
                    height= row[4]
                    year = row[5]
                    month = row[6]
                    day = row[7]
                    dpre= row[8]
                    npre= row[9]
                    pre= row[10]
                    lng = float(row[1])
                    lat = float(row[2])
                    # create the point geometry
                    output_shp.point(lng, lat)
                    # add attribute data
                    output_shp.record(station,lng, lat, height,year,month,day,dpre,npre,pre)  

        if files[i].split('-')[1]=='SSD':
            fnn = files[i].split('.')[0]
#             print(fnn)
            output_shp = shp.Writer(output_shpdir+ os.sep + "%s.shp" % fnn, shp.POINT, encoding='gbk') #encoding='utf-8'
            # output_shp = shp.Writer(output+ os.sep + "%s.shp" % fnn.split('.')[0], shp.POINT) #encoding='utf-8'
            # for every record there must be a corresponding geometry.
            output_shp.autoBalance = 1
            # create the field names and data type for each.you can omit fields here
            output_shp.field('station', 'F', 10, 8) # float
            output_shp.field('longitude', 'F', 10, 8) # float
            output_shp.field('latitude', 'F', 10, 8) # float
            output_shp.field('height', 'F', 10, 8) # float
            output_shp.field('Year', 'F', 10, 8) # int
            output_shp.field('Mon', 'F', 10, 8) # int
            output_shp.field('Day', 'F', 10, 8) # int            
            output_shp.field('ssd', 'F', 10, 8) # string, max-length
            # access the CSV file
            with codecs.open(output_csvdir+ os.sep + fnn + '.csv', 'rb', 'utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
            # skip the header
                next(reader, None)
                #loop through each of the rows and assign the attributes to variables
                for row in reader:
                    station = row[3]
                    height= row[4]
                    year = row[5]
                    month = row[6]
                    day = row[7]
                    ssd= row[8]
                    lng = float(row[1])
                    lat = float(row[2])
                    # create the point geometry
                    output_shp.point(lng, lat)
                    # add attribute data
                    output_shp.record(station,lng, lat, height,year,month,day,ssd)  
print('转矢量完成!')
```

## 1.4 定义投影


```python
# 定义投影
# jupyter notebook中无法写入，需要在pycharm中运行
proj = osr.SpatialReference() 
proj.ImportFromEPSG(4326) # 4326-GCS_WGS_1984; 4490- GCS_China_Geodetic_Coordinate_System_2000
wkt = proj.ExportToWkt()
for root, dirs, files in os.walk(output_shpdir):
    print(root)
for i in range(len(files)):
    if files[i].split('.')[1] == 'shp':
        # 写入投影
        print(files[i])
        f = open((root+os.sep+files[i]).replace(".shp", ".prj"), 'w') 
        f.write(wkt)#写入投影信息
        f.close()#关闭操作流
```
