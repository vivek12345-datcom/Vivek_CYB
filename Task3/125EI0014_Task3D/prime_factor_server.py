import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import PrimeFactors

class PrimeFactorServer(Node):

    def __init__(self):
        super().__init__("prime_factor_server")
        self.server=self.create_service(PrimeFactors,"prime_factors",self.callback)
        self.get_logger().info("Prime Factor Server Started")

    def callback(self,request,response):
        n=request.number
        factors=set()
        divisor=2

        while n>1:
            
            while n%divisor==0:
                factors.add(divisor)
                n//=divisor
            divisor+=1
        response.factors=factors
        return response
    
def main(args=None):
    rclpy.init(args=args)
    node=PrimeFactorServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main
