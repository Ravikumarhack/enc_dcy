from flask import Flask,request,jsonify
from flask_mysql_connector import MySQL
import time
import json
from Crypto.Cipher import AES
import base64
import pandas as pd
app=Flask(__name__)
import sys

#database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'fds'
mysql=MySQL(app)

key = 'ufEuJVLFjtVzXMcCBPDkemUTnbIdWMgJ'
iv = ('ufEuJVLF@tVzXMcC').encode('utf-8')
@app.route('/fdsAPI',methods=['GET','POST'])
def fdsApiFun():
    if request.method=='GET':
        con=mysql.new_cursor()
        start=time.time()
        con.execute('select csc_id,txn_amout,pay_date,txn_date,csc_txn,category_of_Trans,suspected from fds.topup_db')
        end=time.time()
        print(end-start,'\n\n\n')
        alldata=con.fetchall()
        # finalData = pd.read_csv('sampleData.csv').to_dict()
        finalData=[]
        start=time.time()
        for i in alldata:   
            data={}     
            data['csc_id']=i[0]
            data['txn_amout']=i[1]
            data['pay_date']=str(i[2])
            data['txn_date']=str(i[3])
            data['csc_txn']=i[4]
            data['category_of_trans']=i[5]
            data['suspected']=i[6]
            finalData.append(data)
        end=time.time()
        print(sys.getsizeof(finalData)/(1024*1024))
        finalData = json.dumps(finalData).encode('utf-8')
        cipher_encrypt = AES.new(key.encode('utf-8'), AES.MODE_CFB,iv)
        ciphered_bytes = cipher_encrypt.encrypt(finalData)
        cipher_data = base64.b64encode(ciphered_bytes)
        # iv = cipher_encrypt.iv
        # print(iv)
        # iv = base64.b64encode(iv)
        # print(end-start,'\n\n\n')
        # start=time.time()
        print(sys.getsizeof(cipher_data)/(1024*1024))
        return jsonify({'data':cipher_data.decode('utf-8')})
    if request.method == 'POST':
        data = json.loads(request.data)
        # print(data)
        ciphered_data = data['data']
        ciphered_data = base64.b64decode(ciphered_data)
        cipher_decrypt = AES.new(key.encode('utf-8'), AES.MODE_CFB,iv=iv)
        deciphered_bytes = cipher_decrypt.decrypt(ciphered_data)
        decrypted_data = deciphered_bytes.decode('windows-1252')
        print(decrypted_data)
        return decrypted_data


@app.route('/')
def home():
    return "<p>This is FDS api</p>"


if __name__=='__main__':
    app.run(debug=True,port=5001)
