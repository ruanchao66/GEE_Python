# Python版GEE学习笔记01 | 在python中配置GEE（ee）

## 1.在python中配置GEE

### 1.1 conda创建新环境

#### 第一步：创建

conda create --name 自定义环境名 python=python版本

![ee图1](https://user-images.githubusercontent.com/61082571/231941471-b81104ac-07b4-4c07-9586-c341343c385b.png)

备注：

若想要在创建环境同时安装python的一些包：
conda create -n 自定义环境名 python=python版本 numpy pandas

若想在别人虚拟环境的基础上创建自己的环境：
conda create --name <自定义环境名> --clone <别人环境名>

#### 第二步： 激活

conda activate 自定义环境名

![ee图2](https://user-images.githubusercontent.com/61082571/231941513-24e2dea2-e968-4336-b47f-113cb8821712.png)

### 1.2 配置GEE

#### 第一步：安装GEE所需库（ee）

【1】配置代理服务器

set http_proxy=http://127.0.0.1:7890

set https_proxy=http://127.0.0.1:7890

![ee图3](https://user-images.githubusercontent.com/61082571/231941528-32621548-5b99-4d25-ab61-aceec0ad2771.png)

备注：因为Google服务器在国外，因此需要配置代理服务器才能访问。

打开cmd，按照代理软件的不同，输入不同的端口，本机端口为7890（代码为临时性，关掉CMD就失效了，下一次需要继续输入才能让cmd继续代理）。

【2】安装Google的 python API的客户端，命令如下

pip install google-api-python-client

备注：推荐使用 pip install google-api-python-client -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

![ee图4](https://user-images.githubusercontent.com/61082571/231941539-feef8ada-504e-40dd-be53-699da82e5051.png)

【3】安装鉴权验证依赖库，输入下面命令

pip install pyCrypto

备注：pyCrypto很早以前就已经不再更新，安装pycrypto时各种报错，pycryptodome可以完美替代，推荐使用！

pip install pycryptodome -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

![ee图5](https://user-images.githubusercontent.com/61082571/231941558-3e0cb61e-3dc2-4ede-88c2-9d73173acc55.png)

【4】安装GEE的python库

pip install earthengine-api

![ee图6](https://user-images.githubusercontent.com/61082571/231941575-fdc083e2-5a52-4835-9732-f9e696f8c358.png)

备注：推荐使用 pip install earthengine-api -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

pip install --upgrade oauth2client

![ee图7](https://user-images.githubusercontent.com/61082571/231941588-a988f8d0-2878-4282-9f1a-048904688595.png)

备注：推荐使用 pip install --upgrade oauth2client -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

【5】验证我们的GEE账户

earthengine authenticate

![ee图8](https://user-images.githubusercontent.com/61082571/231941607-579b97f5-e8f1-4473-bca1-15c5173b8f4d.png)

#### 第二步：测试本地环境是否搭建完成


```python
#导入gee库
import ee
import os
#设置网络代理端口,7890为自己的端口号
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
#验证账号
# ee.Authenticate()
#初始化
ee.Initialize()
image1 = ee.Image('srtm90_v4')
path = image1.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
})
# 获取下载地址
print(path)
```

顺利得到下载地址，则表示配置成功

![ee图9](https://user-images.githubusercontent.com/61082571/231941626-db27b28c-4c86-47e5-86e6-1e4f03886bda.png)
