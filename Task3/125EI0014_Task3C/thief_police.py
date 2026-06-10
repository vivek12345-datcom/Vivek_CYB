import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import random

class PoliceThief(Node):

    def __init__(self):
        
        self.thief_x = 0.0
        self.thief_y = 0.0
        self.police_x = 0.0
        self.police_y = 0.0

        super().__init__("thief_police")

        self.spawn_client=self.create_client(Spawn,"/spawn")
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for spawn service...")

        self.spawn_turtle()

        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.cmd_vel_pub_pol_=self.create_publisher(Twist,"/police/cmd_vel",10)
        self.pose_=self.create_subscription(Pose,"/turtle1/pose",self.thief_pose,10)
        self.pose_police=self.create_subscription(Pose,"/police/pose",self.police_pose,10)
        self.timer=self.create_timer(0.5,self.move_randomly)

    def thief_pose(self,pose:Pose):
        self.thief_x=pose.x
        self.thief_y=pose.y
    
    def police_pose(self,pose:Pose):
        cmd=Twist()
        self.police_x=pose.x
        self.police_y=pose.y
        if((((self.police_x-self.thief_x)*(self.police_x-self.thief_x))+((self.police_y-self.thief_y)*(self.police_y-self.thief_y)))<=0.25):
            cmd.linear.x=0.0
            cmd.linear.y=0.0
            self.get_logger().info("THief caught at (x=" + str(self.police_x) + ",y=" + str(self.police_y) + ")")
            self.timer.cancel()
            rclpy.shutdown

        else:
            cmd.linear.x=(self.thief_x-self.police_x)/1.5
            cmd.linear.y=(self.thief_y-self.police_y)/1.5

        self.cmd_vel_pub_pol_.publish(cmd)

    def spawn_turtle(self):
        request=Spawn.Request()
        request.x=2.0
        request.y=2.0
        request.theta=0.2
        request.name="police"

        self.spawn_client.call_async(request)

    def move_randomly(self):
        msg=Twist()
        msg.linear.x=random.uniform(2.0,5.0)
        msg.angular.z=random.uniform(2.5,3.0)

        self.cmd_vel_pub_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node=PoliceThief()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()