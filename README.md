# monisrahmen

A smart frame you can send emails to.

## Description

Send pictures as email attachments.
They will be downloaded, adjusted and displayed in a loop.  
A motion sensor will blank the screen after some time of inactivity.  
Optionally, a network share for the pictures can be created.

The mounting frame is 3D printed.  
Some light soldering is required.

### Bill of materials

* 1 Raspberry Pi 2  
  The old model 2 is sufficient for this project and can be found for relatively cheap in late 2022.
* 1 WaveShare model 7" IPS/QLED Integrated Display, 1024x600, 70H-1024600
* 1 RCWL-0516 doppler radar microwave motion sensor module
* 1 HDMI cable, short and flexible
* 8 M2.5 screws, nuts and standoffs  
  Plastic is fine.
* 1 USB-A to Micro USB-B cable
* 1 USB-A to USB-C cable
* 1 Dual USB wall charger  
  The power draw of the display is about 350 mA.
* 4 square head male-to-female jumper wires
* 1 Small cable tie

### Tools

* Soldering equipment
* Hot glue gun

### Installing

* Install Pi OS Lite 32-bit using the Raspberry Pi Imager.  
  You can set up the hostname, user account, SSH and Wifi in the option section of the Imager.
  You should now be able to ssh into your Raspberry.

* Install dependencies:
    ```
    sudo apt-get install fonts-dejavu-core git python3 python3-pip python3-venv samba tmux
    ```

* Download the software:
    ```
    git clone https://github.com/sabotrax/monisrahmen.git
    ```

* Create the virtual environment for Python and install the modules:
    ```
    cd monisrahmen
    python3 -m venv .
    source bin/activate
    pip3 install -r requirements.txt
    echo "source ~/monisrahmen/bin/activate" >> ~/.bashrc
    ```

* Create the configuration file ``config.py``:
    ```
    # email settings
    email_user = "IMAP_USER"
    email_pass = "IMAP_PASSWORD"
    email_host = "IMAP_HOST"
    email_port = 993
    email_inbox = 'Inbox'

    # email subject for image processing
    email_keyword = 'bild'

    # installation directory
    project_path = "/home/schommer/monisrahmen"

    # image directory
    picture_path = project_path + "/pictures"

    # blank screen after
    display_timeout = 120

    # network error message
    network_error = "Kein Netzwerk!"

    screen_width = 1024
    screen_height = 600

    # splash image text
    font_size = 40
    ```

* Configure the display in ``/boot/config.txt``.  
    For the WaveShare model 7" IPS/QLED 1024x600 70H-1024600:
    ```
    hdmi_group=2
    hdmi_mode=87
    hdmi_cvt=1024 600 60 6 0 0 0
    hdmi_drive=1
    ```

* Also in ``/boot/config.txt`` for the display blanking:
    ```
    #dtoverlay=vc4-kms-v3d
    hdmi_blanking=1
    ```
    Blanking a HDMI display only worked on the Pi 2 if we used the legacy graphics driver.

* Rotate the display (optional):  
    Tate Mode for the virtual console.
    ```
    display_hdmi_rotate=3
    ```

* Suppress boot messages.  
    Append to the end of the line of ``/boot/cmdline.txt``:
    ```
    consoleblank=1 logo.nologo vt.global_cursor_default=0
    ```

    Add to ``/boot/config.txt``:
    ```
    avoid_warnings=1
    disable_splash=1
    ```

* Configure the Samba share.  
    Add to the end of ``/etc/samba/smb.conf``:
    ```
    [bilder]
    path = /home/schommer/monisrahmen/pictures/
    public = yes
    writable = yes
    comment = Bilder
    printable = no
    guest ok = yes
    ```

## Acknowledgments

Inspiration, documentation, code snippets, etc.
* [Building a living photo frame](https://www.ofbrooklyn.com/2014/01/2/building-photo-frame-raspberry-pi-motion-detector/)
* Waveshare display [Wiki](https://www.waveshare.com/wiki/70H-1024600) 
* Raspberry Pi [config.txt](https://www.raspberrypi.com/documentation/computers/config_txt.html) documentation
