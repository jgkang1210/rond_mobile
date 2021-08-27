import serial
import time

print("UART Demonstration Program")
print("NVIDIA Jetson Nano Developer Kit")


serial_port = serial.Serial(
    port="/dev/ttyACM0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

while 1:
    # Wait a second to let the port initialize
    time.sleep(1)

    serial_port.write(bytes(bytearray([0xC0])))

serial_port.close()
