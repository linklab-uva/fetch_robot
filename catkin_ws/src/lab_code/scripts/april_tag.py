#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import apriltag


detector = apriltag.Detector()
bridge = CvBridge()
result = []
image = None
val = False
threshold = 1


def save_image(data):
	global bridge, detector, result, image, val
	try:
		image = bridge.imgmsg_to_cv2(data, "rgb8")
		gray = bridge.imgmsg_to_cv2(data, "mono8")
	except CvBridgeError, e:
		print(e)
		return

	result = detector.detect(gray)[0]
	val = True
	print(result)


def main():
	global result, image, bridge, val
	rospy.init_node('april_tag', anonymous=True)
	rospy.Subscriber('/head_camera/rgb/image_raw', Image, save_image)
	image_pub = rospy.Publisher('/april_tag', Image, queue_size=1)

	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		if val:
			# extract the bounding box (x, y)-coordinates for the AprilTag
			# and convert each of the (x, y)-coordinate pairs to integers
			(ptA, ptB, ptC, ptD) = result.corners
			ptB = (int(ptB[0]), int(ptB[1]))
			ptC = (int(ptC[0]), int(ptC[1]))
			ptD = (int(ptD[0]), int(ptD[1]))
			ptA = (int(ptA[0]), int(ptA[1]))
			# draw the bounding box of the AprilTag detection
			cv2.line(image, ptA, ptB, (0, 255, 0), 2)
			cv2.line(image, ptB, ptC, (0, 255, 0), 2)
			cv2.line(image, ptC, ptD, (0, 255, 0), 2)
			cv2.line(image, ptD, ptA, (0, 255, 0), 2)
			# draw the center (x, y)-coordinates of the AprilTag
			(cX, cY) = (int(result.center[0]), int(result.center[1]))
			cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
			# draw the tag family on the image
			tagFamily = result.tag_family.decode("utf-8")
			cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			
			image_pub.publish(bridge.cv2_to_imgmsg(image))

			print(image.shape)
			print(cY)

			image_cY = image.shape[0] // 2
			print(cY == image_cY)

		rate.sleep()


if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		print 'ros interrupt exception error'
