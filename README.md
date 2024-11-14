# plot_3_usec.py

With the wombatPi running coilscan.ino
This charts the raw analog scan, a difference scan, and the shape ('normalised' scan)

### Set the com port in read_wombat.py
### Set the pulse width in the arduino code to suit the coil (wombat_analog.h)


![screenshot](https://www.wombatpi.net/images/au_one_dollar_scan.PNG)


### Buttons:

Take Reference:   The latest Raw signal scan becomes the stored Reference signal

Grab Plot :       Capture the difference scan, Normalise (between 0 and 1) and add to the Lower Chart Window

Clear Plot:       Clear the Lower Chart Window

