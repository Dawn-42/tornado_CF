# tornado_CF
 
### 小型推荐系统 ###

* 框架：Tornado
* 数据库：MySql


* 需要的包
    * Tornado,MySQLdb,numpy

* 效果图
    * 书籍列表页 
        ![效果图](http://note.youdao.com/yws/public/resource/370245d221afce93158358fd95ca3e9c/xmlnote/WEBRESOURCE21783440fcb522250f6c31cd7854b9cb/15483)
    * 详情页
        ![详情](http://note.youdao.com/yws/public/resource/370245d221afce93158358fd95ca3e9c/xmlnote/WEBRESOURCEf7151c0465b266316b08498d46085bac/15487)

* 数据库说明：
    * books
        * 主要包括书籍标题以及描述 
![Book](http://note.youdao.com/yws/public/resource/370245d221afce93158358fd95ca3e9c/xmlnote/WEBRESOURCE388d0f681e3f3d4ffa44321587e0b007/15463)

    * book_tag
        * 主要包括书籍id以及对应的标签
![Book_tag](http://note.youdao.com/yws/public/resource/370245d221afce93158358fd95ca3e9c/xmlnote/WEBRESOURCE09689cc956f43ffaf158d569ab83bf00/15473)

* 算法说明
    * 基于物品标签进行分类 
        * 书籍标签数据为随机生成的1-15的整数，一共有30种不同的标签
        * 根据书籍的标签比较书籍之间的相似度
        * 当进入书籍详情页面的时候选取相似度最高的5本书进行推荐

* 效果举例
    * 对于编号43的书籍，它的标签编号包括：{'tag_5': 13L, 'tag_1': 6L, 'tag_2': 11L, 'tag_3': 0L, 'tag_4': 14L} 
    * 推荐的书籍包括：
        * (book_id,相似度得分) 
        * (135, 0.94427190999915878),
        * (48, 0.89442719099991586),
        * (88, 0.89442719099991586),
        * (98, 0.89442719099991586),
        * (244, 0.89442719099991586)  
    * 编号135的书籍，标签包括：
        * {'tag_5': 13L, 'book_id': 135L, 'tag_1': 15L, 'tag_2': 14L, 'tag_3': 6L, 'tag_4': 15L, 'id': 135L}
