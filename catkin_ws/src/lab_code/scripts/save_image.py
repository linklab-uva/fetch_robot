#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


def save_image(data):
	print('Received Image')
	try:
		cv2_img = CvBridge().imgmsg_to_cv2(data, "bgr8")
		cv2.imwrite('/home/utkarsh/camera_image.jpeg', cv2_img)
		print('Saved Image')
	except CvBridgeError, e:
		print(e)


def main():
	rospy.init_node('save_image', anonymous=True)
	rospy.Subscriber('/head_camera/rgb/image_raw', Image, save_image)

	rospy.spin()


if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		print 'ros interrupt exception error'
