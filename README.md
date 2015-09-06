DashScanner
============

The DashScanner service monitors the network for ARP discovery packets from the Amazon Dash and passes the source MAC on to a webservice. In conjunction with Node-Red, it makes it easy to trigger complex actions.

To set up the service:

1. Edit DashScanner
  * Set DIR to the checkout directory.
2. Edit dash_scanner.py
  * Set DASH_URL to the webservice waiting for MAC posts.
3. Set DashScanner and dash_scanner.py to executable.
4. Copy the DashScanner file to /etc/init.d/DashScanner

Now, start the process with:

```bash
sudo service DashScanner start
```

For the webservice side, set up [Node-Red](http://nodered.org) with an "HTTP In" node with Method:POST and URL:/dash. You can then use this node to trigger a wide variety of different functionality and services.

Originally, I wrote a Node-Red node to handle the ARP capture directly. I didn't like runnin my entire Node-Red service as root, though, so I moved the functionality to it's own service.

This project is inspired heavily by [Ted Benson's](https://twitter.com/edwardbenson) [excellent post on triggering on Dash ARP packets](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8).
