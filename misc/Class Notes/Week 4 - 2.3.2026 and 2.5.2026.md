# Color Images and such

We need to combine the RRGB pixel values into a single value

We could scale the color pixel by their corresponding luminosity
- GrayScale = ($R \times 0.299 + G \times 0.587 + B \times 0.144$)
- We need to do the math in floating point format - floating point has about six operations per pixel - which will be painfully slow
	- floating point math can take up to 1/3 of the active silicon on the processor

- We can use an alternative GrayScale = $(R\times 0.25+G\times 0.5 + B\times 0.125$)
	- Is actually Gray = R/4 + G/2 + B/8 
		- This only captures 87% of the luminosity rather than 100%
		- Is that good enough?

50% Threshold will probably not work - will want to work with Grayscale if possible
Manual VHDL vs Auto Generated VHDL

1. Take the picture
2. Convert to Grayscale
3. Convolve it
4. Edge Detection
5. Find Ball

FrameRate = $\frac{1}{ProcessingTime}$

Maximum speed of the ball we can say is 150mph

We will probably not be able to use matlab for the image conversion, but it's still an important tool for processing

1. Convert the image into some form of usable grayscale
	1. Intermediate of grayscale - identify certain colors?
2. Determine centroid of ball (edge detection, convolution, etc.)

There are certain algorithms that can map to certain colors, but they will not always be accurate

We could use a yCrCb camera to skip a step

**Region of Interest** - where we  know the ball could be, don't process data that we know is worthless (where the ball isn't)

How many false +/-'s can you accept in the design? - Up to us?

```octave
clear;
% Import the image
image = imread('left5.jpg');
% Convert image to grayscale
image = rgb2gray(image);
% display the image
imshow(image);

% Find the circles in the image (as many as there are)
[centers, radii, metric] = imfindcircles(image, [15 100])
% Draw the edges of the circles on the image
viscircles(centers, radii, 'Edge Color', 'Red');
```
**THIS IS SLOW AS HELL ^^^**
Profile it to see how slow