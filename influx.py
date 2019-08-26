import urequests

class Influx:

    def __init__(self, addr, mac, db_name, username, password):
        self.addr = addr
        self.db_name = db_name
        self.instance = mac
        self.username = username
        self.password = password
        self.db_string = "http://{}:8086/write?db={}&u={}&p={}".format(self.addr,
                                                                       self.db_name,
                                                                       self.username,
                                                                       self.password)

    def send(self, keyValues):
        resp_data = ""
        try:
            for k, v in keyValues.items():
                if len(resp_data):
                    resp_data += " \n "
                resp_data += "{},location={} value={:.2f}".format(k, self.instance, v)

            print("To:\n" + self.db_string)
            print("Req:\n" + resp_data)

            resp = urequests.post(self.db_string, data=resp_data)

            print('response: {}'.format(resp.status_code))

            if resp.status_code == 204:
                print('TX: OK')
            else:
                print('TX: ERR')
        except Exception as e:
            print('Error: {}'.format(e))
