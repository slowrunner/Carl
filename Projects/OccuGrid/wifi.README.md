WiFi Monitoring README


== list devices ==
iw dev
- returns phy#0 for built-in WiFi
- returns phy#1 for USB WiFi Adapter

== list all the capabilities of an device ==
iw phy phy1 info
- note drop the '#' from device name



== Python WiFi package ==
sudo pip3 install wifi

- allows accessing device info
- allows configuring devices if running as root/sudo user

- class wifi.Cell is python interface to output of iwlist
  - classmethod all(interface) returns list of all cells returned from iwlist
  - classmethod from_string

== To get signal strength for an interface ==
- print("wlan0:",list(wifi.Cell.all('wlan0'))[0].signal)
- if not root/sudo user returns cached value of once per minute scans by OS
- if root/sudo user: performs scan and returns result


