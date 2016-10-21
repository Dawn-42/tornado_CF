# -*-coding:utf-8-*-
'''
基于分类的推荐
'''

import MySQLdb
import compute_distance

class ItemBasedCF:
    book_id = ''
    def __init__(self, bi):
        self.book_id = bi
        # self.book_tags = self.get_tag_vec(bi)
        # self.rec_books = self.get_k_neighbor(5,self.book_tags)

    def get_k_neighbor(self,k, vector1):
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
                cur_dis = compute_distance.cos_distance(vector1, bt)

                # print cur_dis
                nearest_books[book_id] = cur_dis

            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        # sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        return sorted(nearest_books.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[1:k+1]

    def get_tag_vec(self,book_id):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='blog', port=3306)
            cur = conn.cursor()

            sql = 'select * from book_tag where book_id='+str(book_id)
            # print sql
            cur.execute(sql)
            cur_book_tag = cur.fetchone()[2:7]
            # print data
            cur.close()
            conn.close()
            bt = [0 for i in range(0, 15)]
            for i in range(0, 5):
                bt[cur_book_tag[i] - 1] = 1
            return bt
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
