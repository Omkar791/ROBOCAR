from flask import Flask,jsonify, Response ,make_response, render_template , request

import cv2
#import time
#import RPi.GPIO as GPIO
#mode=GPIO.getmode()

import pygame

import sys
import time
import RPi.GPIO as GPIO

mode=GPIO.getmode()

GPIO.cleanup()

Forward=26
fwd = 19
backward=20
bkd = 16
servo_pin = 2

sleeptime=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(fwd, GPIO.OUT)
GPIO.setup(backward, GPIO.OUT)
GPIO.setup(bkd, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)

p = GPIO.PWM(servo_pin,50)
p.start(0)


def playaudio(audio):
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue



#from playsound import playsound    for windows only



app = Flask(__name__)
video = cv2.VideoCapture(0)

face_cascade  = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


@app.route('/',methods=['GET',"POST"])
def slider():
    
    if request.method == "POST":
        slider = request.form.get('slider')
        return render_template('index.html',slider=slider)
        
    return render_template('index.html')


@app.route('/<int:no>')
def motar(no):
    if no == 1:
        GPIO.output(Forward, GPIO.HIGH)
        GPIO.output(fwd, GPIO.HIGH)
        print("up key is pressed")
        time.sleep(1)
        GPIO.output(Forward, GPIO.LOW)
        GPIO.output(fwd, GPIO.LOW)
    elif no == 2:
        GPIO.output(backward, GPIO.HIGH)
	    GPIO.output(bkd, GPIO.HIGH)
	    print("Moving Backward")
	    time.sleep(1)
	    GPIO.output(backward, GPIO.LOW)
	    GPIO.output(bkd, GPIO.LOW)
        print('down key is pressed')
    elif no == 3:
        GPIO.output(Forward, GPIO.HIGH)
        print(" moving left ")
        time.sleep(0.5)
        GPIO.output(Forward, GPIO.LOW)
        print('left key is pressed')
    elif no == 4:
        GPIO.output(fwd, GPIO.HIGH)
        print("Moving right")
        time.sleep(0.5)
        GPIO.output(fwd, GPIO.LOW)
        print('right key is pressed')
    
    elif no == 5:
	print('5th key is pressed')
	playaudio(audio='voice.mp3')
    return render_template('index.html')


def gen(video):
    while True:
        success, image = video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_in_image = face_cascade.detectMultiScale(gray , 1.3 ,5)
        #print(faces_in_image)
        for (x,y,w,h) in faces_in_image:
            cv2.rectangle(image , (x,y),(x+w,y+h),(0,255,0),2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

'''
@app.route('/<int:id>')
def audio(id):
    if id == 4:
        playsound('voice.mp3')    
    else:
        print('none')
    return render_template('index.html')

'''


@app.route('/slider',methods=['GET','POST'])
def slider_op():
    #print('endpoint is called')
    #print('debug1')
    if request.method == "POST":
        #print('debug')
        req = request.get_json()
        #print(req)
        
        res = make_response(jsonify({'message':'json_received'}),200)
        print(req['name'])
        p.ChangeDutyCycle(float(req['name']))
        time.sleep(1)
        p.ChangeDutyCycle(0)
    return render_template('index.html')




@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=True,port=8000)
