# Lab 2
We'll be making a GUI (preferably in MatLab)
- X, Y, Z scatter plot
- Will be going over setting it up and creating it on Thursday

## Image Definitions
**Pixel** - Single sensor element which can translate light intensity into a digital value
**Image** - A collection of pixels which together comprise a viewable image
**Kernel** - A (small) number of pixels, typically 3x3, but can be larger, which are manipulated as a unit applied to an image

Image sensors (cameras) are designed to acquire images in a manner that is as close as possible to human perception

Sensors are composed of 2x2 arrays of individual pixel sensors and optical lenses which direct the light onto the sensor plane

A filter array is placed in between the lens and the sensor, the filter restricts the light that can pass through to the corresponding sensor pixel - a single cell allows a single color to pass through
- Bayer filter (Bruce Bayer, Eastman Kodak)
- Problem with this is that pixels are (to our eye) shifted, green will shifted from the blue which is shifted from the red - each cell needs to include ALL THREE color pixels rather than one

**Color Depth** - number of bits of resolution for each pixel
- 8-bit -> 256 resolved colors (light levels)
- 24-bit color depth is 8 bits each of R, G, B
### Distortion
What factors can cause an image to be distorted?
- Subject(s) can move
- High intensity light - blast the sensor - "blown out"
	- Most likely a reflection
- Lens condition/aberrations (damage, dirty, distorted)
	- Non-linearities (cannot be fixed)
- Color balancing
- Non-uniformity of the filter
	- Any overlap of the sensors (red filter overlapping blue sensor etc.)
	- Uniformity of the filter, lets more red light through than blue or green
- Defective Pixels
	- Sensors/capacitors that don't work properly

### Displays
Share many characteristics of image sensors

We will write a voltage into the capacitor, which then drives TFT devices (thin film transistors) which are directly on the glass display which selectively block light based on the value written in.
The more voltage we put on it, the LESS light is allowed through the glass

A backlight is illuminated behind the glass and the light that is not blocked comes through

All rows are written simultaneously

**Kernels** 
Convolution
```octave
v' = (i*r)+(h*s)+(g*t)+(f*u)+(e*v)+(d*w)+(c*x)+(b*y)+(a*z)
```
Kernels are almost always square

Need to do edge detection on grayscale
#### Project Q's
How fast is the ball moving?
How quickly do we need to be taking pictures? 
