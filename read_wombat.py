#
# -----** Coil Lab **-----
# wombatpi.net
# Interface to wombat pi
# (running diagnostics application on the arduino)
#
# Modified 29-Oct-2024
#
#
import serial
import time
import threading

BAUDRATE = 115200
SERIAL_PORT = 'COM9'

dataList = []

RUNNING = True

class MODE:
    SCAN_1USEC = "MT\r"
    SCAN_3USEC = "MU\r"

class SerialInterface:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial()
        self.stop_polling = False

    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Connected to {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting: {e}")

    def _disconnect(self):
        self.stop_polling = True
        self.ser.close()
        print(f"Disconnected from {self.port}")

    def send_command(self, command):
        try:
            self.ser.write(command.encode())
            time.sleep(0.1)  # Wait for response
        except serial.SerialException as e:
            print(f"Error sending command: {e}")

    def read_response(self):
        response = ''
        while self.ser.in_waiting > 0:
            response += self.ser.read(self.ser.in_waiting).decode()
        return response

    def read_data(self, num_bytes):
        return self.ser.read(num_bytes)


# the data is a line of comma delimited values
#
def _parse_line_csv(line_text):
    """
    Convert received line text into a list of numbers.

    Args:
        line_text (str): Received text from serial device.

    Returns:
        list[float]: List of numbers extracted from line text.
    """
    # Remove leading/trailing whitespace and newline characters
    line_text = line_text.strip()

    # Split text into individual values (comma-delimited)
    values = line_text.split(",")

    num_list = []
    for val in values:
        try:
            num_list.append(float(val))
        except ValueError as e:
            None

    return num_list


def _parse_line_text(line_text):
    """
    Convert received line text into a list of numbers.

    Args:
        line_text (str): Received text from serial device.

    Returns:
        list[float]: List of numbers extracted from line text.
    """
    # Remove leading/trailing whitespace
    line_text = line_text.strip()

    # Split text into individual lines
    lines = line_text.splitlines()

    # Convert lines to floats (or ints if applicable)
    num_list = [float(line) for line in lines]

    return num_list


data_lock = threading.Lock()

def _poll(si):
    global dataList
    global RUNNING

    while(RUNNING):
        time.sleep(0.1)

        try:
            if si.ser.in_waiting > 0:
                time.sleep(0.05)
                response = si.read_response()
                #print(response)

                with data_lock:
                    dataList = _parse_line_csv(response)

                #print("read : " + str(len(dataList)))


        except serial.SerialException as e:
            print(f"Error polling: {e}")
            break

    print("Serial port closed")

    # finished / stopped
    si._disconnect()


# called from external module/application
def getData():
    with data_lock:
        return dataList.copy()



def runSerial(mode):
    si = SerialInterface(SERIAL_PORT)
    si._connect()
    si.send_command(mode)

    thread = threading.Thread(target=_poll, args=(si,))
    thread.start()

# To finsih the polling task and close the serial port
def close():
    global RUNNING
    RUNNING = False



# Example usage:
if __name__ == "__main__":
    runSerial(MODE.SCAN_3USEC)

