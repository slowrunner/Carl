Based on: https://raspihats.com/i2c-hat/2016/02/16/raspberry-pi-i2c-clock-stretch-timeout.html

Raspberry Pi I2C clock stretch timeout - for consistent BNO055 IMU operation

wget https://raw.githubusercontent.com/raspihats/raspihats/master/clk_stretch/i2c1_set_clkt_tout.c

wget https://raw.githubusercontent.com/raspihats/raspihats/master/clk_stretch/i2c1_get_clkt_tout.c


gcc -o i2c1_set_clkt_tout i2c1_set_clkt_tout.c
gcc -o i2c1_get_clkt_tout i2c1_get_clkt_tout.c

sudo ./i2c1_get_clkt_tout 
i2c1_get_clkt_tout: CLKT.TOUT = 64

sudo ./i2c1_set_clkt_tout 20000


sudo ./i2c1_get_clkt_tout 
i2c1_get_clkt_tout: CLKT.TOUT = 20000


This will be valid only until the next reboot!
 
