from flask import Flask, request, abort
from random import randint

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests
import re
import requests, json

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('AisO8Gpl/tiIuYoM5r/fQixdYKstIuP1xJH4lsrAxfX6d46ESGwQyC5c1OXypTjNLTjfxtOIv2tjclIJHQWCktyWr9xydHMU32Qk8q9eIguProRzi9NKoBQPhyTtYUKa2ykCue7iP9tqztRVIXyVcQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a61ddb69c1ec8893792072096bd7ef02')
#===========[ NOTE SAVER ]=======================
notes = {}

# #REQUEST DATA ADMIN RPL
def cariadmin(nrp):
    URLadmin = "http://www.aditmasih.tk/api_yemima/show.php?nrp=" + nrp
    r = requests.get(URLadmin)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nrp = data['api_yemima'][0]['nrp']
        nama = data['api_yemima'][0]['nama']
        alamat = data['api_yemima'][0]['alamat']

        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "nama : "+nama+"\nrp : "+nrp+"\nalamat : "+alamat
        return data
        # return all_data

    elif(flag == "0"):
        return err

#INPUT DATA ADMIN RPL buat di app.py
def inputadmin(nrp, nama, alamat):
    r = requests.post("http://www.aditmasih.tk/api_yemima/insert.php", data={'nrp': nrp, 'nama': nama, 'alamat': alamat})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nama+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def alladmin():
    r = requests.post("http://www.aditmasih.tk/api_yemima/all.php")
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['api_yemima'])):
            nrp = data['api_yemima'][int(i)][0]
            nama = data['api_yemima'][int(i)][2]
            alamat = data['api_yemima'][int(i)][4]
            hasil=hasil+str(i+1)
            hasil=hasil+".\nnrp : "
            hasil=hasil+nrp
            hasil=hasil+"\nnama : "
            hasil=hasil+nama
            hasil=hasil+"\nalamat : "
            hasil=hasil+alamat
            hasil=hasil+"\n"
        return hasil
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

# #DELETE DATA ADMIN RPL
def hapusadmin(nrp):
    r = requests.post("http://www.aditmasih.tk/api_yemima/delete.php", data={'nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def updateadmin(nrpLama,nrp,nama,alamat):
    URLadmin = "http://www.aditmasih.tk/api_yemima/show.php?nrp=" + nrpLama
    r = requests.get(URLadmin)
    data = r.json()
    err = "data tidak ditemukan"
    nrp_lama=nrpLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api_yemima/update.php", data={'nrp': nrp, 'nama': nama, 'alamat': alamat, 'nrp_lama':nrp_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+nrp_lama+'berhasil diupdate\n'
        elif(flag == "0"):
            return 'Data gagal diupdate\n'

    elif(flag == "0"):
        return err

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)
   
    data=text.split('-')
    if(data[0]=='add'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputadmin(data[1],data[2],data[3])))
    elif(data[0]=='show'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cariadmin(data[1])))
    elif(data[0]=='delete'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusadmin(data[1])))
    elif(data[0]=='replace'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updateadmin(data[1],data[2],data[3],data[4])))
    elif(data[0]=='all'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=alladmin()))
    elif(data[0]=='/menu'):
        menu = "1. show-[nrp]\n2. add-[nrp]-[nama]-[alamat]\n3. delete-[nrp]\n4. replace-[nrp lama]-[nrp baru]-[nama baru]-[alamat baru]\n5. all "
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))
    else
        printf 'error\n'

# def handle_message(event):
#     text = event.message.text #simplify for receove message
#     sender = event.source.user_id #get usesenderr_id
#     gid = event.source.sender_id #get group_id
#     profile = line_bot_api.get_profile(sender)
    
#     #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Kamu jahat '+text))
#     #if text=="mail":
#         #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Kamu jahat mail'))
#     if text=="kana" or text=="hans":
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Kamu tega, '+text))
#     #a=(randint(0, 9))
#     #if a%2:
#         #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Iya'))
#     #else:
#         #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Tidak'))

#     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Halo '+profile.display_name+'\n'+text+' juga :)'))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
