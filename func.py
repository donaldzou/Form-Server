import json
import hashlib
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
            host="178.128.231.4",
            user="donaldzou",
            passwd="Jimolkio0~",
            database="python_web_server"
)

def load_data():
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM post')
        myresult = mycursor.fetchall()
        result = []
        for n in myresult:
            temp = {
                "id": n[0],
                "title": n[1],
                "username":n[2],
                "data":n[3],
                "time":n[4]
            }
            result.append(temp)
        print(result)
        return str(result).replace("'",'"')

def post_content(post_data):
        new_json = json.loads(post_data.decode('utf-8'))
        now = datetime.now()
        id = str(now)+str(new_json)
        new_json['id'] = hashlib.sha256(id.encode('utf-8')).hexdigest()
        mycursor = mydb.cursor()
        sql = "INSERT INTO post (id, title, username,content,time) VALUES (%s, %s,%s,%s,%s)"
        val = (new_json['id'],new_json['title'],new_json['username'],new_json['data'],new_json['time'])
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        return("Stored: "+new_json['id'])

def edit_content(content):
        mycursor = mydb.cursor()
        new_data = json.loads(content.decode('utf-8'))
        content_id = new_data['id']
        mycursor.execute("UPDATE post SET content ='"+new_data['data']+"' WHERE id='"+content_id+"'")
        mydb.commit()
        if mycursor.rowcount == 0:
            return("danger-Uh oh!-There's no changes")
        return('success-All good!-Edit Saved')

def delete_content(content):
    mycursor = mydb.cursor()
    cid = json.loads(content.decode('utf-8'))
    content_id = str(cid['id'])
    mycursor.execute('DELETE FROM post WHERE id = "'+content_id+'";')

    return('Delted: '+str(content_id))