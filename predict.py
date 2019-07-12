import sys
import numpy as np
from keras.models import load_model
from keras.preprocessing import image

if (len(sys.argv) - 1 != 1):
    print("You need the absolute img location as argument!")
    exit(1)

# get model
classifier = load_model("classifier.h5")

# get image with correct dimensions (64, 64)
imgPath = sys.argv[1]
img = image.load_img(imgPath, target_size = (64, 64))
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

print(prediction_tag)
exit(0)
