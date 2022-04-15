#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import apriltag


detector = apriltag.Detector()
bridge = CvBridge()


def save_image(data):
	global bridge, detector
	print('Received Image')
	try:
		cv2_img = bridge.imgmsg_to_cv2(data, "mono8")
	except CvBridgeError, e:
		print(e)
		return

	result = detector.detect(cv2_img)
	print(result)


def main():
	rospy.init_node('april_tag', anonymous=True)
	rospy.Subscriber('/head_camera/rgb/image_raw', Image, save_image)

	rospy.spin()


if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		print 'ros interrupt exception error'
