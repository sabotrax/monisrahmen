# monisrahmen

A digital picture frame you can send emails to.

![Assembled frame](site_documents/assembled.jpg | width=200)

## Description

Send pictures as email attachments.
They will be downloaded and displayed in a loop.  
A motion sensor will blank the screen after some inactivity.  
The image files can be remotely accessed via network share.

The mounting frame is 3D printed.  
Some light soldering is required.

### Bill of materials

* 1 Raspberry Pi 2  
  The old model 2 is sufficient for this project and can be found for relatively cheap in late 2022.
* 1 USB WLAN adapter like Edimax or TP-Link brand
* 1 WaveShare model 7" IPS/QLED Integrated Display, 1024x600, 70H-1024600
* 1 RCWL-0516 doppler radar microwave motion sensor module
* 1 HDMI cable, short and flexible
* 8 M2.5 screws, nuts and standoffs  
  Plastic is fine.
* 1 USB-A to Micro USB-B cable
* 1 USB-A to USB-C cable
* 1 Dual USB wall charger  
  The power draw of the display is about 350 mA.
* 4 square head female-to-female dupont cables
* 1 4x1 male pin-headers
* Small cable ties

### Tools

* Soldering equipment
* Hot glue gun

### Hardware setup

* TBD

### Installing

* Install Pi OS Lite 32-bit using the Raspberry Pi Imager.  
  You can set up the host name, user account, SSH and Wifi in the options of the Imager.
  You should then be able to ssh into your Raspberry.

* Install dependencies:
    ```
    sudo apt-get install fonts-dejavu-core git python3 python3-pip python3-venv samba
    ```

* Download the software:
    ```
    git clone https://github.com/sabotrax/monisrahmen.git
    ```

* Create the virtual environment for Python and install the required modules:
    ```
    cd monisrahmen
    python3 -m venv .
    source bin/activate
    pip3 install -r requirements.txt
    echo "source ~/monisrahmen/bin/activate" >> ~/.bashrc
    ```

* Create ``config.py``:
    ```
    # email settings
    email_user = "IMAP_USER"
    email_pass = "IMAP_PASSWORD"
    email_host = "IMAP_HOST"
    email_port = 993
    email_inbox = 'Inbox'

    # email subject for image processing
    email_keyword = 'foto'

    # delete emails after retrieval
    delete_email = False

    # installation directory
    project_path = "/home/schommer/monisrahmen"

    # image directory
    picture_path = project_path + "/pictures"

    # blank screen after
    display_timeout = 120  # seconds

    # network error message
    network_error = "Kein Netzwerk!"

    screen_width = 1024
    screen_height = 600

    # splash image text
    font_size = 30
    ```

* Configure the display in ``/boot/config.txt``.  
    For the WaveShare model 7" IPS/QLED 1024x600 70H-1024600:
    ```
    hdmi_group=2
    hdmi_mode=87
    hdmi_cvt=1024 600 60 6 0 0 0
    hdmi_drive=1
    ```

    Display blanking:
    ```
    #dtoverlay=vc4-kms-v3d
    hdmi_blanking=1
    ```
    Blanking an HDMI display would work only on the Pi 2 if we used the legacy graphics driver.

    Rotate the virtual console:
    ```
    display_hdmi_rotate=3
    ```
    This would also only work with the legacy driver.

* Suppress the boot messages.  
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
    # change accordingly to your installation directory
    path = /home/schommer/monisrahmen/pictures/
    public = yes
    writable = yes
    comment = Bilder
    printable = no
    guest ok = yes
    ```

    Change directory rights so image files can be deleted from your file manager:
    ```
    chmod 777 pictures
    ```

* Edit the shell scripts.  
    Change the installation directories in ``sitebin/restart_fbi.sh`` and ``sitebin/startup.sh``.  
    The image reload interval can also be configured in ``sitebin/restart_fbi.sh``.

* Set up Cron.  
    For your user ``crontab -e``
    ```
    @reboot                /home/schommer/monisrahmen/bin/python3 /home/schommer/monisrahmen/blank_screen.py
    0,15,30,45 * * * *     /home/schommer/monisrahmen/bin/python3 /home/schommer/monisrahmen/get_pics_by_mail.py
    ```

    For root ``sudo crontab -e``
    ```
    @reboot                /home/schommer/monisrahmen/sitebin/startup.sh
    2,17,32,47 * * * *     /home/schommer/monisrahmen/sitebin/restart_fbi.sh
    ```

    Adjust paths according to your installation directory.  
    Notice that fbi is being restarted shortly after emails have been checked.

## Acknowledgments

Inspiration, documentation, code snippets, etc.
* [Building a living photo frame](https://www.ofbrooklyn.com/2014/01/2/building-photo-frame-raspberry-pi-motion-detector/)
* Waveshare display [Wiki](https://www.waveshare.com/wiki/70H-1024600) 
* Raspberry Pi [config.txt](https://www.raspberrypi.com/documentation/computers/config_txt.html) documentation
* Crontab configuration ``man 5 crontab``
* Samba configuration ``man 5 smb.conf``
* fbi - Linux framebuffer image viewer ``man fbi``
