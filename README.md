# GaodeCrawler

项目链接：<https://github.com/RealIvyWong/GaodeCrawler>

## 1 实现功能

这个项目是爬取某个城市所有类别的高德 POI 数据，并写进 sqlite 数据库。

会用到你自己的高德 API key。而且目前（2019 年 5 月）高德免费 API key 的配额是每天调用量为 2000（意思就是一个 key 只能访问 2000 个页面，一个页面可能 20+ 条数据），所以注意一天不要爬取太多。

用这个代码爬取的武汉市的 POI 数据有 41w+ 条，还是比较多的了。可能一个中等城市爬个小半天左右吧。

【注】 key 要是 **Web** 服务的。

## 2 依赖环境

使用的是 Python 3.7。

无需额外的第三方库。

## 3 使用方法

**step1.** 修改 start.py 中的【自己设置区域】的三个变量 citycode（城市代码）, keypoolFile（key 池的文件），database（数据库的文件名，默认为 poi.sqlite)。

**step2.** 修改 keypool.txt 文件中的 API key（每个 key 占一行）。

**step2.** Run start.py。

> 【**如何知道想要爬取的城市的citycode**】
>
> 打开当前文件夹中的 city.json 文件，搜索你所想爬取的文件名，对应的 citycode 就能看到。
>
> 比如说 {"city":"北京市","adcode":"110000","citycode":"010"} 北京市的 citycode，就是 010。

## 4 文件说明

包含三个文件。

### start.py

爬虫本体。

### city.json

城市列表数据。

### amap_poicode.xlsx

高德直接下载获得的 poi 列表。

### amap_poicode.csv

其实就是上面这个 xlsx 文件转为的 csv 文件，因为 csv 文件对于 python 程序更友好，所以它才有存在的必要。

### keypool.txt

key 池，每个 key 一行。

## 5 爬取示例

如果开始成功运行之后，控制台输出大概是这样的。代码的原理是先按整个城市范围进行搜索，然后再按各个区县进行搜索，这样可以获得更多的数据，所以一个城市的爬取会按一个个区域来爬。

![1558873768062](https://github.com/RealIvyWong/ImageHosting/raw/master/assets/1558873768062.png)

得到的`poi.sqlite`结构是包含一个 poi 表。

表的字段有 id（序号）, poi_id（POI 自己的 id）, biz_type（好像是商业类型的数据，忘记了，一般都为空，不重要）, name（POI 名）, type（POI 类型，按分号划分大中小类三级）, address（地址）, tel（电话)，location（经纬度，目测是火星坐标系），pcode（省的代码），pname（省的名称），citycode（城市代码），cityname（城市名），adcode（区域代码），adnametext（区县名），business_area（所属商业区，不一定会有）。

![1558875092443](https://github.com/RealIvyWong/ImageHosting/raw/master/assets/1558875092443.png)

## 6 联系我

如果有什么建议或意见，欢迎联系我（huangyingjing@whu.edu.cn)或者提 issue！

## 7 请我喝杯咖啡

如果我的代码帮助到了你，欢迎你请我喝杯咖啡~

<img src="https://github.com/RealIvyWong/ImageHosting/raw/master/assets/支付宝收款码.jpg" height="30%" width="30%"> <img src="https://github.com/RealIvyWong/ImageHosting/raw/master/assets/微信收款码.png" height="30%" width="30%">