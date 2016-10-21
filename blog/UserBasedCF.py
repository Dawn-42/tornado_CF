# -*-coding:utf-8-*-
import MySQLdb
from math import sqrt

users_score_item = {}

# 获取数据
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='blog', port=3306)
    cur = conn.cursor()
    cur.execute('select * from user_comment')
    results = cur.fetchall()
    all_booktag = dict()
    for row in results:
        if row[1] not in users_score_item:
            users_score_item[row[1]] = {}
        # 读取数据：获取用户评价过的所有物品分数  {用户：{物品：评分}}
        users_score_item[row[1]][row[3]] = int(row[2])
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

class recommender:
    # 推荐 n 本书
    def __init__(self, data, k=5, n=5):
        self.k = k
        self.n = n
        self.fn = self.pearson
        self.data = data

    # 皮尔逊相关系数，计算相关性
    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0  # 相同书评论分数之和
        sum_y = 0
        sum_x2 = 0  # 平方和
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1  # 统计相同的选择个数
                x = rating1[key]  # 物品得分
                y = rating2[key]
                sum_xy += x * y  # 对于相同的选择计算得分乘积的和
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            # 此时分母为0（即两个用户没有一本书相同，相关度为0）
            return 0
        den = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if den == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / den

    def get_k_neighbor(self, username):
        # 计算获得相似的用户
        distances = []
        for instance in self.data:  # 对于每个用户
            if instance != username:  # 遍历用户还未结束的时候
                distance = self.fn(self.data[username], self.data[instance])  # 计算用户间的相关系数
                distances.append((instance, distance))
        # distance 中保存所有用户之间的相关程度  （用户名，相关得分）
        distances.sort(key=lambda cur_bookTuple: cur_bookTuple[1], reverse=True)
        return distances

    def recommend(self, users_score_item):
        recommendations = {}  # book:score
        # 计算出user与所有其他用户的相似度，返回一个list
        nearest = self.get_k_neighbor(users_score_item)
        userRatings = self.data[users_score_item]  # 获得该用户的所有投票
        totalDistance = 0.0
        # 最近的k个用户的距离之和
        for i in range(self.k):
            totalDistance += nearest[i][1]
        if totalDistance == 0.0:  # 避免分母为0（为了将权值映射到0-1之间）
            totalDistance = 1.0

        # 将与user最相近的k个人中user没有看过的书推荐给user，按照用户间的相似度进行加权
        for i in range(self.k):
            # 第i个人的与user的相似度，转换到[0,1]之间
            weight = nearest[i][1] / totalDistance
            name = nearest[i][0]
            neighborRatings = self.data[name]
            for cur_book in neighborRatings:
                if cur_book not in userRatings:  # 如果用户没有评价过
                    if cur_book not in recommendations:
                        recommendations[cur_book] = (neighborRatings[cur_book] * weight)
                    else:
                        # 按照相似度的权值加权
                        recommendations[cur_book] = (recommendations[cur_book] + neighborRatings[cur_book] * weight)

        recommendations = list(recommendations.items())
        recommendations.sort(key=lambda cur_bookTuple: cur_bookTuple[1], reverse=True)  # 按照得分排序
        return recommendations[:self.n], nearest


def adjustrecommend(user_name):
    bookid_list = []
    rec = recommender(users_score_item)
    k, nearuser = rec.recommend(bytes(user_name))
    for i in range(len(k)):
        bookid_list.append(k[i][0])
    return bookid_list, nearuser[:7]


bookid_list, near_list = adjustrecommend("1Ws3SmK")
# print ("bookid_list:", bookid_list)
# print ("near_list:", near_list)