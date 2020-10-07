import warnings
import nltk
from flask import Flask, render_template
# import
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')
#download
nltk.download('punkt',quiet=True)
#get article
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus=article.text
#tokenization
text=corpus
sentence_list= nltk.sent_tokenize(text)
def index_sort(list_var):
  length=len(list_var)
  list_index=list(range(0,length))
  x=list_var
  for i in range(length):
    for j in range (length):
      if x[list_index[i]]>x[list_index[j]]:
        temp=list_index[i]
        list_index[i]=list_index[j]
        list_index[j]=temp

  return list_index
#random greeting
def bot_response(user_input):
  user_input= user_input.lower()
  sentence_list.append(user_input)
  bot_response=''
  cm=CountVectorizer().fit_transform(sentence_list)
  similarity_scores= cosine_similarity(cm[-1],cm)
  similarity_scores_list = similarity_scores.flatten()
  index=index_sort(similarity_scores_list)
  index=index[1:]
  response_flag=0

  j=0
  for i in range(len(index)):
    if similarity_scores_list[index[i]]>0.0:
      bot_response=bot_response+' '+sentence_list[index[i]]
      response_flag=1
      j+=1
      if j>2:
        break
  if response_flag==0:
    bot_response= bot_response+' '+'i did not understand'
  sentence_list.remove(user_input)

  return bot_response


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def main():
  exit_list=['exit','bye']
  print('hello!!!!')
  print('I am Docbot')
  print('How can i help you?')
  print('1.book apointment \n 2. get information about a disease\n enter the number')
  x=request.args.get('msg')
  if x=='1':
    while(True):
      user_input=request.args.get('msg')
      if user_input.lower() in exit_list:
        break

  elif x=='2':
      print('enter the name of disease')
      name=request.args.get('msg')
      if name.lower()=='chronic kidney disease':
        url='https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521'
      elif name.lower()=='brain tumor':
        url='https://www.mayoclinic.org/diseases-conditions/brain-tumor/symptoms-causes/syc-20350084#:~:text=A%20brain%20tumor%20is%20a,tumors%20are%20cancerous%20(malignant).'
      #get article
      article = Article(url)
      article.download()
      article.parse()
      article.nlp()
      corpus=article.text
      #tokenization
      text=corpus
      sentence_list= nltk.sent_tokenize(text)
      while(True):
        user_input=request.args.get('msg')
        if user_input.lower() in exit_list:
          break
        else:
          return str('doc bot:'+ bot_response(user_input))
if __name__ == "__main__":
    app.run(debug=True)