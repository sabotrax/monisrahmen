# monisrahmen

A smart frame you can send emails to.

## Description

Send pictures as email attachments.
They will be downloaded, adjusted and displayed in a loop.

### Installing

* Configure the display in /boot/config.txt.
    Depending on the model.
    For the WaveShare model 7" IPS/QLED 1024x600 70H-1024600:
    ```
    hdmi_group=2
    hdmi_mode=87
    hdmi_cvt=1024 600 60 6 0 0 0
    hdmi_drive=1
    ```

* Suppress boot messages by appending to the end of the line of /boot/cmdline.txt:
    ```
    consoleblank=1 logo.nologo vt.global_cursor_default=0
    ```
* For the same reason add to /boot/config.txt:
    ```
    avoid_warnings=1
    disable_splash=1
    ```

## Acknowledgments

Inspiration, code snippets, etc.
* [Building a living photo frame](https://www.ofbrooklyn.com/2014/01/2/building-photo-frame-raspberry-pi-motion-detector/)
