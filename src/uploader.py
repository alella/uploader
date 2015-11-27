from flask import *
from werkzeug import secure_filename
import os
import logging
import socket

app = Flask(__name__)
app.config['PORT'] = 50960
app.config['UPLOAD_DIR'] = os.getcwd()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print "Trying to fetch file..."
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        to_disk_file_name = os.path.join(app.config['UPLOAD_DIR'], filename)
        file.save(to_disk_file_name)
        
    print "File saved at {0}".format(to_disk_file_name)
    return "File saved at {0}".format(to_disk_file_name)

@app.route('/')
def home():
    print "Service opened in {0}".format(request.remote_addr)
    return """<form method=POST enctype=multipart/form-data action="/upload">
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>"""

if __name__ ==  "__main__":
    host_ip = socket.gethostbyname(socket.gethostname())
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print "Started service on http://{0}:{1}".format(host_ip,
                                                         app.config['PORT'])
    app.run(host='0.0.0.0', debug=True, port=app.config['PORT'])
