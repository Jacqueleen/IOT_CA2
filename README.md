# How to make a Smart Clinic using IoT devices

## 1. Overview
Clinics are usually crowded and can have long waiting times. Sometimes, it would be helpful if the clinic could display the number of people in the queue so we can estimate our waiting time. This tutorial will show you how to read the RFID cards of patients going into a clinic and display the number of people who have already entered the clinic on an LCD display. This tutorial will also teach you how to remotely control the light source inside the clinic waiting room and get readings of light intensity, temperature and humidity of the waiting room.

## 2. Setting up your RFID card reader & LCD display

### Hardware needed:
* MFRC522 card reader module x1
* 16x2 LCD display x1

### Completed Fritzing Diagram
![RFID/LCD Fritzing Diagram](fritz2.png)

### Install the necessary libraries
In your raspberry pi, install the rpi-lcd library to manipulate LCD display
`sudo pip install rpi-lcd`

Follow the following steps to prepare the libraries for the MFRC522 card reader
1. Go to your raspberrypi and run raspi-config
`sudo rasp-config`
2. Select "Interfacing Options" and enable SPI
3. Modify the /boot/config.txt to enable SPI
`sudo nano /boot/config.txt`
4. Ensure these lines are included in config.txt
```
device_tree_param=spi=on
dtoverlay=spi-bcm2835
```
5. Install the Python development libraries
`sudo apt-get install python-dev`
6. Set up the SPI Python libraries since the card reader uses the SPI interface
```
cd ~
git clone https://github.com/lthiery/SPI-Py.git
cd ~/SPI-Py
sudo python setup.py install
```
7. Clone the MFRC522-python library to your home folder as follows:
```
cd ~
git clone https://github.com/pimylifeup/MFRC522-python.git
cd ~/MFRC522-python
sudo python setup.py install
```


