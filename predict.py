import sys
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.preprocessing import image

classifier = None
def init():
    # get model
    global classifier
    if classifier == None:
        classifier = load_model("classifier.h5")

def predictFromFile(imgPath):
    img = readFileToImg(imgPath)
    return predict(img)

def predictFromPILImg(img):
    # make sure the file has dimensions (64, 64)
    img = img.resize((64, 64), Image.ANTIALIAS)
    return predict(img)

def readFileToImg(imgPath):
    # get image with correct dimensions (64, 64)
    return image.load_img(imgPath, target_size = (64, 64))

def predict(img):
    init()
    # prepare image
    img = img.convert("RGB") # omits the alpha channel
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)

    # predict image with classifier
    prediction = classifier.predict(img)

    # interpret prediction value
    prediction_tag = ""
    if (prediction[0][0] >= 0.5):
        prediction_tag = "dog"
    else:
        prediction_tag = "cat"

    return prediction_tag

if __name__ == "__main__":
    if (len(sys.argv) - 1 != 1):
        print("You need the absolute img location as argument!")
        exit(1)
    
    imgPath = sys.argv[1]
    prediction_tag = predictFromFile(imgPath)
    print("The image was predicted to be a:", prediction_tag)
    exit(0)
