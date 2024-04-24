## 遇到的问题
2. excel是iqy形式的程序没法读iqy
2. matweb网站直接wget， curl材料网址，获得不到文件，需要模仿浏览器进行下载
3. 解决办法：在浏览器中可以使用matguid获得网页下材料的网址，根据html元素读取材料信息，保存成csv文件

## todo
- 方案一：
1. selenium 中download iqy 需要登录，尝试使用cookie是否能够解决该问题。
2. **下载的数据集非常的多，所以需要自动下载。**
3. 网页那么多，如果模拟浏览器一个个点击，运行非常的耗时，耗电脑，而且不是很稳定。
- 方案二：
1. requests中save content,but block by matweb.

- 方案二：
1. 使用pandas直接扣网页中的数据，然后保存为csv文件。

## 样例
start_url=['http://www.matweb.com/search/QuickText.aspx?SearchText=AA2618']

得到
https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5e92a1ae7f24e1b918bf4e65dbc7e52
https://www.matweb.com/search/DataSheet.aspx?MatGUID=f6d0bebbfc7248838243b7fa141431ba
https://www.matweb.com/search/DataSheet.aspx?MatGUID=71708ff2737d4932be5abc695927fc12