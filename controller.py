import serial
import time 
# Define the necessary constants
ADDR = 0xf1  # Replace with the address of your device
RESET_COM = 0x01
COM = 0x02 #COM_EXTANTION_DISPENSE = $02;   
CS = 0x04  # Replace with the correct checksum calculation
NDECK = 1  # Replace with the actual shelf number
NDISP = 5  # Replace with the actual spiral number
VAL = 0x01   # Replace with the value to turn up (1 to 10)

COM_PORT = '/dev/ttyACM0'  # Replace with your actual COM port name
BAUD_RATE = 9600
COMMAND_BYTES = b'\xF0\x00\xF0'
COM_TRANSLATOR_POLL = 0x00
COM_EXTANTION_RESET = 0x01


def reset_devices():
    # Reset translator
    checksum = calculate_checksum([ADDR, COM_EXTANTION_RESET])
    command = bytes([ADDR, COM_EXTANTION_RESET, checksum])
    print("Send RESET_CONTROLLER command!")
    response = send_command(command)
    print("Response from controller:", response)

    # Wait for devices to reset
    time.sleep(1)


def send_command(command):
    ser = serial.Serial(COM_PORT, baudrate=BAUD_RATE)
    ser.timeout = 4.3
    ser.write(command)
    #response = ser.read(1)
    response_all =  ser.readlines()

    response = ser.read(2)
    ser.close()
    print(f'All response: {response_all}')
    return response

def send_command_and_read_all(command):
    ser = serial.Serial(COM_PORT, baudrate=BAUD_RATE)
    ser.timeout = 4.3
    ser.write(command)
    response = ser.readline()
    ser.close()
    return response

# Function to calculate the checksum byte for a command
def calculate_checksum(cmd):
    return sum(cmd) % 256

# Function to send the turn up command
def turn_up_spring():
    checksum = calculate_checksum([ADDR, COM, NDECK, NDISP, VAL])
    command = bytes([ADDR, COM, NDECK, NDISP, VAL, checksum])
    print("Send command!")
    response = send_command(command)
    print(response)
    response = get_state()
    return response

def get_good(ndeck=None, ndisp=None):
    checksum = calculate_checksum([ADDR, COM, ndeck, ndisp])
    command = bytes([ADDR, COM, ndeck, ndisp, checksum])

    print("Send GET_GOOD command!")
    response = send_command(command)
    print('Status: ', response)
    response = get_state()
    print('State: ', response)
    return response

def get_state():
    checksum = calculate_checksum([ADDR, COM_TRANSLATOR_POLL])
    command = bytes([ADDR, COM_TRANSLATOR_POLL, checksum])
    response = send_command_and_read_all(command)
    return response



# Main program
if __name__ == '__main__':
    print('-------------------')
    reset_devices()
