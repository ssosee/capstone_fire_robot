# -*- coding: utf-8 -*-
import io
import picamera
import logging
import socketserver
import RPi.GPIO as GPIO
import time
from threading import Condition
from http import server
print(GPIO.VERSION)

title = 'Picmaera StreamingService Demo'

PAGE="""
<!doctype html>
<html>
    <head>
    <meta charset="utf-8">
    <title>PiCam Service</title>
    </head>
        <style>
            h1{
            margin-bottom: 0px;
            color:red;
            text-align: center;
            padding-top: 5px;
            padding-right: 5px;
            padding-left: 5px;
            padding-bottom: 5px;
            font-size:33px;
            }
            div{
            margin-top: 10px;

            text-align: center;
            padding-top: 5px;
            padding-right: 5px;
            padding-left: 5px;
            padding-bottom: 5px;

            border-width: medium;
            border: 10px solid blue;
            }
        </style>
    <body>
    <h1>Picmaera StreamingService Demo</h1>
    <script type="text/python3" src="fire2.py"></script>
    <input type ="button" value="fire" onclick =" document.querySelector('h1').style.background = 'pink';
    document.querySelector('h1').style.color = 'red';
  ">
    <input type ="button" value="nothing" onclick ="  document.querySelector('h1').style.background = 'skyblue';
    document.querySelector('h1').style.color = 'red';
  ">
        <div>
            <img src="stream.mjpg" width="100%" height="85%" />
        </div>
        <!--Start of Tawk.to Script-->
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/5b8004f4afc2c34e96e7de2a/default';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
<!--End of Tawk.to Script-->
    </body>
</html>
"""
GPIO.setmode(GPIO.BCM)
di_fire = 25
globalCounter = 0
GPIO.setup(di_fire, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def myInterrupt(channel):
    global globalCounter
    globalCounter += 1
    state = GPIO.input(di_fire)
    #di_fire 를 읽는다.
    if state:
        print ("Nothing :)\n")
        print(state)
    else:
        print("hello fire! :(\n")
        print(state)

#4번 핀이 OFF될 때 myInterrupt 함수를  통해 인터럽트를 받겠다는 요청
#GPIO.FALLING은 ON 상태에서 OFF로 변경될 때 시그널을 받겠다는 의미
#GPIO.add_event_detect(di_fire, GPIO.FALLING, callback=myInterrupt)
GPIO.add_event_detect(di_fire, GPIO.BOTH, callback=myInterrupt)

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    #HTTP 요청을 처리하는 클래스
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/Picam.html')
            self.end_headers()
        elif self.path == '/Picam.html':
            print("Picam.html")
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html') #html
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            print("stream.mjpg")
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    print("while")
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='1280x720', framerate=60) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        print("picam")
        address = ('', 8080)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
