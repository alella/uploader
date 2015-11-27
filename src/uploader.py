import os
import logging
import socket
import argparse

from flask import *
from werkzeug import secure_filename

app = Flask(__name__)
app.config['UPLOAD_DIR'] = os.getcwd()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def parse_args():
    parser = argparse.ArgumentParser(description='Hosts temporary service to upload files.')
    parser.add_argument('-p',
                        '--port',
                        dest='port',
                        default=False,
                        help='Host service on this port')

    args = parser.parse_args()
    return args

def get_port(arg_port):
    if not arg_port:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
    else:
        port = int(arg_port)
        
    return port

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print("Trying to fetch file...")
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        to_disk_file_name = os.path.join(app.config['UPLOAD_DIR'], filename)
        file.save(to_disk_file_name)
        
    print("File saved at {0}".format(to_disk_file_name))
    return "File saved at {0}".format(to_disk_file_name)

@app.route('/')
def home():
    print("Service opened in {0}".format(request.remote_addr))
    return """<form method=POST enctype=multipart/form-data action="/upload">
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>"""

if __name__ ==  "__main__":
    args = parse_args()
    host_ip = socket.gethostbyname(socket.gethostname())
    port = get_port(args.port)
    
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print("Started service on http://{0}:{1}".format(host_ip, port))
        
    app.run(host='0.0.0.0', debug=True, port=port)
