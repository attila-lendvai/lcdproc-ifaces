#!/usr/bin/env python

# RedHat:
# yum install python-dev
# yum install python-setuptools

# Debian, and the likes:
# sudo apt-get install python-setuptools python-netifaces python-daemon
# sudo easy_install lcdproc

import time
import string
import datetime
import netifaces

# deamon example: http://www.python.org/dev/peps/pep-3143/

import grp
import pwd
import daemon
import lockfile
import syslog
import time
import socket
import sys
import traceback

from lcdproc.server import Server

def _syslog(level, message, *args):
    formattedMessage = message % args
    syslog.syslog(level, "lcdproc: " + formattedMessage)
    print(formattedMessage)

def logInfo(message, *args):
    _syslog(syslog.LOG_INFO,  message % args)

def logDebug(message, *args):
    _syslog(syslog.LOG_DEBUG, message % args)

def logWarn(message, *args):
    _syslog(syslog.LOG_WARNING, message % args)

def logError(exception, message, *args):
    _syslog(syslog.LOG_ERR, message % args)
    etype, evalue, etraceback = sys.exc_info()
    if exception:
        logException(syslog.LOG_ERR, etype, evalue, etraceback)

def logException(level, etype, evalue, etb):
    for line in traceback.format_exception(etype, evalue, etb):
        for line in line.rstrip().split('\n'):
            syslog.syslog(level, line)

def main():
    logInfo("Starting up...")
    while True:
        try:
            lcd = Server("localhost", debug=False)
            lcd.start_session()
            logInfo("Connected to LCDd")

            lcd.add_key("Up")
            lcd.add_key("Down")

            screen1 = lcd.add_screen("Screen1")
            screen1.set_heartbeat("off")

            line1_widget = screen1.add_scroller_widget("line1", left=1, top=1, right=20, bottom=1, speed=10, text="")
            line2_widget = screen1.add_scroller_widget("line2", left=1, top=2, right=20, bottom=2, speed=10, text="")

            currentIndex = 0

            logInfo("Entering endless loop...")
            while True:

                interfaceNames = sorted(netifaces.interfaces())

                interfaceNames = filter (lambda name:
                                             not name in ["lo"],
                                         interfaceNames)

                currentIndex = max(0, min(currentIndex, len(interfaceNames) - 1))
                currentInterfaceName = interfaceNames[currentIndex]

                line1 = currentInterfaceName + ": "
                line2 = ""
                addresses = netifaces.ifaddresses(currentInterfaceName)

                if netifaces.AF_INET in addresses:
                    line1 += addresses[netifaces.AF_INET][0]['addr']

                if netifaces.AF_INET6 in addresses:
                    line2 += addresses[netifaces.AF_INET6][0]['addr']

                line1_widget.set_text(line1)
                line2_widget.set_text(line2)

                time.sleep(0.1)

                while True:
                    event = lcd.poll()
                    if not event:
                        break
                    event = string.strip(event)
                    if event == "key Up":
                        currentIndex = currentIndex + 1
                    elif event == "key Down":
                        currentIndex = currentIndex - 1
        # probably it's better to just quit together with LCDd, therefore it's commented out...
        #except socket.error, EOFError:
        #    logWarn("Error connecting to LCDd, retrying in 30 seconds...")
        #    time.sleep(30)
        except Exception as e:
            logError(e, "Error reached toplevel, exiting with exit code 42")
            sys.exit(42)

# Run

if __name__ == "__main__":
    context = daemon.DaemonContext(
        working_directory = '/opt',
        umask = 0o002,
        gid = grp.getgrnam('nogroup').gr_gid,
        uid = pwd.getpwnam('nobody').pw_uid,
        )

    with context:
        main()
