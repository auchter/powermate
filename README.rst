powermate: python library for Griffin Powermate Bluetooth
=========================================================

This provides a basic library for using a Griffin Powermate Bluetooth controller with Python.

Getting Started
---------------

Bring up your Bluetooth interface::

        $ sudo hciconfig hci0 up

Discover your Griffin Powermate's address::

        $ sudo hcitool lescan 
        00:12:92:08:07:B9 PowerMate Bluetooth

Run the demo to try to connect and display events from your Powermate::

        $ powermate-demo 00:12:92:08:07:B9
        Connected to 00:12:92:08:07:B9
        Clockwise
        ^C


