#!/usr/bin/env python

import os
import re
import sys
from logging import getLogger
import socket
import argparse
import subprocess
import inspect
from netifaces import interfaces, ifaddresses, AF_INET

from flask import *
from werkzeug import secure_filename

abs_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
abs_basedir = os.path.dirname(os.path.dirname(abs_file_path))
template_folder = os.path.join(abs_basedir, "templates")
static_folder = os.path.join(abs_basedir, "static")
app = Flask(__name__,
            template_folder=template_folder,
            static_folder=static_folder)

log = getLogger('werkzeug')
log.setLevel(40)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Hosts temporary service to upload files.')
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

    args = parser.parse_args()
    return args


def get_port(arg_port):
    if not arg_port:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
    else:
        port = arg_port
    return int(port)


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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print("Trying to fetch a file...")
    if request.method == 'POST':
        for file in request.files.getlist('file[]'):
            filename = secure_filename(file.filename)
            to_disk_file_name = os.path.join(
                app.config['UPLOAD_DIR'], filename)
            file.save(to_disk_file_name)
            print("File saved at {0}".format(to_disk_file_name))

    return ""


def print_ip_sockets(port):
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(
            ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        print '{0}: http://{1}:{2}'.format(
            ifaceName, addresses[0], port
        )


@app.route('/')
def home():
    print("Service opened in {0}".format(request.remote_addr))

    return render_template('index.html')


if __name__ == "__main__":
    args = parse_args()
    port = get_port(args.port)
    app.config['UPLOAD_DIR'] = args.dir

    print_ip_sockets(port)

    app.run(host='0.0.0.0', debug=False, port=port)
