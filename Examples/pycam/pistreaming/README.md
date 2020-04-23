# Pi Video Streaming Demo on my GoPiGo3 Robot "Carl"

Reference:  https://github.com/waveform80/pistreaming


This is a demo of low latency streaming of the Pi's camera module to
a web browser running on a Pi3B mounted in my GoPiGo3 robot "Carl"

It utilizes Dominic Szablewski's 
[JSMPEG project](https://github.com/phoboslab/jsmpeg). 

Other dependencies are the Python [ws4py library](http://ws4py.readthedocs.org/), 
[picamera library](http://picamera.readthedocs.org/) (specifically version 1.7 or above),
and [FFmpeg](http://ffmpeg.org).


## Installation  (modified for my particular folder structure)

Firstly make sure you've got a functioning Pi camera module (test it with
`raspistill` to be certain). Then make sure you've got the following packages
installed:

    $ sudo apt-get install ffmpeg git python3-picamera python3-ws4py

Make location and cd to it:  ~/Carl/Examples/pycam/pistreaming/

Next, clone the repository:

    $ git clone https://github.com/waveform80/pistreaming.git

Copy content up:  cp pistreaming/* .
Remove cloned dir: rm -rf pistreaming
(this removes .git pointing back to source)
then git add ../pistreaming, commit, push


## Usage

Run the Python server script which should print out a load of stuff
to the console as it starts up:

    $ cd ~/Carl/Examples/pycam/pistreaming
    $ ./server640x480x24.py  or ./server320x240x24.py
    Initializing pistreaming 640 x 480 at 24 fps
    Initializing websockets server on port 8084
    Initializing HTTP server on port 8082
    Initializing camera
    Initializing broadcast thread
    Spawning background conversion process
    Starting websockets thread
    Starting HTTP server thread
    Starting broadcast thread

Now fire up your favourite web-browser and visit the address
`http://pi-address:8082/` - it should fairly quickly start displaying the feed
from the camera. 

If you find the video stutters or the latency is particularly bad (more than a
second), check your network connection between the Pi and the clients.

To shut down the server press Ctrl+C - you may find it'll take a while
to shut down unless you close the client web browsers (Chrome in particular
tends to keep connections open which will prevent the server from shutting down
until the socket closes).

NOTE: When reconnecting after switching server resolution, may need to refresh browser 
window to get the correct resolution.


## PERFORMANCE

Pi3B (1cm heatsink) in GoPiGo3 Robot
Running Processes:
- RPI-Monitor (every 30 seconds runs data getters causing load spikes)
- Raspbian For Robots Web VNC Desktop
- ssh shell
- Juicer (Carl's power model - Docking management)
Base load is 1min: 0.18  5min: 0.2 and desktop gauge shows 0..2..25..7..0
Max Temp with Base Load: 52 degC (78 degree room temp)

Serving one web client at 640x480x24fps:
Base load is 1min: 1.4 5min: 1.4 and desktop gauge shows 25..17..26..41..23
Max Temp with 1 client: 65 degC

Serving one web client at 320x240x24fps:
Base load is 1min: 0.8 5min: 0.8 and desktop gauge shows 12..30..8..33..10
Max Temp with 1 client: 55 degC


