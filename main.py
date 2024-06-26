import subprocess

# Inicia o servidor RPC
rpc_process = subprocess.Popen(['python', 'server/RPC_server.py'])

# Inicia o servidor WebSocket
websocket_process = subprocess.Popen(['python', 'server/websocket_server.py'])

# Inicia o servidor Web para servir o HTML
web_server_process = subprocess.Popen(['python', 'server/web_server.py'])

# Espera os processos terminarem
rpc_process.wait()
websocket_process.wait()
web_server_process.wait()
