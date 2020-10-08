import warnings
import nltk
from flask import Flask, render_template, request, Blueprint
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


# random greeting
def bot_response(user_input, static=None):
    # user_input= "chronic kidney disease"
    # sentence_list.append(user_input)
    bot_response = ''
    # cm = CountVectorizer().fit_transform(sentence_list)
    # similarity_scores = cosine_similarity(cm[-1], cm)
    # similarity_scores_list = similarity_scores.flatten()
    # index = index_sort(similarity_scores_list)
    # index = index[1:]
    response_flag = 0
    greetings = ['hi', 'hello','hay']
    # if user_input in greetings:
    #     bot_response=bot_response+' '+'Hello !!!!!!!   Enter ur question'
    #     response_flag = 1
    names = ['chronic kidney disease', 'brain tumor','fever']
    names.append(user_input)
    cn = CountVectorizer().fit_transform(names)
    similarity_scores_names = cosine_similarity(cn[-1], cn)
    similarity_scores_list = similarity_scores_names.flatten()
    index1 = index_sort(similarity_scores_list)
    index1 = index1[1:]
    max=0.0
    name=''
    url=''
    for i in range(len(index1)):
        if similarity_scores_list[index1[i]] > max:
            name=names[index1[i]]
            max=similarity_scores_list[index1[i]]
    disease = 0
    # if user_input in names:
    #     name= user_input

    if name.lower() == 'chronic kidney disease':
        url = 'https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521'
    elif name.lower() == 'brain tumor':
        url = 'https://www.mayoclinic.org/diseases-conditions/brain-tumor/symptoms-causes/syc-20350084#:~:text=A%20brain%20tumor%20is%20a,tumors%20are%20cancerous%20(malignant).'
        # get article
    elif name.lower() == 'fever':
        url='https://www.mayoclinic.org/diseases-conditions/fever/symptoms-causes/syc-20352759'
    if url!='':
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        corpus = article.text
        # tokenization
        text = corpus
        sentence_list = nltk.sent_tokenize(text)
        sentence_list.append(user_input)
        bot_response = ''
        cm = CountVectorizer().fit_transform(sentence_list)
        similarity_scores = cosine_similarity(cm[-1], cm)
        similarity_scores_list = similarity_scores.flatten()
        index = index_sort(similarity_scores_list)
        index = index[1:]
        j=0
        for i in range(len(index)):
            if similarity_scores_list[index[i]] > 0.0:
                bot_response = bot_response + ' ' + sentence_list[index[i]]
                response_flag = 1
                j += 1
                if j > 2:
                    sentence_list.remove(user_input)
                    break
    if response_flag == 0:
        bot_response = bot_response + ' ' + 'i did not understand'


    return bot_response



disease = Blueprint("disease", __name__,static_folder="static",template_folder="templates/disease")


@disease.route("/disease")
def home():
    return render_template("index1.html")
@disease.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot_response(userText))

