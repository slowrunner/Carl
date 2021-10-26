# RPI-BENCHMARK

* From: https://github.com/aikoncwd/rpi-benchmark/

* Installation (Not required)

```
mkdir benchmark
cd benchmark
wget https://raw.githubusercontent.com/aikoncwd/rpi-benchmark/master/rpi-benchmark.sh
chmod +x rpi-benchmark.sh
```

## Usage

* copy and paste the following command in your Raspberry Pi console:

     curl -L https://raw.githubusercontent.com/aikoncwd/rpi-benchmark/master/rpi-benchmark.sh | sudo bash

The rpi-benchmark script will start in 2 seconds :relaxed:
<br>

* Execution if installed

```
sudo ./rpi-benchmark.sh
```

## Information

The script runs 7 benchmark tests to stress the Raspberry Pi hardware:

1. **Speedtest-cli test:** Calculate ping, upload and download internet speed
2. **CPU sysbench test:** Calculate 5000 prime numbers
3. **CPU sysbench test:** Multithread with 4000 yields and 5 locks
4. **MEMORY RAM test:** Sequencial access to 3Gb of memory
5. **microSD HDParm test:** Calculate maximun read speed for SD
6. **microSD DD write test:** Calculate maximun write speed with 512Mb file
7. **microSD DD read test:** Calculate maximun read speed with 512Mb file

After every test, it will report the current CPU temperature  

Rpi-benchmark script will show the current hardware (w/any overclock) settings. 
<br>
<br>
