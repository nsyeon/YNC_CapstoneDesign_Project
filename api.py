from flask import Flask, request, render_template
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import datetime, time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.HIGH)

servo_pin = 13
servo_pin2 = 12

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)

reader = SimpleMFRC522() 

@app.route('/', methods=['GET']) 
def Home():
    return render_template("./index.html")

@app.route('/give', methods=['GET']) 
def Open():
    #리더
    try:
        print("카드를 인식시켜 주세요...")
        id , text = reader.read()
        print("아이디 :", id)

        if id == 395560176182 :
            GPIO.output(17,GPIO.LOW)
            time.sleep(10.0)
            GPIO.output(17,GPIO.HIGH)

    finally: 
        return ""

@app.route('/n_tag', methods=['GET']) 
def Close():
    pwm = GPIO.PWM(servo_pin, 49)
    pwm2 = GPIO.PWM(servo_pin2, 49)

    pwm.start(0.75)
    pwm2.start(0.75)

    pwm.ChangeDutyCycle(7)
    pwm2.ChangeDutyCycle(7)
    time.sleep(5.0)

    pwm.ChangeDutyCycle(10.0)
    pwm2.ChangeDutyCycle(4.0)
    time.sleep(5.0)

    pwm.ChangeDutyCycle(7)
    pwm2.ChangeDutyCycle(7)
    time.sleep(1.5)

    return ""

@app.route('/y_tag', methods=['GET'])
def Turn():
    pwm = GPIO.PWM(servo_pin, 49)
    pwm2 = GPIO.PWM(servo_pin2, 49)

    pwm.start(0.75)
    pwm2.start(0.75)

    pwm.ChangeDutyCycle(7)
    pwm2.ChangeDutyCycle(7)

    #리더
    try:
        print("카드를 인식시켜 주세요...")
        id , text = reader.read()
        print("아이디 :", id)

        if id == 395560176182 :
            time.sleep(5.0)
            pwm.ChangeDutyCycle(4.0)
            pwm2.ChangeDutyCycle(10.0)
            time.sleep(5.0)

    finally: 
        pwm.ChangeDutyCycle(7)
        pwm2.ChangeDutyCycle(7)
        time.sleep(1.5)
        pwm.stop()
        pwm2.stop()

    return ""

try:
    if __name__ == "__main__" :     # app이 main 프로젝트이면 실행하라
        app.run(host='0.0.0.0', port=8080, debug=True)
finally:
    GPIO.cleanup()