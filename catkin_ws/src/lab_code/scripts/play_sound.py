#!/usr/bin/env python

import rospy
from sound_play.msg import SoundRequest
from move_base_msgs.msg import MoveBaseActionResult

play_sound = False

def status(data):
	global play_sound
	if data.status.status == 3:
		play_sound = True
	else:
		play_sound = False


def sound():
	global play_sound
	rospy.init_node('play_sound', anonymous=True)
	rate = rospy.Rate(10)

	sound_pub = rospy.Publisher('/robotsound', SoundRequest, queue_size=1)	
	rospy.Subscriber('/move_base/result', MoveBaseActionResult, status)

	sound = SoundRequest()

	sound.sound = 3
	sound.command = 1
	sound.volume = 1

	while not rospy.is_shutdown():
		if play_sound:
			play_sound = False
			sound_pub.publish(sound)
			print('Reached!')
		rate.sleep()


if __name__ == '__main__':
	try:
		sound()
	except rospy.ROSInterruptException:
		print 'ros interrupt exception error'
