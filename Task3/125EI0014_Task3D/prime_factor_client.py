import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import PrimeFactors

class PrimeFactorClient(Node):

    def __init__(self):
        super().__init__("prime_factor_client")
        self.client=self.create_client(PrimeFactors,"prime_factors")

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for server......")

        request=PrimeFactors.Request()
        request.number=int(input("Enter a positive number: "))
        future=self.client.call_async(request)
        future.add_done_callback(self.callback)

    def callback(self,future):
        response=future.result()
        self.get_logger().info(f"Prime factors: {response.factors}")

        rclpy.shutdown()

def main(args=None):
        rclpy.init(args=args)
        node=PrimeFactorClient()
        rclpy.spin(node)

if __name__ == '__main__':
        main()
