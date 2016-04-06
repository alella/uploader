#!/usr/bin/env python

import os
import re
import sys
import logging
import socket
import argparse
import subprocess
import inspect

from flask import *
from werkzeug import secure_filename

abs_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
abs_basedir = os.path.dirname(os.path.dirname(abs_file_path))
template_folder = os.path.join(abs_basedir, "templates")
static_folder = os.path.join(abs_basedir, "static")
app = Flask(__name__,
            template_folder=template_folder,
            static_folder=static_folder)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def parse_args():
    parser = argparse.ArgumentParser(description='Hosts temporary service to upload files.')
    parser.add_argument('-p',
                        '--port',
                        dest='port',
                        default=False,
                        help='Host service on this port if specified else, picks up a random port')
    
    parser.add_argument('-d',
                        '--dir',
                        dest='dir',
                        default=os.getcwd(),
                        help='Stores files in specified directory. Uses local directory by default')

    parser.add_argument('-g',
                        '--global',
                        dest='global_url',
                        action='store_true',
                        default=False,
                        help='Uses public url for uploading files')

    args = parser.parse_args()
    return args

def get_port(arg_port):
    if not arg_port:
        if os.path.exists('./.uploader_tmp'):
            port = open('.uploader_tmp').read()
            os.remove('./.uploader_tmp')
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("",0))
            s.listen(1)
            port = s.getsockname()[1]
            s.close()
    else:
        port = arg_port
        
    return port

def exists(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def write_port(port):
    with open('./.uploader_tmp', 'w') as w:
        w.write(str(port))

def launch_global_url(port):
    if not exists('ngrok'):
        print("Unable to find ngrok binary.")
        print("Public URLs cannot be used without ngrok (https://ngrok.com)")
        sys.exit(0)
        
    p = subprocess.Popen(['ngrok', '-log=stdout', str(port)], stdout=subprocess.PIPE)
    
    while True:
        line = p.stdout.readline()
        if line:
            if "Tunnel established at" in line:
                url = re.findall(r"Tunnel established at (.*)",line)[0]
                break
    return url

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print("Trying to fetch a file...")
    if request.method == 'POST':
        for file in request.files.getlist('file[]'):
            filename = secure_filename(file.filename)
            to_disk_file_name = os.path.join(app.config['UPLOAD_DIR'], filename)
            file.save(to_disk_file_name)
            print("File saved at {0}".format(to_disk_file_name))
            
    return ""

@app.route('/')
def home():
    if not app.config['isGlobal']:
        print("Service opened in {0}".format(request.remote_addr))

    return render_template('index.html')

if __name__ ==  "__main__":
    args = parse_args()
    host_ip = socket.gethostbyname(socket.gethostname())
    port = get_port(args.port)
    app.config['UPLOAD_DIR'] = args.dir
    app.config['isGlobal'] = args.global_url

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        if not app.config['isGlobal']:
            print("Started service on http://{0}:{1}".format(host_ip, port))
        else:
            global_url = launch_global_url(port)
            print("Started service on http://{0}:{1} on local network".format(host_ip, port))
            print("Public url is {0}".format(global_url))
    else:
        write_port(port)

    app.run(host='0.0.0.0', debug=True, port=port)
