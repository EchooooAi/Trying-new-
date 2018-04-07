from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

#生成词云
def create_word_cloud(filename):
    text = open('{}.txt'.format(filename),encoding ='utf-8').read()
    #结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    #设置词云
    wc = WordCloud(
        # background
        background_color='white',
        # 最大显示词云数
        max_words=2000,
        #设置字体，在电脑中一般路径
        font_path="C:\Windows\Fonts\simfang.ttf",
        height=1200,
        width=1600,
        # 设置字体最大值
        max_font_size=100,
        #设置多少种随机生成状态，即多少种配色方案
        random_state=30,
        )

    myword = wc.generate(wl) #生成词云
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file("py_book1.png") #保存词云

if __name__ == '__main__':
    create_word_cloud('qq_word')