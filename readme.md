## Description
The goal is to upload an image file from browser and predict whether it's a cat or a dog.

This repository contains a pre-trained classifier (classifier.h5), that was trained with a simple CNN.
The training follows the tutorial in https://medium.com/nybles/create-your-first-image-recognition-classifier-using-cnn-keras-and-tensorflow-backend-6eaab98d14dd

The data that `train.py` expects in directory *dataset* can be found here: https://www.superdatascience.com/pages/machine-learning (Part 8, Section 40, CNN)

### Dones
- script for training the classifier
- script for prediction using the trained classifier
- webserver GET

### TODOs
- webserver POST: upload image file to webserver
- do prediction for that image file
- return prediction to browser