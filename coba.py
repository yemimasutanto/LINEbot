import requests, json

def inputadmin(nrp, nama, alamat):
    r = requests.post("http://www.aditmasih.tk/api_yemima/insert.php", data={'nrp': nrp, 'nama': nama, 'alamat': alamat})
    data = r.json()

    flag = data['flag']
    print(flag)
   
    # if(flag == "1"):
    #     return 'Data '+nama+' berhasil dimasukkan\n'
    # elif(flag == "0"):
    #     return 'Data gagal dimasukkan\n'


inputadmin("12345","aa","bb")