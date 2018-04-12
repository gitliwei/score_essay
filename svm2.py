import random

from libsvm.python.svmutil import *
from libsvm.python.svm import *
import pymysql
y, x = svm_read_problem('lele_spider/train.txt')
model = svm_train(y, x )

yt, xt = svm_read_problem('lele_spider/test.txt')
p_label, p_acc1, p_val = svm_predict(yt[:], xt[:], model)

print(p_acc1)



