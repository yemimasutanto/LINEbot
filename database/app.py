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
line_bot_api = LineBotApi('w3scpD6SKPEamgZPLSSAVZjPhP1C12+PXgXDdkrlEtCIAPoICgPdaHdlMwJV8ykiqDM9Y9i/X9UvhfGu13D2gI4J55LtiRUDnrHJ/OsJ/riStdx+rkSvrdFZCHiiCc6ekKJYZ5kXi+TSHGPaBAqiSAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('89fda4e9bbd8c74be8079f3069fe24e4')
#===========[ NOTE SAVER ]=======================
notes = {}

#REQUEST DATA MHS
def carimhs(nrp):
    URLmhs = "http://www.aditmasih.tk/api-hafid/show.php?nrp=" + nrp
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nrp = data['data_angkatan'][0]['nrp']
        nama = data['data_angkatan'][0]['nama']
        kos = data['data_angkatan'][0]['kosan']

        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "Nama : "+nama+"\nNrp : "+nrp+"\nKosan : "+kos
        return data
        # return all_data

    elif(flag == "0"):
        return err

#INPUT DATA MHS
def inputmhs(nrp, nama, kosan):
    r = requests.post("http://www.aditmasih.tk/api-hafid/insert.php", data={'nrp': nrp, 'nama': nama, 'kosan': kosan})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nama+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def allmhs():
    r = requests.post("http://www.aditmasih.tk/api-hafid/all.php")
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['data_angkatan'])):
            nrp = data['data_angkatan'][int(i)][0]
            nama = data['data_angkatan'][int(i)][2]
            kos = data['data_angkatan'][int(i)][4]
            hasil=hasil+str(i+1)
            hasil=hasil+".\nNrp : "
            hasil=hasil+nrp
            hasil=hasil+"\nNama : "
            hasil=hasil+nama
            hasil=hasil+"\nKosan : "
            hasil=hasil+kos
            hasil=hasil+"\n"
        return hasil
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'


#DELETE DATA MHS
def hapusmhs(nrp):
    r = requests.post("http://www.aditmasih.tk/api-hafid/delete.php", data={'nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def updatemhs(nrpLama,nrp,nama,kosan):
    URLmhs = "http://www.aditmasih.tk/api-hafid/show.php?nrp=" + nrpLama
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    nrp_lama=nrpLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api-hafid/update.php", data={'nrp': nrp, 'nama': nama, 'kosan': kosan, 'nrp_lama':nrp_lama})
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
    text = event.message.text #simplify for receive message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)

    data=text.split('-')
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carimhs(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2],data[3])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusmhs(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatemhs(data[1],data[2],data[3],data[4])))
    elif(data[0]=='semwa'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allsmhs()))
    elif(data[0]=='menu'):
        menu = "1. lihat-[nrp]\n2. tambah-[nrp]-[nama]-[kosan]\n3. hapus-[nrp]\n4. ganti-[nrp lama]-[nrp baru]-[nama baru]-[kosan baru]\n5. semwa"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)