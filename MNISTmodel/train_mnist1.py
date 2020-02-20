import tensorflow as tf
import datetime
import os
import numpy as np
from tensorflow.python.keras.callbacks import TensorBoard

mnist = tf.keras.datasets.mnist
(training_images, training_labels), (test_images, test_labels) = mnist.load_data()

# print(training_images.shape)
# print(test_images.shape)
training_images = training_images / 255.0
test_images = test_images / 255.0
training_images = training_images.reshape(training_images.shape[0], 28, 28, 1)
test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

test_images, validation_images = np.split(test_images, [int(test_images.shape[0]*0.4)])
test_labels, validation_labels = np.split(test_labels, [int(test_labels.shape[0]*0.4)])

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])


## Designing callbacks
class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        print("\nReached {} epoch".format(epoch + 1))
        if logs.get('accuracy') > 0.997:
            print("Reached 99.99% accuracy so cancelling training!")
            self.model.stop_training = True


log_dir = os.path.join(
    "logs",
    "fit",
    datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(training_images,
          training_labels,
          validation_data=(validation_images, validation_labels),
          epochs=20,
          callbacks=[myCallback(), tensorboard_callback],
          verbose=2)

# model.summary()
metrics = model.evaluate(test_images, test_labels)
print("[Loss, Accuracy]")
print(metrics)
model.save("./models/train_mnist1_model3.h5")

