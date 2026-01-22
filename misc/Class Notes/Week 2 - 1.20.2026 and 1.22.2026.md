# Matlab Intro, Image Generation, Plotting, and Stereo Imaging

Matlab environment is inherently interpretive
- Commands are entered, interpreted and operations are performed immediately

By default everything is a **double** (64 bits)

---
**Perfect Number Example**
```Vectorized_C
function [Result] = Perfect(candidate)
% Determine whether the number passed in is a perfect number or not

% Calculate the sum of the Candidates divisors
Sum = 0;
for Divisor = (Candidate-1):-1:1
	if(rem(Candidate, Divisor) == 0)
		Sum = Sum + Divisor;
	end
end

%
if (Sum == Divisor)
	Result = 1;
else
	Result = 0;
end
```
---

Images don't contain floating point numbers, they are 16 bit (or 8 bit) integers. 
Everything in Matlab is an array or matrixed stored as \[Row Col\]

Because everything is a matrix, multiplication is by default matrix multiplication
- Element by element multiplication is ".\*"
- Matrix multiplication is "\*"

# Peter Corke's Spatial Math Toolbox
Stereo imaging we focus on a point (P), with two cameras a left ($P_L$) and right ($P_R$)
From those cameras we an triangulate $Z_P$ using $X_L$ and $X_R$ 
What happens if $Y_L \neq Y_R$ ? Math gets a lot harder
- This may happen with cameras outside in the wind
- **Specifications should include how accurate our system is to *x* amount of wind 
  (Changes in $\Delta Y$)**

Need to install Peter Corke's...
- Robotics Toolbox
- Machine Vision Toolbox

### CameraCentral object
When a camera is instantiated the options must be specified
'focal' - focal length in meters
'pixel' - pixel size in meters
'resolution' - image plane resolution
'centre' - location of the principal points (array of two values for x,y)
'name' - text string name
'pose' - position of the camera is a homogenous transformation
```matlab
cam=CameraControl(...);
cam.T = ... %Homogenous transformation
```

The value to assign to the position is created with an SE3 object
The position is insantiated with an x,y,z, position translation from the origin (0,0,0)
```matlab
pos=SE3(...array of three values, x, y ,z);
cam.T=pos;
```

Cmera can now be used to get projections of world-view position

Given **p** is an 3xN array of x,y,z, real-world positions
- For the firstposition in the array, p(1,1) = $x_1$, p(2,1)=$y_1$,p(3,1)=$z_1$

uv=cam.project(p) produces the corresponding image plane coordinates (2xN) of the projected image
uv being the x,y coordinates in the image space. U and V are cords within the image

Example camera setup in matlab
```matlab
cam=CentralCamera( ...
'focal',10/1000, ...
'pixel',6e-6, ...
'resolution',[752, 480], ...
'centre',[752/2, 480/2], ...
'name','MyCamera');
Tcam=SE3(0, 1, 1);
cam.T=Tcam;
P=[1,0,10]';
cam.project(P)
cam.plot(P)
```

