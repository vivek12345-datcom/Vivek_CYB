#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtleController(Node):
    
    def __init__(self):
        super().__init__("turtle_controller")
        
        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.pose_subscriber_=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.get_logger().info("Turtle info has been started")

    def pose_callback(self,pose:Pose):
        cmd=Twist()
        

        if pose.x>=5.5 and pose.x<7.544 and pose.y>5.544 and pose.y<7.544:
            cmd.linear.x=1.0
            cmd.linear.y=1.0
            cmd.angular.z=0.0

        elif(pose.y>=7.544):
            cmd.linear.y=1.0
            cmd.linear.x=1.0
            cmd.angular.z=1.0
            
        elif(pose.y<=5.544):
            cmd.linear.y=-1.0
            cmd.linear.x=1.0
            cmd.linear.y=1.0
            cmd.linear.x=1.0
            cmd.angular.z=-1.0

        
        self.cmd_vel_pub_.publish(cmd) 

def main(args=None):
    rclpy.init(args=args)
    node=TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()