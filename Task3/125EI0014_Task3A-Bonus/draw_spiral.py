import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawSpiral(Node):

    def __init__(self):
        super().__init__("draw_spiral")
        self.x_cord_=0.05
        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.timer_=self.create_timer(0.5,self.send_vel_cmd)

    def send_vel_cmd(self):
        cmd=Twist()
        cmd.linear.x=self.x_cord_
        cmd.angular.z=2.0
        self.x_cord_+=0.05
        self.cmd_vel_pub_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node=DrawSpiral()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()