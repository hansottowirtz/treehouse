import lights
import pixels

import threading
import signal
import time
import wifi_connection

class Treehouse:
    def setup(self):
        signal.signal(signal.SIGINT, self.close) # on KeyboardInterrupt etc.
        wc = WifiConnection()
        wc.setup()

    def close(self):
        print 'Closing Treehouse'
        self.pxls.close()

    def start_pixels(self):
        self.pxls = None
        try:
            self.pxls = pixels.Pixels()
            pxls_thread = threading.Thread(target=self.handle_pixels)
            # pxls_thread.daemon = True
            pxls_thread.start()
        except KeyboardInterrupt:
            self.close()

    def handle_pixels(self):
        try:
            print 'Started pixels thread'
            self.pxls.start()
            self.pxls.recorder.request_frame(self.test)
        except KeyboardInterrupt:
            self.close()

    def test(self, *args):
        print 'testje xp'
        self.pxls.recorder.request_frame(self.test)


if __name__ == '__main__':
    th = Treehouse()
    th.setup()
    signal.signal(signal.SIGINT, th.close)
    th.start_pixels()
