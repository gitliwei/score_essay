import random

from libsvm.python.svmutil import *
from libsvm.python.svm import *
import pymysql

def score_result(s):
    db = pymysql.connect("localhost", "liwei", "0000", "articlescore", charset='utf8')
    cursor = db.cursor()

    pragraph = s.count("\n")+1
    pragraph = pragraph/10
    score = "优"
    count = len(s)
    count = count/1000
    good = random.randint(0,5)

    dictum = 0
    name = 0
    poem = 0
    idiom = 0

    sql = '''SELECT * FROM dictum;'''
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[1] in s:
                dictum = dictum +1
    except Exception as e:
        print(str(e))

    sql = '''SELECT * FROM famous_name;'''
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[1] in s:
                name = name +1
    except Exception as e:
        print(str(e))

    sql = '''SELECT * FROM poem;'''
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[1] in s:
                poem = poem +1
    except Exception as e:
        print(str(e))

    sql = '''SELECT * FROM idiom;'''
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[1] in s:
                idiom = idiom +1
    except Exception as e:
        print(str(e))
    db.close()

    y, x = svm_read_problem('lele_spider/train.txt')
    # yt, xt = svm_read_problem('lele_spider/test.txt')
    # yt, xt = svm_read_problem('lele_spider/train.txt')
    model = svm_train(y, x )

    # f = open('input_essay.txt', 'w', encoding="utf-8")
    # f.write("1")
    # f.write(" 1:")
    # f.write(str(pragraph))
    # f.write(" 2:")
    # f.write(str(count))
    # f.write(" 3:")
    # f.write(str(name))
    # f.write(" 4:")
    # f.write(str(poem))
    # f.write(" 5:")
    # f.write(str(dictum))
    # f.write(" 6:")
    # f.write(str(idiom))
    # f.write(" 7:")
    # f.write(str(good))
    # f.write('\n')
    #
    # print(pragraph,count,score,dictum,name,poem,idiom,good)
    # f.close()
    #
    # yt, xt = svm_read_problem('input_essay.txt')
    # p_label, p_acc, p_val = svm_predict(yt[:], xt[:], model)
    #
    # print(p_acc[1])
    # print(1-p_acc[1])
    #
    # f = open('input_essay.txt', 'w', encoding="utf-8")
    # f.write("2")
    # f.write(" 1:")
    # f.write(str(pragraph))
    # f.write(" 2:")
    # f.write(str(count))
    # f.write(" 3:")
    # f.write(str(name))
    # f.write(" 4:")
    # f.write(str(poem))
    # f.write(" 5:")
    # f.write(str(dictum))
    # f.write(" 6:")
    # f.write(str(idiom))
    # f.write(" 7:")
    # f.write(str(good))
    # f.write('\n')
    #
    # print(pragraph,count,score,dictum,name,poem,idiom,good)
    # f.close()
    #
    # yt, xt = svm_read_problem('input_essay.txt')
    # p_label, p_acc, p_val = svm_predict(yt[:], xt[:], model)
    #
    # print(p_acc[1])
    # print(1-p_acc[1])

    flag = 0

    f = open('input_essay.txt', 'w', encoding="utf-8")
    f.write("1")
    f.write(" 1:")
    f.write(str(pragraph))
    f.write(" 2:")
    f.write(str(count))
    f.write(" 3:")
    f.write(str(name))
    f.write(" 4:")
    f.write(str(poem))
    f.write(" 5:")
    f.write(str(dictum))
    f.write(" 6:")
    f.write(str(idiom))
    f.write(" 7:")
    f.write(str(good))

    f.write('\n')

    print(pragraph,count,score,dictum,name,poem,idiom,good)
    f.close()

    yt, xt = svm_read_problem('input_essay.txt')
    p_label, p_acc1, p_val = svm_predict(yt[:], xt[:], model)

    if p_acc1[1]==0:
        score = "优"
        flag = 1

    f = open('input_essay.txt', 'w', encoding="utf-8")
    f.write("2")
    f.write(" 1:")
    f.write(str(pragraph))
    f.write(" 2:")
    f.write(str(count))
    f.write(" 3:")
    f.write(str(name))
    f.write(" 4:")
    f.write(str(poem))
    f.write(" 5:")
    f.write(str(dictum))
    f.write(" 6:")
    f.write(str(idiom))
    f.write(" 7:")
    f.write(str(good))

    f.write('\n')

    print(pragraph,count,score,dictum,name,poem,idiom,good)
    f.close()

    yt, xt = svm_read_problem('input_essay.txt')
    p_label, p_acc1, p_val = svm_predict(yt[:], xt[:], model)

    if p_acc1[1]==0:
        score = "良"
        flag = 1

    if flag == 0:
        score = "差"

    res = {'score':score,'pragrapg':pragraph,'count':count,'poem':poem,'dictum':dictum,'idiom':idiom,'name':name}
    return  res
