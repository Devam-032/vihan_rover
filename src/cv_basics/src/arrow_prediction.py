from typing import Tuple
from tflite_model_maker.image_classifier import DataLoader
from tflite_model_maker import image_classifier

import tensorflow as tf
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

MODEL_PATH = (r'C:\Users\ASUS\Desktop\rover_ai\image_classification\models\arrow_classifier.tflite')

def get_interpreter(model_path: str) -> Tuple:
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    return interpreter, input_details, output_details

def predict(image_path: str) -> int:
    interpreter, input_details, output_details = get_interpreter(MODEL_PATH)
    input_shape = input_details[0]['shape']
    img = tf.io.read_file(image_path)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.resize(img, (input_shape[2], input_shape[2]))
    img = tf.expand_dims(img, axis=0)
    resized_img = tf.cast(img, dtype=tf.uint8)
    
    interpreter.set_tensor(input_details[0]['index'], resized_img)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)
    return np.argmax(results, axis=0)

img_path=r'C:\Users\ASUS\Desktop\rover_ai\image_classification\rover_data_3\train\right\img1.jpeg'
print(predict(img_path))
# if t==0:
#     print('Left')
# elif t==1:
#     print('Right')
# else:
#     print('stop')

# img = mpimg.imread(img_path)
# imgplot = plt.imshow(img)
# plt.show()