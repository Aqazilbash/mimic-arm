import time
import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Bool
import message_filters

class HandTracker(Node):
    pass

def main():
    rclpy.init()
    rclpy.spin(HandTracker())
    rclpy.shutdown()
