# Color Images and such

We need to combine the RRGB pixel values into a single value

We could scale the color pixel by their corresponding luminosity
- GrayScale = ($R \times 0.299 + G \times 0.587 + B \times 0.144$)
- We need to do the math in floating point format - floating point has about six operations per pixel - which will be painfully slow
	- floating point math can take up to 1/3 of the active silicon on the processor

