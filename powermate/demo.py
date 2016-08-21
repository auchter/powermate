#!/usr/bin/env python3.4

from powermate import Powermate, PowermateDelegate
import argparse
import time


class PrintEvents(PowermateDelegate):
    def __init__(self, addr):
        self.addr = addr

    def on_connect(self):
        print('Connected to %s' % self.addr)

    def on_disconnect(self):
        print('Disconnected from %s' % self.addr)

    def on_battery_report(self, val):
        print('Battery: %d%%' % val)

    def on_press(self):
        print('Press')

    def on_long_press(self, t):
        print('Long press: %d seconds' % t)

    def on_clockwise(self):
        print('Clockwise')

    def on_counterclockwise(self):
        print('Counterclockwise')

    def on_press_clockwise(self):
        print('Press clockwise')

    def on_press_counterclockwise(self):
        print('Press counterclockwise')


def main():
    parser = argparse.ArgumentParser(description='Print Powermate events')
    parser.add_argument('address', metavar='addr', type=str,
                        help='Bluetooth address of Powermate')
    args = parser.parse_args()

    p = Powermate(args.address, PrintEvents(args.address))
    while True:
        time.sleep(5)
    p.stop()
