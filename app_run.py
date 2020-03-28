from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('mym7y5Iv6WO0rqwerT0HhwobgaQfwmrRWHihcqkeVz22rj8jtjvpEBTchx3pwrk5Ttk0WNMrwYJpM8304omHyvf2ZMrdwis+OB4iH9+nUx8MeQmMiiviVqZGutPng3S7RKKT4M0dNzE0BszyxOG+BQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0e5e4f007110e8d162e8b6dcc662c603')

def dcard():
    topics = []
    url = "https://www.dcard.tw/f"
    r = requests.get(url)
    alright = False
    # print(r)
    if (r.status_code==200):
        # print("NORMAL\n")
        alright = True
    else:
        # print("Something Fishy\n")
        topics.append("Something Fishy")

    if alright == True:
        soup = BeautifulSoup(r.text,'html.parser')
        # filter_1 = soup.find_all("article")
        filter_2 = soup.find_all("a",class_ = 'sc-1v1d5rx-4 cJzlcl')
    #     print(filter_2)
        for c in filter_2:
            if (c.text != ''):
                # print(c.text)
                topics.append(c.text)
    return topics

def scrape_item_page(url):

    headers = {
        'user-Agent': 'Googlebot',
        'From': 'YOUR EMAIL ADDRESS'
    }

    info = []
    r_item_page = requests.get(url,headers=headers)
    soup_item_page = BeautifulSoup(r_item_page.text,'html.parser')
    contents_item_page = soup_item_page.find_all("div",class_ = 'qaNIZv')
    price_item_page = soup_item_page.find_all("div",class_ = '_3n5NQx')
    text = ""
    for c_ ,p_ in zip(contents_item_page,price_item_page):
        text = str(c_.contents[0].text)+" "+str(p_.contents[0])

    return text

def shopeeU(keywords):
    if keywords == 'A':
        key = '制服'
    elif keywords == 'B':
        key = '校服'
    elif keywords == 'C':
        key = '運動服'
    elif keywords == 'D':
        key = '高中制服'
    elif keywords == 'E':
        key = '國中制服'
    elif keywords == 'F':
        key = '二手制服'
    elif keywords == 'G':
        key = '女中'
    else:
        key = keywords

    url = f'https://shopee.tw/search?keyword={key}&page=0&sortBy=ctime&usedItem=true'

    print("this is U_url : "+ url)
    print("this is U_keyword : "+ key)
    
    headers = {
        'user-Agent': 'Googlebot',
        'From': 'YOUR EMAIL ADDRESS'
    }
    
    r = requests.get(url,headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    contents = soup.find_all("div",class_ = '_1NoI8_ _16BAGk')
    prices = soup.find_all("span", class_='_341bF0')
    all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
    links = [i.find('a').get('href') for i in all_items]
    all_items = []
    items_url = []
    for l in (links):
        text = 'https://shopee.tw/'+l
        items_url.append(text)

    print("itmes_url len = "+ str(len(items_url)))

    if (len(items_url)>0):
        num_items = 0
        x = 0
        while(num_items<=10):
            item_info = scrape_item_page(items_url[x])
            x+=1
            if item_info =='':
                pass
            else:
                print(item_info)
                all_items.append(item_info)
                num_items+=1
    else:
        all_items.append('ERROR')

    return all_items

def shopeeN(keywords):

    url = f'https://shopee.tw/search?keyword={keywords}&page=0&sortBy=sales'

    print("this is N_url : "+ url)
    print("this is N_keyword : "+ keywords)
    
    headers = {
        'user-Agent': 'Googlebot',
        'From': 'YOUR EMAIL ADDRESS'
    }
    
    r = requests.get(url,headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    contents = soup.find_all("div",class_ = '_1NoI8_ _16BAGk')
    prices = soup.find_all("span", class_='_341bF0')
    all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
    links = [i.find('a').get('href') for i in all_items]
    all_items = []
    items_url = []
    for l in (links):
        text = 'https://shopee.tw/'+l
        items_url.append(text)

    print("itmes_url len = "+ str(len(items_url)))

    if (len(items_url)>0):
        num_items = 0
        x = 0
        while(num_items<=10):
            item_info = scrape_item_page(items_url[x])
            x+=1
            if item_info =='':
                pass
            else:
                print(item_info)
                all_items.append(item_info)
                num_items+=1
    else:
        all_items.append('ERROR') 
    

    return all_items

def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print(type(signature))

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_key_word = event.message.text

    if input_key_word == "dcard":
        topics = dcard()
        hot_topics = ""
        for x in range(10):
            cvt_d = listToString(topics[x].contents)
            hot_topics = hot_topics+"\n"+cvt_d
        print(hot_topics)
        user_input = TextSendMessage(text=hot_topics)
    else:
        if input_key_word[0:7] == "shopeeU":
            search_ = input_key_word[7:]
            search = []
            for x in search_:
                search = search_           
            all_items = ""
            all_items_ = []
            all_items_ = shopeeU(search)
            for x in range (len(all_items_)):
                all_items = all_items + (all_items_[x]+'\n')
            user_input = TextSendMessage(text = all_items)
        elif input_key_word[0:7] == "shopee ":
            search_ = input_key_word[7:]
            search = []
            for x in search_:
                search = search_           
            all_items = ""
            all_items_ = []
            all_items_ = shopeeN(search)
            for x in range (len(all_items_)):
                all_items = all_items + (all_items_[x]+'\n')
            user_input = TextSendMessage(text = all_items)
        else:
            user_input = TextSendMessage(text=event.message.text)

    line_bot_api.reply_message(event.reply_token,user_input)

    # input_key_word = ""

if __name__ == "__main__":
    app.run()