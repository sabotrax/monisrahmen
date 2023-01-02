## Assembly instructions

### Overview

Parts of the mounting frame:
* The base plate for the sensor board in the top left.
* The slot for the frame stand in the top right.
* The mounting holes for the daughter board of the display in the upper mid.
* The mounting holes for the Raspberry Pi in the lower half.
* Two strain reliefs in the upper right and bottom mid.

<img src="assembly-1.jpg" width="400">

### Step 1

Push 8 M2.5 screws through the mounting holes from the bottom side up.

<img src="assembly-1-3.jpg" width="400">

The outcome should look like this:

<img src="assembly-1-2.jpg" width="400">

### Step 2

Screw 8 M2.5 standoffs onto the screws.

<img src="assembly-2.jpg" width="400">

The outcome should look like this:

<img src="assembly-2-2.jpg" width="400">

### Step 3

Solder the 4x1 pin-header to the back side of the sensor board.  
The sensor's actual antenna is facing down.

<img src="assembly-3.jpg" width="400">

### Step 4

Connect the boards (board pin numbering, not BCM) using 6 DuPont cables.
* Raspberry Pi to radar sensor board:  
  2 - VIN  
  6 - GND  
  11 - OUT  
  13 - CDS  
* Raspberry Pi to HDMI board:   
  12 - PWM  
  14 - GND  

<img src="assembly-4.jpg" width="400">

Mount the Raspberry Pi and sensor board onto the standoffs and tighten them down with 8 M2.5 nuts.

<img src="assembly-4-2.jpg" width="400">

The outcome should look like this:

<img src="assembly-4-3.jpg" width="400">

### Step 5

Place the sensor board onto the two tiny standoffs of the frame using the central mounting holes.  
Tie the board to the base plate using a cable tie. There's a gap for the tie on the underside of the frame.

<img src="assembly-5.jpg" width="400">

The outcome should look like this:

<img src="assembly-5-2.jpg" width="400">

### Step 6

Connect the HDMI ports of the Raspberry Pi and the daughter board of the display with the HDMI cable.

<img src="assembly-6.jpg" width="400">

The outcome should look like this:

<img src="assembly-6-2.jpg" width="400">

### Step 7

Using the USB cable, connect the USB-C port of the HDMI board to a USB-A port of the Raspberry Pi.
Secure it to the frame using the strain relief. You might want to use a shorter cable than I did.

<img src="assembly-7.jpg" width="400">

The outcome should look like this:

<img src="assembly-7-2.jpg" width="400">

### Step 8

Connect the HDMI-FPC cable to the display with the lettering on the cable facing towards you.  
These cables are susceptible to breaking, so you might want to consider a tutorial on Youtube.

<img src="assembly-8.jpg" width="400">

Put the frame over the display passing the FPC table up through the frame.

<img src="assembly-8-2.jpg" width="400">

Connect the FPC cable to the HDMI board.

<img src="assembly-8-3.jpg" width="400">

### Step 9

Connect the Micro-USB power cord to the Raspberry Pi and secure it to the frame using a cable tie and the strain relief.

<img src="assembly-9.jpg" width="400">

The outcome should look like this:

<img src="assembly-9-2.jpg" width="400">

### Step 10

Sand down the skewed part of the frame stand so it can fit in the mounting slot.

<img src="assembly-10.jpg" width="400">

The outcome should look like this:

<img src="assembly-10-2.jpg" width="400">

You can now go on with the software installation.
