# -*-coding:utf-8-*-
'''
基于分类的推荐
'''
from numpy import *;  # 导入numpy的库函数
import numpy as np;
import MySQLdb

class ItemBasedCF:
    def __init__(self, id):
        self.id = id
    def cos_dis(vector1, vector2):
        # 计算余弦距离
        a1 = np.array(vector1, dtype=int)
        a2 = np.array(vector2, dtype=int)
        a3 = multiply(a1, a2);
        return sum(a3) * 1.0 / (sqrt(sum(a1)) + sqrt(sum(a2)))


    def get_k_neighbor(k, vector1):
        nearest_books = dict()
        # 计算得到物品id,距离
        # get data from mysql
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='blog', port=3306)
            cur = conn.cursor()
            cur.execute('select * from book_tag')
            results = cur.fetchall()
            all_booktag = dict()
            for row in results:
                book_id = row[1]
                book_tag = row[2:7]
                # changge book_tag to 01 array
                bt = [0 for i in range(0, 15)]
                for i in range(0, 5):
                    bt[book_tag[i] - 1] = 1
                cur_dis = cos_dis(vector1, bt)
                nearest_books[book_id] = cur_dis

            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        # sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        return sorted(nearest_books.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[0:k]


    def get_tag_vec(id):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='blog', port=3306)
            cur = conn.cursor()
            sql = 'select * from book_tag where book_id=' + bytes(id)
            cur.execute(sql)
            cur_booktag = cur.fetchone()[2:7]
            # print data
            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        bt = [0 for i in range(0, 15)]
        for i in range(0, 5):
            bt[cur_booktag[i] - 1] = 1
        return bt


    print get_k_neighbor(3, get_tag_vec(1))


