Uploader
========

A very simple tool to upload files to your system.

##### Step 1
Install the tool
```
pip install git+git://github.com/alella/uploader
```

##### Step 2
Start the service
```
$ uploader
lo: http://127.0.0.1:5050
wlp58s0: http://192.168.1.8:5050
Destination dir: /tmp
...
```
You should be now able to open the url from any system in the local network to upload files using the mentioned link. Simply drag and drop files to upload.

![](https://raw.githubusercontent.com/alella/uploader/master/screenshot.png)


```
usage: uploader [-h] [-p PORT] [-d DIR]

Hosts temporary service to upload files.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Host service on this port if specified else, picks up
                        a random port
  -d DIR, --dir DIR     Stores files in specified directory. Uses local
                        directory by default
```
