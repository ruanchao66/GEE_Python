# Python版GEE学习笔记02 | 在python中配置GEE（geemap）

这里推荐安装吴秋生老师的geemap，其中内置了ee（gee），所以只要安装geemap包，就可以直接使用python gee。

详细介绍可参考吴秋生老师的geemap官网：https://geemap.org/installation/

## 1.在python中配置GEE

### 1.1 conda创建新环境

#### 第一步：创建

conda create --name 自定义环境名 python=python版本

![gee图1](https://user-images.githubusercontent.com/61082571/231941896-3dc2de76-6335-4ed7-a9ad-6b6e6c42b089.png)

备注：

若想要在创建环境同时安装python的一些包：
conda create -n 自定义环境名 python=python版本 numpy pandas

若想在别人虚拟环境的基础上创建自己的环境：
conda create --name <自定义环境名> --clone <别人环境名>

#### 第二步： 激活

conda activate 自定义环境名

![gee图2](https://user-images.githubusercontent.com/61082571/231941908-63d54326-b3aa-4645-bd69-8126310aefcf.png)

## 1.2 在jupyter notebook中添加conda环境

以下Geo为环境名，可将其修改为自己所要添加的conda环境。

#### 第一步：安装ipykernel

conda install ipykernel

![gee图3](https://user-images.githubusercontent.com/61082571/231941918-7ac6a31e-dcc3-49ce-b77d-c46410649785.png)

#### 第二步：将环境写入notebook的kernel中

python -m ipykernel install --user --name Geo --display-name “Geo”

![gee图4](https://user-images.githubusercontent.com/61082571/231941927-a24439df-01e3-41af-aefd-7c2ffaa17cff.png)

#### 第三步：打开jupyter notebook

jupyter notebook

![gee图5](https://user-images.githubusercontent.com/61082571/231941934-4a022515-16af-457a-81a4-47241e4e47c0.png)

### 1.3 在Jupyter notebook选择conda环境

![gee图6](https://user-images.githubusercontent.com/61082571/231941943-24bfb1c5-baae-49f7-bb46-5dcc2721ba80.png)

### 1.4 配置GEE

#### 第一步：安装GEE所需库（geemap）

备注：这里推荐安装吴秋生老师的geemap，内置了ee（gee），所以只要安装geemap包就好。

详细介绍可参考吴秋生老师的geemap官网：https://geemap.org/installation/ 

安装方法：

【1】conda install -c conda-forge mamba

![gee图7](https://user-images.githubusercontent.com/61082571/231941950-9cb1bf4d-cc8a-47e1-9557-a0ac489c035a.png)

【2】mamba install -c conda-forge geemap pygis

![gee图8](https://user-images.githubusercontent.com/61082571/231941959-9210cd48-ce51-43f8-86f0-9b25816b2e7b.png)


#### 第二步：测试本地环境是否搭建完成


```python
#使用import命令加载gee库，并设置网络代理端口
import ee
import geemap
import os
# Map=geemap.Map()
# Map
```


```python
#设置网络代理端口,7890为自己的端口号
#方法一：
geemap.set_proxy(port=7890)

#方法二：
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
```


```python
#geemap可以在jupyter中加载地图，如果出现如下地图界面，则说明成功了
Map=geemap.Map()
Map
```

![gee图9](https://user-images.githubusercontent.com/61082571/231941974-711dc464-e44f-423c-aa6e-7d725cae2a67.png)

备注：如果运行Map后，程序没有报错，但无法加载出地图，则需要在创建的环境中运行下面两行代码并重启

jupyter nbextension install --py ipyleaflet

![gee图10](https://user-images.githubusercontent.com/61082571/231941979-2f7033a5-1759-4581-b255-8b9aaf257c7e.png)

jupyter nbextension enable --py ipyleaflet

![gee图11](https://user-images.githubusercontent.com/61082571/231941986-5963b244-ccd4-4313-b7f4-3409410cc55f.png)
