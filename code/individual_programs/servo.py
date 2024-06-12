import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

servo_pin1 = 18
servo_pin2 = 17

# Set PWM parameters
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)
pwm1 = GPIO.PWM(servo_pin2, 50)  # 50 Hz (20 ms PWM period)
pwm2 = GPIO.PWM(servo_pin1, 50)

def angle_to_duty_cycle(angle):
    return (0.05 * angle) + 2.5

try:
    pwm1.start(angle_to_duty_cycle(80))
    # Keep the servo at 80 degrees for 1 second
    time.sleep(1)
    pwm1.start(angle_to_duty_cycle(100))
    # Keep the servo at 110 degrees for 1 second
    time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    pwm1.stop()
    GPIO.cleanup()
