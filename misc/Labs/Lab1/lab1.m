% Hard coded parameters
b = 50; % baseline [mm]
f = 6; % focal length [mm]
ps = 0.006; % pixel size [mm]
xNumPix = 752; % number of pixels in the x direction of the sensor [px]
cxLeft = xNumPix/2; % left camera x center [px]
cxRight = xNumPix/2; % right camera x center [px]

% Create the ball
BALL = SE3(50, 0, 100);

% create two cameras
Cam_L = SE3(0, 0, 0);
Cam_R = SE3(b, 0, 0);

% see the ball
BALL_L = inv(Cam_L) * BALL;
BALL_R = inv(Cam_R) * BALL;

% find the balls position from the cameras
XL = BALL_L.t(1);
ZL = BALL_L.t(3);

XR = BALL_R.t(1);
ZR = BALL_R.t(3);

xLeft = cxLeft + (f *(XL/ZL)) / ps;
xRight = cxRight + (f *(XR/ZR)) / ps;

%Equations to find depth
d = (abs((xLeft - cxLeft)-abs(xRight-cxRight))*ps);
Z = (b * f)/d;