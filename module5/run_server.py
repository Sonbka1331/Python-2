import sys
import subprocess


sys.path.insert(1, "../module_4")
from app import app


def start_server():
    data = sys.argv[1]
    if data.isdigit():
        port = int(data)
    else:
        print('Invalid port value')
        return 1
    command = f"lsof -i:{port}"
    result_obj = subprocess.run(command, capture_output=True, shell=True)
    result = result_obj.stdout.decode()
    if result == '':
        app.run()
    else:
        command = f'sudo fuser -k {port}/tcp'
        subprocess.run(command, capture_output=True, shell=True)
        app.run(debug=True, port=port)


if __name__ == '__main__':
    start_server()
