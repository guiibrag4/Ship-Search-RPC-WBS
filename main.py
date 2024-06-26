import multiprocessing
import os

def run_rpc_server():
    os.system('python server/RPC_server.py')

def run_websocket_server():
    os.system('python server/websocket_server.py')

def run_client():
    os.system('python client/client.py')

def run_web_server():
    os.system('python server/web_server.py')

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_rpc_server)
    p2 = multiprocessing.Process(target=run_websocket_server)
    p3 = multiprocessing.Process(target=run_client)
    p4 = multiprocessing.Process(target=run_web_server)

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()