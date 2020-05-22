from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import hashlib

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def post_content(self, post_data):
        #Load json file
        json_file = open('data.json','r')
        #Read data
        json_data = json.loads(json_file.readline())
        #Get New Json data
        new_json = json.loads(post_data.decode('utf-8'))
        #Insert id
        from datetime import datetime
        now = datetime.now()
        id = str(now)+str(new_json)
        new_json['id'] = hashlib.sha256(id.encode('utf-8')).hexdigest()
        #Append
        json_data.append(new_json)
        #Close
        json_file.close()
        #Open as write
        json_file = open("data.json",'w')
        #Write json data
        json_file.write(json.dumps(json_data))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        print("data:",post_data.decode('utf-8'))
        
        path = str(self.path)
        path = path.strip('/')
        exec("self."+path+'(post_data)')
        # self.post_content(post_data)
        self._set_response()
        self.wfile.write("Stored".encode('utf-8'))
    

def run(server_class=HTTPServer, handler_class=S, port=7070):
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