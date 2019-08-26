import network
import time

class Wifi:
    def __init__(self, ssid, passw, dhcp=True):
        self.ssid = ssid
        self.passw = passw

        self.ifce = network.WLAN(network.STA_IF)
        self.ifce.active(True)

    def Connect(self, blocking=True, timeout_ms=20000):

        if not self.Connected():
            self.ifce.connect(self.ssid, self.passw)

            if blocking:
                start_time = time.ticks_ms()

                while not self.Connected():
                    self.ifce.connect(self.ssid, self.passw)
                    now = time.ticks_ms()
                    if now > (start_time + timeout_ms):
                        return False
                    time.sleep_ms(100)

        return self.Connected()

    def Connected(self):
        return self.ifce.isconnected()

    def GetConfig(self):
        return self.ifce.ifconfig()

    def Scan(self):
        return self.ifce.scan()

    def Status(self):
        return self.ifce.status()

    def GetMac(self):
        try:
            return "_".join([hex(b)[2:] for b in self.ifce.config('mac')])
        except Exception as e:
            return ""
