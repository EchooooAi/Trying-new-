import numpy as np

#1`
dataset_filename = 'D:\\chrome下载\\Pythonsjwjrm\\Pythonsjwjrm\\Python数据挖掘入门与实战\\Code_REWRITE\\Chapter 1\\affinity_dataset.txt'
X = np.loadtxt(dataset_filename)
print(X[:])
print(X[:5])
X.shape

#2
from collections import defaultdict
 #defaultdict https://www.cnblogs.com/herbert/archive/2013/01/09/2852843.html
valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurances = defaultdict(int)
n_feature = 5
 #人群中,购买了premise后，最大可能购买其他产品(conclusion)
 #对每一个人循环
for sample in X:
    #假设买了序列为premise的产品作为前提
    for premise in range(n_feature):
        #实际未购买
        if sample[premise] == 0:continue
        #实际购买了此物(sample[premise]为1)，则记录所有人购买premise次数，并寻找在买premise下是否购买其他产品（排除自己）
        num_occurances[premise] +=1
        for conclusion in range(n_feature):
            if premise == conclusion:continue
            if sample[conclusion] ==1:
               #有效规则
               valid_rules[(premise,conclusion)] +=1
            else:
                invalid_rules[(premise,conclusion)] +=1
#支持度
support = valid_rules
#置信度
confidence = defaultdict(float)
#valid_rules的key有两个值,keys()是一个将字典的键转化为列表的函数
for premise,conclusion in valid_rules.keys():
    rule =(premise,conclusion)
    #买了premise产品，又买了conclusion产品的人/买了premise产品的所有人
    confidence[rule] = valid_rules[rule]/num_occurances[premise]
features =['bread','milk','cheese','apple','banana']
def print_rule(premise,conclusion,support,confidence,features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    rule = (premise,conclusion)
    print('Rule: If a person buys {0} he will also buy {1}'.format(premise_name,conclusion_name))
    print(' - support:{0}'.format(support[rule]))
    print(' - confidence:{0:.5f}'.format(confidence[rule]))
        
#3
print_rule(2,1,support,confidence,features)

#4
#找出支持度最佳规则
from operator import itemgetter
#operator.itemgetter 函数获取的不是值，而是定义了一个函数，通过该函数作用到对象上才能获取值 https://blog.csdn.net/dongtingzhizi/article/details/12068205
#   sorted()函数 http://www.runoob.com/python/python-func-sorted.html
#   对支持度中的所有元组(premise,conclusino)排序，Key:按出现次数(相当于原support中的值),从高到低（reverse = True 降序）排序
sorted_support = sorted(support.items(),key=itemgetter(1),reverse = True)
#输出最高的5条规则
for index in range(5):
    print('Rule #{0}'.format(index+1))
    premise,conclusion = sorted_support[index][0]
    print_rule(premise,conclusion,support,confidence,features)

#5
#找出置信度最佳规则
sorted_confidence = sorted(confidence.items(),key=itemgetter(1),reverse = True)
for index in range(5):
    print('Rule #{0}'.format(index+1))
    premise,conclusion = sorted_confidence[index][0]
    print_rule(premise,conclusion,support,confidence,features)
    #失误：conclusion 与 confidence 搞混
