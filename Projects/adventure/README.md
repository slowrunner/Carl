# Colossal Cave Adventure for Raspberry Pi OS


git clone https://github.com/troglobit/advent4.git
sudo apt-get install autoconf
cd advent4
./autogen.sh
./configure --prefix=/usr --localstatedir=/var
make -j3
sudo make install-strip

* to run it
advent

https://en.wikipedia.org/wiki/Colossal_Cave_Adventure
