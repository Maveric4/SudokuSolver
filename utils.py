import cv2
import numpy as np
import tensorflow

def standarize_digit_img_to_model_input(img, size):
    if isinstance(img, str):
        img = cv2.imread(img)
    img_resized = cv2.resize(img, (size, size))
    return img_resized


def binarize_img(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray_img, (5, 5), 0)
    ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.bitwise_not(th)


def prepare_to_predict(img):
    return img.reshape(1, 28, 28, 1) / 255.0


def predict_digit(model, img):
    digit_img = standarize_digit_img_to_model_input(img, 28)
    if len(img.shape) == 3:
        bin_digit_img = binarize_img(digit_img)
    else:
        bin_digit_img = digit_img
    img = prepare_to_predict(bin_digit_img)
    prob_predictions = model.predict(img)
    if np.any(prob_predictions > 0.7):
        prediction = [(np.where(item == np.amax(item)))[0][0] for item in prob_predictions]
        return prediction[0]
    else:
        return 0


def load_model(model_path):
    return tensorflow.keras.models.load_model(model_path)


def load_mnist_model():
    model_path = "./MNISTmodel/models/train_mnist1_model3.h5"
    return tensorflow.keras.models.load_model(model_path)

