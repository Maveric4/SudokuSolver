# import tensorflow as tf
import cv2
import sys
sys.path.append("..")
import utils
import numpy as np

model_path = "./models/train_mnist1_model3.h5"
img_path = "../img/seven.png"
# img_path = "../img/one.png"
# img_path = "../img/six.png"

mnist_model = utils.load_model(model_path)

## Way 1
print("Way 1")
digit_img = utils.standarize_digit_img_to_model_input(img_path, 28)
bin_digit_img = utils.binarize_img(digit_img)
img = utils.prepare_to_predict(bin_digit_img)

cv2.imshow("Digit", digit_img)
cv2.imshow("Binary digit", bin_digit_img)
cv2.waitKey(50)

prob_predictions = mnist_model.predict(img)
prediction = [(np.where(item == np.amax(item)))[0][0] for item in prob_predictions]
print("Prediction: {}".format(prediction[0]))


## Way 2
print("Way 2")
prediction = utils.predict_digit(mnist_model, img_path)
print("Prediction: {}".format(prediction))
