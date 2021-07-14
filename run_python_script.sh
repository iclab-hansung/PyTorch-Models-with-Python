#!/bin/bash



sudo python3 solo_run_python.py ${1} 19 &
sleep .5
sudo python3 solo_run_python.py ${1} 19 &
sleep .5

sudo python3 solo_run_python.py ${1} 19 &
sleep .5
sudo python3 solo_run_python.py ${1} 18 &
sleep .5

sudo python3 solo_run_python.py ${1} 18 &
sleep .5
sudo python3 solo_run_python.py ${1} 18 &
sleep .5

# sudo python3 solo_run_python.py ${1} 5 &
# sleep .5
# sudo python3 solo_run_python.py ${1} 5 &
# sleep .5
