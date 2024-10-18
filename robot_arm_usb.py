import serial
import time
import tkinter as tk

arduino = serial.Serial('/dev/tty.usbmodem101', 9600, timeout=1)
time.sleep(2)  # Espera a que la conexión serial se inicialice

starting_position = [90, 180, 140, 90, 50, 40]

def send_angle(servo, angle):
    if 0 <= angle <= 180 and 1 <= servo <= 6:
        command = f'{servo}{(angle)}\n'
        arduino.write(command.encode())
        print(f'Sent angle {angle} to servo {servo}')
        wait_for_ack()
    else:
        print('Invalid angle or servo number')

def wait_for_ack():
    while True:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode('utf-8').strip()
            if response == "ACK":
                print("ACK received")
                break
            else:
                print(f"Unexpected response: {response}")
        else:
            print("Waiting for ACK")

def set_starting_position():
    starting_position = [90, 180, 140,90,50,40]
    for i, pos in enumerate(starting_position):
        send_angle(i+1,pos)

def increase_angle(servo, scale):
    current_angle = scale.get()
    new_angle = min(current_angle + 10, 180)
    scale.set(new_angle)
    send_angle(servo, new_angle)

def decrease_angle(servo, scale):
    current_angle = scale.get()
    new_angle = max(current_angle - 10, 0)
    scale.set(new_angle)
    send_angle(servo, new_angle)

def create_button(frame, text, command):
    button = tk.Button(frame, text=text, command=command)
    button.pack(side=tk.LEFT, padx=5, pady=5)

def create_arrow_buttons(frame, servo, scale):
    left_button = tk.Button(frame, text="◀", repeatdelay=50, repeatinterval=50, command=lambda: decrease_angle(servo, scale))
    left_button.pack(side=tk.LEFT)
    right_button = tk.Button(frame, text="▶", repeatdelay=50, repeatinterval=50, command=lambda: increase_angle(servo, scale))
    right_button.pack(side=tk.LEFT)
    return left_button, right_button


# GUI
root = tk.Tk()
root.title("Servo Motor Control")

servo_frames = [tk.Frame(root) for _ in range(6)]
servo_labels = [tk.Label(frame, text=f'Servo {i+1}') for i, frame in enumerate(servo_frames)]
servo_scales = [
    tk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL) if i != 1 
    else tk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL , command=lambda value, i=i: send_angle(i+1, int(value))) 
    for i, frame in enumerate(servo_frames)
]
servo_buttons = [tk.Button(frame, text='Set Angle', command=lambda i=i: send_angle(i+1, servo_scales[i].get())) for i, frame in enumerate(servo_frames)]

for i in range(6):
    servo_frames[i].pack(pady=10)
    servo_labels[i].pack(side=tk.LEFT)
    create_arrow_buttons(servo_frames[i], i+1, servo_scales[i])
    servo_scales[i].pack(side=tk.LEFT, padx=5)
    servo_buttons[i].pack(side=tk.LEFT, padx=5)
    servo_scales[i].set(starting_position[i])
    

# Add button to set starting position
starting_position_frame = tk.Frame(root)
starting_position_frame.pack(pady=10)
starting_position_button = tk.Button(starting_position_frame, text='Set Starting Position', command=set_starting_position)
starting_position_button.pack(pady=10)

root.mainloop()

# Cierra la conexión serial al terminar
arduino.close()
