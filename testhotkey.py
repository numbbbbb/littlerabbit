from Cocoa import *
import time
from Foundation import *
from PyObjCTools import AppHelper
import time
import struct
import subprocess
import os


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, handler)


def handler(event):
    global ifopen
    if "flags=0x140109" in str(event) and "unmodchars=\"k\"" in str(event):
        os.system("killall Python")
    elif ("flags=0x40101" in str(event) and "unmodchars=\"1\"" in str(event)):
        pid = os.fork()
        if pid == 0:
            subprocess.call(["/opt/local/bin/python2.7 /Users/selfdir/Documents/littlerabbit/opencv-version.py left"], shell=True)
        pid = os.fork()
        if pid == 0:
            subprocess.call(["/opt/local/bin/python2.7 /Users/selfdir/Documents/littlerabbit/opencv-version.py right"], shell=True)
        #os.system("python /Users/selfdir/Documents/littlerabbit/main.py")


def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    print "Let's go!"
    AppHelper.runEventLoop()


if __name__ == '__main__':
    main()
