
from flask import Flask, Response , render_template, request
import cv2
import time
app = Flask(__name__)
video = cv2.VideoCapture(-1)

import RPi.GPIO as GPIO
from time import sleep


mode=GPIO.getmode()
#GPIO.cleanup()

#   motar initial code 
Forward=26
Backward=21
sleeptime=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)
GPIO.setwarnings(False)

# motar initial code end 


# servo initial code start 
servo_pin = 19 
GPIO.setmode(GPIO.BCM)
#defining servo pin as output pin
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setwarnings(False)
p = GPIO.PWM(servo_pin, 50)
p.start(0)

# servo initial code end here

face_cascade  = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#maskNet = load_model('')
@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "POST":
        slider = request.form["slider"]
        print(slider)
        p.ChangeDutyCycle(float(slider))
        sleep(1)
        p.ChangeDutyCycle(0)
    return render_template('index.html')



@app.route('/<int:no>',methods=['GET' , 'POST'])
def motar(no):
    if no == 1:
        GPIO.output(Forward, GPIO.HIGH)
        print("Moving Forward")
        time.sleep(5)
        GPIO.output(Forward, GPIO.LOW)
        

    elif no == 2:
        print('down key is pressed ')
    elif no ==3:
        print('left key is pressed')
    elif no == 4:
        print('right key is pressed')

    return render_template('index.html')



def gen(video):
    while True:
        success, image = video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_in_image = face_cascade.detectMultiScale(gray, 1.3 ,5)
        #print(faces_in_image)
        for (x,y,w,h) in faces_in_image: 
            cv2.rectangle(image , (x,y),(x+w,y+h),(0,255,0),2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False,threaded=True)
