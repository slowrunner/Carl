ping -c4 10.0.0.1 > /dev/null

if [ $? != 0 ]
then
  echo "No network connection, restarting wlan0"
  /sbin/ifdown 'wlan0'
  sleep 6
  /sbin/ifup --force 'wlan0'
else
  echo "Network connection confirmed"
fi

