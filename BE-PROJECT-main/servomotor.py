from flask import Flask,render_template,request  #importing the flask module
import RPi.GPIO as GPIO
from time import sleep
servo_pin = 2
GPIO.setmode(GPIO.BCM)

#defining servo pin as output pin
GPIO.setup(servo_pin, GPIO.OUT)
p = GPIO.PWM(servo_pin, 50)
p.start(0)
app = Flask(__name__)




@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test",methods=["POST"])
def test():
    slider = request.form["slider"]
    p.ChangeDutyCycle(float(slider))
    sleep(1)
    p.ChangeDutyCycle(0)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
