from flask import Flask,request,jsonify
from flask_mysql_connector import MySQL
import json
from Crypto.Cipher import AES
import base64

app=Flask(__name__)

#database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'abc'          # Name of Database
mysql=MySQL(app)

#Key and initilizator vector
key = 'klV@#&LFjtVzXMcCppDkemUTnbIdWMgJ'
iv = ('ufEuJr4F@tVzXM**').encode('utf-8')

@app.route('/edAPI',methods=['GET','POST'])
def fdsApiFun():
    if request.method=='GET':
        #Create crusor
        con=mysql.new_cursor()
        con.execute('select * from abc.xyz_db')
        alldata=con.fetchall()
        #Dump data to json format and encode utf-8 format
        finalData = json.dumps(alldata).encode('utf-8')
        # Encrypt data with AES encryption to cipher text
        cipher_encrypt = AES.new(key.encode('utf-8'), AES.MODE_CFB,iv)
        ciphered_bytes = cipher_encrypt.encrypt(finalData)
        # Encoding cipher text to base64
        cipher_data = base64.b64encode(ciphered_bytes)
        return jsonify({'data':cipher_data.decode('utf-8')})
    

    if request.method == 'POST':
        # json data load
        data = json.loads(request.data)
        ciphered_data = data['data']
        # Decoding data from base64
        ciphered_data = base64.b64decode(ciphered_data)
        # Decrypt the cipher text
        cipher_decrypt = AES.new(key.encode('utf-8'), AES.MODE_CFB,iv=iv)
        deciphered_bytes = cipher_decrypt.decrypt(ciphered_data)
        decrypted_data = deciphered_bytes.decode('windows-1252')
        return decrypted_data


@app.route('/')
def home():
    return "<p>This is api</p>"


if __name__=='__main__':
    app.run()
