import dbus, avahi
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import time
import re
pattern = re.compile("\d+")

class Runner():
    def __init__(self, avahi_server):
        self.avahi_server = avahi_server

    def on_state_change(self, state, error):
        if state == avahi.SERVER_COLLISION:
            print(f"[state: collision] collided, waiting 5s...")
            time.sleep(5)

        elif state == avahi.SERVER_RUNNING:
            hostname = self.avahi_server.GetHostName()
            print(f"[state: running] hostname changed: {hostname}")
            if '-' in hostname and pattern.search(hostname.split('-')[-1]) is not None:
                hostname = str(hostname)
                suffix = hostname[-2:]
                hostname = hostname[0:-2]
                print(f"removing `{suffix}` suffix: {hostname}")
                self.avahi_server.SetHostName(hostname)

def main():
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    object  = bus.get_object("org.freedesktop.Avahi","/")
    avahi_server = dbus.Interface(object, 'org.freedesktop.Avahi.Server')
    runner = Runner(avahi_server)
    avahi_server.connect_to_signal('StateChanged', runner.on_state_change)
    print("Starting main loop")
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()
