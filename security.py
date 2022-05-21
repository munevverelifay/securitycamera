from picamera import PiCamera
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import RPi.GPIO as GPIO
import time

camera = PiCamera()

sender_address ='*****@gmail.com'
sender_pass ='*****'
receiver_address ='**@gmail.com'

message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A picture taken by Pi camera module. It has an attachment.'

GPIO.setmode(GPIO.BCM)
GPIO_PIR = 7

GPIO.setup(GPIO_PIR,GPIO.IN)
Current_State  = 0
Previous_State = 0
try:
    while GPIO.input(GPIO_PIR)==1:
        Current_State = 0

    while True:
        Current_State = GPIO.input(GPIO_PIR)
        if Current_State==1 and Previous_State==0:
            Previous_State==1
            while True:
                pic = '/home/pi/Desktop/img.jpg'
                camera.start_preview()
                sleep(5)
                camera.capture(pic)
                camera.stop_preview()
                print('Hareket Algilandi ve Fotograf Cekildi')
                File = open(pic, 'rb')
                img = MIMEImage(File.read())
                File.close()
                message.attach(img)

                session = smtplib.SMTP('smtp.gmail.com', 587)
                session.starttls()
                session.login(sender_address, sender_pass)
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)
                session.quit()
                print('FOTOGRAF MAIL OLARAK GONDERILDI')
            Previous_State=1
        elif Current_State==0 and Previous_State==1:
            print('Hareket Algılanmadı')
            Previous_State=0
        time.sleep(0.01)
except KeyboardInterrupt:
  print("Quit")
    
  GPIO.cleanup()