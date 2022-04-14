#!/usr/bin/env python

import rospy
import csv
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from std_msgs.msg import Bool
from sound_play.msg import SoundRequest


POIs_done = 0
filename = '/home/utkarsh/catkin_ws/src/lab_code/scripts/pois.csv'
reader = csv.DictReader(open(filename, 'r'))
moving = False
initial_pose_set = False


def sound(data):
	global moving
	if data.sound == 3:
		moving = False


def initial_pose(data):
	global initial_pose_set
	if not initial_pose_set:
		print('Set initial pose')
		initial_pose_set = True


def navigate():
	global reader, moving, POIs_done

	rospy.init_node('lab_navigation', anonymous=True)
	rate = rospy.Rate(10)

	rospy.Subscriber('/robotsound', SoundRequest, sound)
	rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, initial_pose)
	goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
	initial_connections = goal_pub.get_num_connections()

	goal = PoseStamped()

	# wait until the initial pose has been set
	while not initial_pose_set:
		rate.sleep()

	# wait until the publisher's connection is established
	while goal_pub.get_num_connections() == initial_connections:
		rate.sleep()
	
	while not rospy.is_shutdown():
		if not moving:
			try:
				next_point = next(reader)
			except StopIteration:
				print('There are no more points')
				moving = True
				continue

			goal.header.frame_id = 'map'
			goal.header.stamp = rospy.Time.now()

			goal.pose.position.x = float(next_point['x'])
			goal.pose.position.y = float(next_point['y'])

			goal.pose.orientation.z = float(next_point['oz'])
			goal.pose.orientation.w = float(next_point['ow'])

			print('Going to POI #'+ str(POIs_done + 1))

			goal_pub.publish(goal)

			moving = True
			POIs_done += 1

		rate.sleep()


if __name__ == '__main__':
	try:
		navigate()
	except rospy.ROSInterruptException:
		print 'ros interrupt exception error'
