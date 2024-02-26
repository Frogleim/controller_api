import threading
import time
import serial

TimeToAnswer = 200
TimeToNextByte = 3

TRANSLATOR_ADDR = 0xF0
COM_TRANSLATOR_POLL = 0x00
COM_TRANSLATOR_RESET = 0x01
#COM_DISPENSE = 0x01

class TUSB(threading.Thread):
    def __init__(self, port_name, speed, modul_number, interval):
        super().__init__()
        self.port_name = port_name
        self.speed = speed
        self.modul_number = modul_number
        self.interval = interval
        self.modul = 0
        self.state_translator = 0
        self.port_rx_buf = bytearray(256)
        self.port = None
        self.timer_translator = None
        self.stopped = False  # Initialize stopped attribute to False
        self.thread_started = False  # Initialize thread_started attribute to False


    def process_translator(self):
        command = bytearray([TRANSLATOR_ADDR, COM_TRANSLATOR_POLL])
        count = self.send_to_port(command)

    def send_to_port(self, send):
        control = 0
        count = 0
        result = 0
        log_str = '(->)'
        for byte_to_send in send:
            control += byte_to_send
            self.port.write(bytes([byte_to_send]))
            log_str += f' {byte_to_send:02X}'
            count += 1
        self.port.write(bytes([control]))
        log_str += f' {control:02X}'

        dt_start = time.time()
        while True:
            if self.port.in_waiting == 0:
                if (time.time() - dt_start) * 1000 > TimeToAnswer:
                    print(log_str + ' устройство не отвечает!')
                    break
            else:
                if result == self.port.in_waiting:
                    print(result)
                    if (time.time() - dt_start) * 1000 > TimeToNextByte:
                        break
                else:
                    result = self.port.in_waiting
                    dt_start = time.time()
            time.sleep(0.001)

        if result > 0:
            received_data = self.port.read(result)
            log_str += ' (<-)'
            control = 0
            for byte_received in received_data:
                control += byte_received
                log_str += f' {byte_received:02X}'
            if len(received_data) > 1:
                log_str += f' (cs={control:02X})'
            print(log_str)

    def run(self):
        if self.timer_translator:
            self.timer_translator.start()
            print('Поток запущен...')
            while not self.stopped:  # Corrected condition
                time.sleep(1)
            self.timer_translator.cancel()
            print('Поток остановлен...')

    def start_timer(self):
        self.timer_translator = threading.Timer(self.interval / 1000, self.process_translator)
        self.timer_translator.start() 
    def connect(self):
        try:
            self.port = serial.Serial(self.port_name, baudrate=self.speed, timeout=0)
            print('Создание потока...')
            if not self.thread_started:  # Check if thread is not already started
                self.start()  # Start the thread
                self.thread_started = True  # Update thread_started flag
            print('Поток создан...')
        except Exception as e:
            print(str(e))

            
    def close(self):
        if self.timer_translator:
            self.timer_translator.cancel()
        if self.port:
            self.port.close()
        self.stopped = True  # Set stopped attribute to True when closing the thread
        print('Поток удален...')

# Usage:
if __name__ == "__main__":
    port_name = 'COM4'  # Replace with your actual port name
    speed = 9600  # Replace with your actual baudrate
    modul_number = 1  # Replace with your actual module number
    interval = 600  # Replace with your actual interval
    usb_thread = TUSB(port_name, speed, modul_number, interval)
    usb_thread.connect()
    #if (usb_thread.thread_started == False):
    #    usb_thread.start()
    usb_thread.send_to_port())
    print("Ready to send")
    #usb_thread.send_to_port(COM_DISPENSE)
    time.sleep(10)  # Run for 10 seconds for demonstration
    usb_thread.close()
