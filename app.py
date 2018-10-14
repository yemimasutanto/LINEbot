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
def show(nrp):
    URLadmin = "http://www.aditmasih.tk/api_yemima/show.php?nrp=" + nrp
    r = requests.get(URLadmin)
    data = r.json()
    err = "Data tidak ditemukan"

#INPUT DATA ADMIN RPL buat di app.py
def add(nrp, nama, alamat):
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
        for i in range(0,len(data['data_admin'])):
            nrp = data['data_admin'][int(i)][0]
            nama = data['data_admin'][int(i)][2]
            alamat = data['data_admin'][int(i)][4]
            print("List admin"):
            hasil=hasil+str(i+1)
            hasil=hasil+".\nNrp : "
            hasil=hasil+nrp
            hasil=hasil+"\nNama : "
            hasil=hasil+nama
            hasil=hasil+"\nAlamat : "
            hasil=hasil+alamat
            hasil=hasil+"\n"
        return hasil
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

# #DELETE DATA ADMIN RPL
def delete(nrp):
    r = requests.post("http://www.aditmasih.tk/api_yemima/delete.php", data={'nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def update(nrpLama,nrp,nama,namabaru,alamat):
    URLadmin = "http://www.aditmasih.tk/api_yemima/show.php?nrp=" + nrpLama + namabaru
    r = requests.get(URLadmin)
    data = r.json()
    err = "data tidak ditemukan"
    nrp_lama=nrpLama
    nama_baru=namabaru
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api_yemima/update.php", data={'nrp': nrp, 'nama': nama, 'namabaru':namabaru, 'alamat': alamat, 'nrp_lama':nrp_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+nrp_lama+' berhasil diupdate\n'
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
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=add(data[1],data[2],data[3])))
    elif(data[0]=='show'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=show(data[1])))
    elif(data[0]=='delete'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=delete(data[1])))
    elif(data[0]=='replace'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=update(data[1],data[2],data[3],data[4])))
    elif(data[0]=='all'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=alladmin()))
    elif(data[0]=='/menu'):
        menu = "1. show-[nrp]\n2. add-[nrp]-[nama]-[alamat]\n3. delete-[nrp]\n4. replace-[nrp lama]-[nrp baru]-[nama baru]-[alamat baru]\n5. all admin "
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
