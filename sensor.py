import machine
import bme280_float

class BME:
    def __init__(self):
        self.i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
        self.sensor = bme280_float.BME280(address=0x76, i2c=self.i2c)

        self.temp = -1
        self.pressure = -1
        self.humidity = -1

    def Read(self):
        self.temp, self.pressure, self.humidity = self.sensor.read_compensated_data()
        self.pressure /= 100

    def Test(self):
        print(str(self.sensor.values))