from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
import json
import sys
import cgi
import random
import os
import string

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open("index.html", "r") as file:
            self.respond(file.read(), 200)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers['Content-Type']})
        fileitem = form["file"]
        response = {}
        responseCode = 400

        if fileitem.file:
            filename = os.path.basename(fileitem.filename)
            tmpfilename = os.path.dirname(os.path.realpath(__file__)) + "/tmp_images/" + filename
            # TODO: check whether
            # - directory tmp_images exists
            # - filename already exists (allow overwrite or append random string to file for differentiation?)
            with open(tmpfilename, "wb") as fh:
                fh.write(fileitem.file.read())
            print("The file " + filename + " was uploaded successfully", flush = True)
        else:
            response["success"] = False
            response["reason"] = "There was an error with saving the uploaded file"
            responseCode = 500
        
        # TODO: prediction
        prediction = "cat"
        if (True):
            response["success"] = True
            response["result"] = {"prediction": prediction}
            responseCode = 200

        self.respond(toJsonString(response), responseCode)

    def respond(self, responseString, responseCode):
        response = BytesIO()
        response.write(stringMsgToBytes(responseString))
        self.send_response(responseCode)
        self.end_headers()
        self.wfile.write(response.getvalue())

def bytesMsgToString(byteMsg):
    return str(byteMsg, "utf-8")

def stringMsgToBytes(stringMsg):
    return bytes(stringMsg, "utf-8")

def jsonStringToDict(jsonString):
    try:
        jsonObject = json.loads(jsonString)
    except ValueError:
        return False, None
    return True, jsonObject

def toJsonString(msg):
    return json.dumps(msg)

def createRandomString(length, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(length))


if __name__ == '__main__':
    # defaults
    host = "0.0.0.0"
    port = 8080

    argc = len(sys.argv)
    if (argc >= 2):
        host = sys.argv[1]
    if (argc >= 3):
        port = int(sys.argv[2])
    print("Listening on %s:%d" % (host, port), flush = True)

    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    httpd.serve_forever()
