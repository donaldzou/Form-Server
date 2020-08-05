from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import hashlib
import mysql.connector
from func import *


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        try:
            # self.path has /test.html
            if len((self.path).split('.')) == 2:
                f = open((self.path).strip('/'), 'rb')
                self.send_response(200)
                if self.path.endswith(".css"):
                    self.send_header('Content-type','text/css')
                else:
                    self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            else:
                self._set_response()
                self.wfile.write(eval((self.path).strip('/')+'()').encode('utf-8'))
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def load_data(self):
        mydb = mysql.connector.connect(
            host="178.128.231.4",
            user="donaldzou",
            passwd="Jimolkio0~",
            database="python_web_server"
        )

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
        return str(result).replace("'",'"')

    def open(self):
        #Load json file
        json_file = open('json/comment.json', 'r')
        #Read data
        json_data = json.loads(json_file.readline())
        json_file.close()
        return json_data

    def save(self, json_data):
        json_file = open("data.json", 'w')
        json_file.write(json.dumps(json_data))
        json_file.close()

    



    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        print("data:", post_data.decode('utf-8'))
        path = str(self.path)
        path = path.strip('/')
        self._set_response()
        self.wfile.write(eval(path+'(post_data)').encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
