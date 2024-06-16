import time
import rpyc
import slave_service
import threading, sys
from rpyc.utils.server import ThreadedServer
from load_balancer import LoadBalancer

class MasterService(rpyc.Service):
    def exposed_find(self, option, input_spec=None):
        service, ip, port = balance_service.forward_request()
        c2 = rpyc.connect_by_service(service)
        response = c2.root.get_answer(option, input_spec)
        return response


class ServerThread(threading.Thread):
    def __init__(self, service, port):
        threading.Thread.__init__(self)
        self.service = service
        self.port = port
        self.server = ThreadedServer(self.service, port=self.port, auto_register=True)

    def run(self):
        print(f"Server is starting on port {self.port}...")
        self.server.start()
    
    def stop(self):
        self.server.close()
        print(f"Stop running")


if __name__ == "__main__":
    try:

        slave_name = "Slave1"
        SlaveServiceClass = slave_service.create_slave_service_class(slave_name)
        slave_thread1 = ServerThread(SlaveServiceClass, port=18862)
        slave_thread1.start()

        slave_name = "Slave2"
        SlaveServiceClass = slave_service.create_slave_service_class(slave_name)
        slave_thread2 = ServerThread(SlaveServiceClass, port=18863)
        slave_thread2.start()

        time.sleep(1)

        balance_service = LoadBalancer()
        server_thread = ServerThread(MasterService, port=18861)
        server_thread.start()

        # Stop terminal run
        while True:
            # Keep the main thread alive to catch KeyboardInterrupt
            threading.Event().wait(1)
    
    except KeyboardInterrupt:
        print("Shutting down...")
        server_thread.stop()
        slave_thread1.stop()
        slave_thread2.stop()
        sys.exit(0)