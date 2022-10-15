import pandas as pd
import re
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from string import punctuation
from nltk.corpus import stopwords


#Bert model
bert_model=SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
stop_words=stopwords.words('russian')
#min_similarity=0.1
min_similarity=0.75
sent_bertphrase_embeddings=[]

#убрать комментарий, когда файл с базой вопросов и ответов будет окончательно подведен под указанный в документации формат
#GoogleSheets.prepare_file("credentials.json", gtoken)

df=pd.read_csv("FAQ11.csv", sep=',', encoding='utf-8')

#предварительная обработка предложения
def cleanRequest(sentence):
    sentence=sentence.lower().strip()
    for word in stop_words:
        sentence=re.sub(word, "", sentence)
    #с удалением знаков препинания имеются некоторые проблемы
    #думаю, что корень лежит в исходном материале, если его оформить по шаблону и свести к минимуму 
    #кол-во знаков препинания, то по принципу выше можно избавиться не только от стоп-слов, но и от знаков препинания
    return sentence

#предварительная обработка нашего многомерного массива с вопросами и ответами (DataFrame)
def cleanedQuestions(df):
    cleaned_questions=[]
    for index, row in df.iterrows():
        cleaned=cleanRequest(row["questions"])
        cleaned_questions.append(cleaned)
    return cleaned_questions

#возвращает самый релевантный ответ по запросу
def autoFAQ(question_embedding, sentence_embeddings, FAQdf, sentences, min_similarity):
    max_sim=-1
    index_sim=-1
    
    #косинусовое сходство вычисляется здесь, это основной принцип алгоритма
    for index, faq_embedding in enumerate(sentence_embeddings):
        sim=cosine_similarity(faq_embedding, question_embedding)[0][0]
        #
        if(sim>max_sim):
            max_sim=sim
            index_sim=index
    #print(f"\nСхожесть: {max_sim}")
    if max_sim>min_similarity:
        #print("\nВопрос по запросу: ", FAQdf.iloc[index_sim, 0])
        #print(FAQdf.iloc[index_sim, 1])
        #print("\n")
        return FAQdf.iloc[index_sim, 1]
    else:
        print("\nЯ не справился с вопросом(")
        return "Я не нашел подходящего ответа в своей базе."

#предварительная обработка вопросов из исходного материала
cleaned_questions=cleanedQuestions(df)
for sent in cleaned_questions:
    sent_bertphrase_embeddings.append(bert_model.encode([sent]))