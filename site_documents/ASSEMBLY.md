## Assembly instructions

### Step 1

Push 8 M2.5 screws through the mounting holes upwards from the bottom side.

<img src="assembly-1.jpg" width="400">

In this picture there is:  
* The base plate for the sensor board in the top left.
* The slot for the frame stand in the top right.
* The mounting holes for the daughter board of the display in the upper mid.
* The mounting holes for the Raspberry Pi in the lower half.
* Two strain reliefs in the upper right and bottom mid.

The outcome should look like this:

<img src="assembly-1-3.jpg" width="400">
<img src="assembly-1-2.jpg" width="400">

### Step 2

Screw 8 M2.5 standoffs onto the screws.

<img src="assembly-2.jpg" width="400">

The outcome should look like this:

<img src="assembly-2-2.jpg" width="400">

### Step 3

Solder 4x1 pin-headers to the back side of the sensor board.  
The sensor's antenna is facing away from you.

<img src="assembly-3.jpg" width="400">

### Step 4

Connect the boards (board pins, not BCM) using 6 DuPont cables.
* Pi to radar sensor board  
  2 - VIN  
  6 - GND  
  11 - OUT  
  13 - CDS  
* Pi to HDMI board  
  12 - PWM  
  14 - GND  

<img src="assembly-4.jpg" width="400">

Mount the Pi and sensor board onto the standoffs and secure them down with 8 M2.5 nuts.

<img src="assembly-4-2.jpg" width="400">

The outcome should look like this:

<img src="assembly-4-3.jpg" width="400">
