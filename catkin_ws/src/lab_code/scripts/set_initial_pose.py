#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped


def set_pose():
	rospy.init_node('set_initial_pose', anonymous=True)
	rate = rospy.Rate(10)

	pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)
	initial_connections = pose_pub.get_num_connections()

	pose = PoseWithCovarianceStamped()

	pose.header.frame_id = 'map'
	pose.header.stamp = rospy.Time.now()

	pose.pose.pose.position.x = -4.6815389438
	pose.pose.pose.position.y = 5.96489293409

	pose.pose.pose.orientation.z = 0.937464041414
	pose.pose.pose.orientation.w = 0.34808213263

	while pose_pub.get_num_connections() == initial_connections:
		rate.sleep()

	pose_pub.publish(pose)


if __name__ == '__main__':
	try:
		set_pose()
	except rospy.ROSInterruptException:
		print 'ros interrupt exception error'
