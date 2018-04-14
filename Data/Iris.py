#1 
from sklearn.datasets import load_iris


dataset = load_iris()
x = dataset.data
y = dataset.target
#print(dataset.DESCR)


#2
import numpy as np
#axis=0 压缩行，求各列的平均数，返回1*m； axis=1则相反；默认求所有值的平均数
attribute_means = x.mean(axis=0)
x_d = np.array(x>=attribute_means,dtype='int')


#3 OneR-1
from collections import defaultdict
from operator import  itemgetter
 # params依次：数据集；分类类别（数组）（诸如男，女）；选好的特征值索引（特征值列表排序后的索引）；给定特征值（如，长度宽度）
 #  训练特征值目的：[一个给定特征+值情况下]1.得到最可能（最高频）的类别以及2.得到错误率（次数）
def train_feature_value(x,classifications,feature_index,feature_value):
    #分类类别记数
    class_counts = defaultdict(int)
    #整个数据集中取每个【个体】以及【个体的类别】，若【个体的特征值】符合【给定的特征值】,【这个类别】符合条件记数+1-->即是找出所有【符合给定特征值】的类别记数情况
    for sample,classification in zip(x,classifications):
        if sample[feature_index] == feature_value:
            class_counts[classification] += 1

    #对【符合给定特征值】类别记数情况进行[降序]排序并取[最大记数]的一种情况下的【类别】
    sorted_class_counts = sorted(class_counts.items(),key=itemgetter(1),reverse = True)
    most_frequent_class = sorted_class_counts[0][0]

    #计算这条规则下的错误率 表示的是分类不适用的个体数量 这里class_value 相当于classification
    # 如果类别不是最高出现频率类别则 取出来这个类别的记数，组成列表
    incorrect_predictions = [class_count for class_value,class_count 
                             in class_counts.items()
                             if class_value != most_frequent_class]
    error = sum(incorrect_predictions)
    return most_frequent_class,error


#4 OneR-2
 #对于某项特征(feature_index)，遍历其每一个特征值(feature_value)，使用train_feature_value函数(得到最高频类别，和这个特征值出现错误的次数)
 #  定义函数把所有错误次数加起来，得到的是该特征下的总错误次数
def train_on_feature(x,classifications,feature_index):
    #set 是一个只有key的集合,同数学意义
    #返回 feature_index 所指的列，如feature_index == 1，则返回第一列所组成的数组,最后转化为集合(去重)
    feature_values = set(x[:,feature_index])
    #预测器{'特征值':类别}；errors列表
    predictors = {}
    errors = []
    for current_value in feature_values:
        most_frequent_class,error = train_feature_value(x,classifications,feature_index,current_value)
        predictors[current_value] = most_frequent_class
        errors.append(error)
    total_error = sum(errors)
    return predictors,total_error 


#5 OneR-3 -test
from sklearn.cross_validation import train_test_split
 #将数据集分成两部分训练及测试集，防止过拟合，random_state指定切分随机状况；每次切分相同随机状况，切分结果相同，值为none每次切分结果真正随机。
Xd_train, Xd_test, y_train, y_test = train_test_split(x_d,y,random_state=14)
all_predictors = {}
errors = {}
# shape 返回数组维度（降序），shape[0]最高维;矩阵则对应行[0]，列[1]
for feature_index in range(Xd_train.shape[1]):
    predictors, total_error = train_on_feature(Xd_train,y_train,feature_index)
    print()
    all_predictors[feature_index] = predictors
    errors[feature_index] = total_error
#从所有特征中 找出 [错误率]最低的特征，以此为依据作为分类唯一规则-->得到最佳特征
best_feature,best_error = sorted(errors.items(),key=itemgetter(1))[0]
#最佳特征-->最佳特征值,创建model模型
model = {'feature':best_feature,
         'predictor':all_predictors[best_feature]}
#?????????
print(model)
def predict(x_test,model):
    variable = model['feature']
    predictor = model['predictor']
    y_predicted = np.array([predictor[int(sample[variable])] for sample in x_test])
    return y_predicted

y_predicted = predict(Xd_test,model)
accuracy = np.mean(y_predicted == y_test) *100
print('The test accuracy is {:.1f}%'.format(accuracy))

#示例上
#print(all_predictors)
#{0: ({0: 0, 1: 2}, 41), 1: ({0: 1, 1: 0}, 58), 2: ({0: 0, 1: 2}, 37), 3: ({0: 0, 1: 2}, 37)}
#示例上的 all_predictors 中 得到的字典值为train_on_feature的两个值，所以在建立模型中取第一个[0]第二个是总错误率
#自己 -->缺少了错误个数
#print(all_predictors)
#{feature(long?wide?):{feature_value(how long?how wide?):class(what kind?)},(mayInclude mistakes)}
#{0: {0: 0, 1: 2}, 1: {0: 1, 1: 0}, 2: {0: 0, 1: 2}, 3: {0: 0, 1: 2}}
#https://blog.csdn.net/leafage_m/article/details/79046435