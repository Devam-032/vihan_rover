#!/usr/bin/env python3
#from _future_ import print_function
#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing.image import img_to_array
import cv2
import numpy as np
import argparse
import random as rng
#from tensorflow.keras.backend import set_session
#import tensorflow as tf
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge
dir = Float32()
dir.data = 0
#from stage3.msg import Arrow_detection

pub1 = rospy.Publisher('Arrow_stream', Image, queue_size=10)
pub2 = rospy.Publisher('wtg', Float32, queue_size=10 ,latch=True)
#feedback = Arrow_detection()
"""

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction=0.8
session = tf.compat.v1.Session(config=config)
session1 = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

sess = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session (sess)
#model = load_model("Arrow160inceptionv3p.h5")"""

rng.seed(12345)


def get_contour_areas(contours):
    all_areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        all_areas.append(area)
    return np.max(all_areas)


def drawContours11111(img):
    blur = cv2.medianBlur(img, 5)
    # cv2.imshow("blur",blur)
    edged = cv2.Canny(blur, 150, 255)
    # cv2.imshow("edged",edged)
    contours, heirarchy = cv2.findContours(
        edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    blank_image = np.zeros([img.shape[0], img.shape[1], 3], dtype=np.uint8)
    blank_image.fill(255)
    #cv2.drawContours(blank_image, contours, -1, (160,160, 0), 3)
    maxarea = get_contour_areas(contours)
    return blank_image, maxarea


def callback(x):
    global feedback
    pass


def thresh_callback(val):
    global feedback
    global rcnt
    global lcnt
    threshold = val

    ret, th = cv2.threshold(src_gray, 127, 255, cv2.THRESH_BINARY)
    canny_output = cv2.Canny(th, threshold, 255)
    contours, _ = cv2.findContours(
        canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    area = cv2.contourArea(contours[max_index])
    if area > 50000:
        global dir
        pub_count = 0
        print("Area is too near to object")
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(src, (x, y), (x + w, y + h), color, 2)
        cv2.circle(src, (x+int(w/2), y+int(h/2)), 3, color, -1)
        cropped_image = src[y:y+h, x:x+w]
        try:
            predict_again(cropped_image)
            dir.data = 1000000000
            #pub2.publish(dir)
        except ValueError:
            pass

    if area > 8000:
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(src, (x, y), (x + w, y + h), color, 2)
        cv2.circle(src, (x+int(w/2), y+int(h/2)), 3, color, -1)
        cropped_image = src[y:y+h, x:x+w]
        try:
            predict_again(cropped_image)
            dir.data = 1000000000
            #pub2.publish(dir)
        except ValueError:
            pass
        x = (x+int(w/2))
        dir.data = 1000000000 + x
        #pub2.publish(dir)

    cv2.imshow("source_window", src)


def predict_again(src):
    """         ############################TO PREDICT WID CERTAIN MODEL#######################################################3
    src = src/255
    src = cv2.resize(src,(224,224))
    img = img_to_array(src)
    img = img.reshape((1,img.shape[0],img.shape[1],img.shape[2]))
    yhat2 = model.predict(img)
    np.argmax(yhat2,axis =1)
    print("yhat2:::::::::::::::::::",np.argmax(yhat2))
    """
    global rcnt
    global lcnt
    global dir
    H, W = src.shape[:2]
    # cv2.imshow("cROPPPPPPED",src)
    #print (src.shape)

    img1 = src[:, :int(W/2)]
    img2 = src[:, int(W/2)+1:]
    contoured1, area1 = drawContours11111(img1)
    contoured2, area2 = drawContours11111(img2)
    # cv2.imshow("blank_image",contoured1)
    # cv2.imshow("blank_image1",contoured2)
    print(area1, area2)
    if area2 > area1:
        #print ("New:::::::::::::RIGGGGGGGGGHT")
        if rcnt >= 3:
            print("New:::::::::::::RIGGGGGGGGGHT")
            dir.data = 1
            pub2.publish(dir)
        rcnt += 1
        lcnt = 0
    elif area1 > area2:
        #print ("New:::::::::::::LEFTTTTTTTTT")
        if lcnt >= 3:
            print("New:::::::::::::LEFTTTTTTTTT")
            dir.data = -1
            pub2.publish(dir)
        lcnt += 1
        rcnt = 0


cap = cv2.VideoCapture(0)
counter = 0
lcnt = 0
rcnt = 0
rospy.init_node("Arrow_detection")
rate = rospy.Rate(5)


while True:
    # feedback.direction = 0
    success, frame = cap.read()
    br = CvBridge()
    pub1.publish(br.cv2_to_imgmsg(frame))
    if frame is None:
        break
    img = frame.copy()
    src = frame.copy()
    if src is None:
        exit(0)
    try:

        """
        frame1 = frame/255
        frame1 = cv2.resize(frame1,(160,160))
        image = img_to_array(frame1)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        yhat = model.predict(image)

        np.argmax(yhat,axis=1)

        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        src_gray = cv2.blur(src_gray, (3, 3))
        thresh = 100
        if (np.argmax(yhat) == 0):
                if counter >=15:
                        print ("DETECTED")
                try:"""
        thresh = 100

        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        src_gray = cv2.blur(src_gray, (3, 3))

        thresh_callback(thresh)
        """
			except ValueError:
				pass
				print("#########################mjnbjhb vf#################################")

				#feedback.detection = 1
			counter += 1
		else:
			counter = 0
			print("NHI DETECTED")
			feedback.detection = 0
			feedback.direction = 0
		"""
        cv2.imshow("source_window", src)
    except AttributeError or ValueError:
        pass
    if cv2.waitKey(1) == 13:
        break


cap.release()
cv2.destroyAllWindows()
