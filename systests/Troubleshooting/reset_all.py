#!/usr/bin/env python3

# Reset I2C bus?

from gopigo3 import GoPiGo3

gpg = GoPiGo3()

gpg.reset_all()

print("reset_all() executed")

