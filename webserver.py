from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
from io import BytesIO
from pathlib import Path
import json
import sys
import cgi
import random
import os
import string

from predict import predictFromPILImg

shouldSaveUploadedImage = False

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
            img = Image.open(BytesIO(fileitem.file.read()))
            if shouldSaveUploadedImage:
                # create target dir if it doesn't exist
                tmpDir = Path(os.path.dirname(os.path.realpath(__file__)) + "/tmp_images")
                if not (tmpDir.exists() & tmpDir.is_dir()):
                    os.mkdir(str(tmpDir))
                tmpfilename = tmpDir / filename

                # add random string to filename (before .jpg) if file already exists
                if tmpfilename.exists() & tmpfilename.is_file():
                    tmpfilenameSplit = str(tmpfilename).split(".")
                    tmpfilenameSplit[-2] = tmpfilenameSplit[-2] + "_" + createRandomString(10)
                    tmpfilename =  ".".join(tmpfilenameSplit)

                img.save(tmpfilename)
                print("The file " + filename + " was saved successfully to " + tmpfilename, flush = True)
            
            # do prediction
            prediction = predictFromPILImg(img)
            print("prediction for file " + filename + ": " + prediction, flush = True)
            response["success"] = True
            response["result"] = {"prediction": prediction}
            responseCode = 200
        else:
            response["success"] = False
            response["reason"] = "There was an error with saving the uploaded file"
            responseCode = 500

        self.respond(toJsonString(response), responseCode)

    def respond(self, responseString, responseCode):
        response = BytesIO()
        response.write(stringMsgToBytes(responseString))
        self.send_response(responseCode)
        self.end_headers()
        self.wfile.write(response.getvalue())

# helpers
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
