import requests
from bs4 import BeautifulSoup
from googlesearch import search
from flask import Blueprint,render_template,request
gsearch = Blueprint("gsearch", __name__,static_folder="static",template_folder="templates/search")
def bot_response(user_input):
    query = user_input
    url = ''

    response=''
    for j in search(query,tld="co.in",num=1,stop=1,pause=2):
        url= j
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    match = soup.find_all('div',class_="info-section")
    # match
    link = soup.find_all('a',limit=20)
    j = 0
    for links in link:
        if j < 10:
            response=response+' '+links.text
        else:
            break
        j+=1

    return response
@gsearch.route("/g/")
def home():
    return render_template("search.html")


@gsearch.route("/g/search")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot_response(userText))
