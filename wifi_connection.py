from wifi import Cell, Scheme

class WifiConnection:
    def setup(self):
        try:
            cell = Cell.all('wlan0')[0]
            scheme = Scheme.for_cell('wlan0', 'home', cell)
            scheme.save()
            scheme.activate()
        except:
            pass
