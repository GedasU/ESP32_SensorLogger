import time
from display import Display
from sensor import BME
from wifi import Wifi
from influx import Influx


INFLUXDB_ADDR = "192.168.1.40"
INFLUXDB_USER = "templogger"
INFLUXDB_PASS = "micropython"
INFLUXDB_DB = "sensors"

def StartupBanner(output):
    output.Clear()
    output.WriteLine("ESP Temperature", 0)
    output.WriteLine("  logger", 1)
    output.Display()
    print("ESP Temperature logger")


def InitialWaitForWifi(display):
    progress = ""
    while not wifi.Connected():
        display.Clear()
        progress += "."
        if len(progress) >= 16:
            progress = ""
        display.WriteLine(progress, 0)
        display.WriteLine("Connecting to:", 1)
        display.WriteLine("    {}".format(SSID), 2)
        display.Display()
        print("Wifi connecting... {}".format(SSID))
        wifi.Connect(blocking=False)
        time.sleep_ms(1000)


def MainLoop(wifi, db, oled, sensor):
    sensor.Read()
    sensor.Test()

    oled.Clear()
    oled.WriteLine("Temp {:.1f} degC".format(sensor.temp), 0)
    oled.WriteLine("Pressure {:.0f} hPa".format(sensor.pressure), 1)
    oled.WriteLine("Humidity {:.0f} %".format(sensor.humidity), 2)

    log = {
        "temperature": sensor.temp,
        "pressure": sensor.pressure,
        "humidity": sensor.humidity
    }
    if wifi.Connected():
        oled.WriteLine("Wifi:", 3)
        oled.WriteLine(wifi.GetConfig()[0], 4)
        print("Wifi {}".format(wifi.GetConfig()[0]))

        db.send(log)

    else:
        oled.WriteLine("Wifi Down", 3)

    oled.Display()

    if not wifi.Connected():
        wifi.Connect(blocking=False)


wifi = Wifi(SSID, PASS)
wifi.Connect(blocking=False)
oled = Display(row_pitch=13)
sensor = BME()
db = Influx(INFLUXDB_ADDR, wifi.GetMac(), INFLUXDB_DB, INFLUXDB_USER, INFLUXDB_PASS)

StartupBanner(oled)
time.sleep(1)
InitialWaitForWifi(oled)

while True:
    MainLoop(wifi, db, oled, sensor)

    time.sleep(3)
