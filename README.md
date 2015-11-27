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
Started service on http://192.168.1.143:46186
```
you should be now able to open the url from any system in the local network to upload files using the mentioned link.

![](http://s23.postimg.org/8enu1k8vf/2015_11_28_031853_307x35_scrot.png)

Public urls can also be generated provided [ngrok](https://ngrok.com/) is installed.

```
usage: uploader [-h] [-p PORT] [-d DIR] [-g]

Hosts temporary service to upload files.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Host service on this port if specified else, picks up
                        a random port
  -d DIR, --dir DIR     Stores files in specified directory. Uses local
                        directory by default
  -g, --global          Uses public url for uploading files
```
