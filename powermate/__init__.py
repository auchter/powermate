"""
pypowermate: python library for Griffin Powermate Bluetooth controllers
"""
from bluepy import btle
import struct
import threading
import time

# Hardcoding these handles probably isn't the right way to do this. Instead, we
# should discover these via UUID. However, bluepy's API isn't expressive enough
# to support this.
BATTERY_VAL_HND = 0x25
BATTERY_CC_HND = 0x26
LED_VAL_HND = 0x29
KNOB_VAL_HND = 0x2c
KNOB_CC_HND = 0x2d


class PowermateDelegate(object):
    def on_connect(self):
        """Called when a connection is established to the Powermate"""
        pass

    def on_disconnect(self):
        """
        Called when connection to the Powermate is lost. Most frequently, this
        occurs when the Powermate has gone to sleep, or is out of range
        """
        pass

    def on_battery_report(self, val):
        """
        Called when the Powermate sends a battery report. The parameter is the
        battery percentage remaining
        """

    def on_press(self):
        """Called when the wheel is pressed and released quickly"""
        pass

    def on_long_press(self, t):
        """
        Called when the wheel is long-pressed; t will be the time it was
        depressed, from 1 to 6 seconds
        """
        pass

    def on_clockwise(self):
        """Called when the wheel is rotated clockwise"""
        pass

    def on_counterclockwise(self):
        """Called when the wheel is rotated counterclockwise"""
        pass

    def on_press_clockwise(self):
        """Called when the wheel is rotated clockwise while pressed"""
        pass

    def on_press_counterclockwise(self):
        """Called when the wheel is rotated counterclockwise while pressed"""
        pass


class Powermate(object):
    class PerhipheralThread(threading.Thread):
        class EventDispatcher(btle.DefaultDelegate):
            def __init__(self, event_handler):
                btle.DefaultDelegate.__init__(self)
                self.e = event_handler
                self.long_press = 0

            def handleNotification(self, handle, data):
                val = struct.unpack('b', data)[0]
                if handle == KNOB_VAL_HND:
                    self.handle_knob(val)
                elif handle == BATTERY_VAL_HND:
                    self.handle_battery(val)

            def handle_knob(self, data):
                if data == 104:
                    self.e.on_clockwise()
                elif data == 103:
                    self.e.on_counterclockwise()
                elif data == 101:
                    self.e.on_press()
                elif data == 112:
                    self.e.on_press_clockwise()
                elif data == 105:
                    self.e.on_press_counterclockwise()
                elif data >= 114 and data <= 119:
                    self.long_press = data - 113
                elif data == 102:
                    if self.long_press > 0:
                        self.e.on_long_press(self.long_press)
                        self.long_press = 0

            def handle_battery(self, data):
                self.e.on_battery_report(data)

        def __init__(self, address, handler, iface=None):
            threading.Thread.__init__(self)
            self.address = address
            self.handler = handler
            self.iface = iface
            self.kill = False
            self.connected = False

        def _enable_notification(self, handle):
            val = (1).to_bytes(2, byteorder='little')
            self.p.writeCharacteristic(handle, val, False)

        def connect(self):
            try:
                self.p = btle.Peripheral(self.address, iface=self.iface)
                self.p.setDelegate(self.EventDispatcher(self.handler))
                self._enable_notification(BATTERY_CC_HND)
                self._enable_notification(KNOB_CC_HND)
                self.handler.on_connect()
                self.connected = True
                return True
            except btle.BTLEException as e:
                print(e)
                return False

        def run(self):
            while not self.kill:
                while not self.connect():
                    time.sleep(1)
                while not self.kill:
                    try:
                        if self.p.waitForNotifications(1.0):
                            continue
                    except btle.BTLEException as e:
                        print(e)
                        self.connected = False
                        self.handler.on_disconnect()
                        break

        def stop(self):
            self.kill = True

    def __init__(self, address, handler, iface=None):
        self.perhipheral = self.PerhipheralThread(address, handler, iface)
        self.perhipheral.start()

    def stop(self):
        self.perhipheral.stop()
        self.perhipheral.join()
