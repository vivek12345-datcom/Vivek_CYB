#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class WaypointNavigation(Node):

    def __init__(self):
        super().__init__("waypoint_navigation")

        self.points = [[5.5, 9.5],[7.0, 5.5],[10.0, 5.5],[7.8, 3.0],[9.0, 0.5],[5.5, 2.5],[2.0, 0.5],[3.2, 3.0],[1.0, 5.5],[4.0, 5.5],[5.5, 9.5]]
        self.counter = 0
        self.cmd_vel_pub_ = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.pose_sub_ = self.create_subscription(Pose,"/turtle1/pose",self.call_back,10)

    def call_back(self, pose: Pose):

        if self.counter >= len(self.points):
            return

        target_x = self.points[self.counter][0]
        target_y = self.points[self.counter][1]
        dx = target_x - pose.x
        dy = target_y - pose.y

        distance = math.sqrt(dx * dx + dy * dy)
        target_theta = math.atan2(dy, dx)
        angle_error = target_theta - pose.theta
        self.get_logger().info(f"Position error: dx={dx},dy={dy}")
        self.get_logger().info(f"Angular error:{angle_error}")
        while angle_error > math.pi:
            angle_error -= 2 * math.pi

        while angle_error < -math.pi:
            angle_error += 2 * math.pi

        cmd = Twist()

        cmd.angular.z = 4.0 * angle_error
        if abs(angle_error) < 0.3:
            cmd.linear.x = min(distance, 2.0)
        else:
            cmd.linear.x = 0.0
        if distance < 0.2:
            self.counter += 1
            self.get_logger().info(
                f"Reached waypoint {self.counter}"
            )

        self.cmd_vel_pub_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = WaypointNavigation()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()