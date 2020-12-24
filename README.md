# What

Display the network interfaces on an LCD display using
[lcdproc](http://lcdproc.omnipotent.net/).

Some servers have small LCD displays. This project is a quick and dirty
Python script that can daemonize itself to display the network interfaces
on the LCD (e.g. their IP addresses).

# Who, Where

You can reach me at [attila@lendvai.name](mailto:attila@lendvai.name).

The project's home is on [Github](https://github.com/attila-lendvai/lcdproc-ifaces/).

# Install

Start it up as root, e.g. from `/etc/rc.local`. It will daemonize itself and log to `syslog`.

# Status

I'm no longer using it, and I don't even have the means for testing it.

If you're interested in maintaining this project then you're welcome to
take it over.
