import gzip
import tensorflow as tf

f_images = gzip.open('./data/train-images-idx3-ubyte', 'wb')
f_labels = gzip.open('./data/train-labels-idx1-ubyte', 'wb')


img_shape = 28, 28, 1
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(x_train.shape[0], *img_shape).astype('float32') / 255
x_test = x_test.reshape(x_test.shape[0], *img_shape).astype('float32') / 255

images_file = x_train.tobytes()
labels_file = y_train.tobytes()

f_images.write(images_file)
f_labels.write(labels_file)

f_images.close()
f_labels.close()
