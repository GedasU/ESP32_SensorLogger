import machine
import ssd1306

class Display:

    row_height = 15

    def __init__(self, row_pitch=15):
        self.reset = machine.Pin(16, machine.Pin.OUT)
        self.reset.off()
        self.reset.on()

        self.row_height = row_pitch

        self.i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)

        self.Clear()

    def Clear(self):
        self.oled.fill(0)
        self.oled.show()

    def Display(self):
        self.oled.show()

    def WriteLine(self, msg="", row=0):
        self.oled.text(msg, 0, row * self.row_height)