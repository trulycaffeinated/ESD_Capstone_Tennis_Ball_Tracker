% Hard coded parameters
b = 50; % baseline [mm]
f = 10; % focal length [mm]
ps = 0.006; % pixel size [mm]
xNumPix = 752; % number of pixels in the x direction of the sensor [px]
cxLeft = xNumPix/2; % left camera x center [px]
cxRight = xNumPix/2; % right camera x center [px]

% create two cameras
Cam_L = SE3(0, 0, 0);
Cam_R = SE3(b, 0, 0);

% Create the ball
Z_b = linspace(.5, 10, 100); %
BALL = repmat(SE3(), 1, numel(Z_b));   % preallocate exactly 100
for i = 1:numel(Z_b)
    BALL(i) = SE3(0, 0, Z_b(i));
end
    
% see the ball
BALL_L = inv(Cam_L) * BALL;
BALL_R = inv(Cam_R) * BALL;

% find the balls position from the cameras
pL = transl(BALL_L).';
pR = transl(BALL_R).';

XL = pL(1,:)
ZL = pL(3,:)

XR = pR(1,:)
ZR = pR(3,:)

xLeft = cxLeft + (f *(XL./ZL))
xRight = cxRight + (f *(XR./ZR))

%Equations to find depth
d = abs((xLeft - cxLeft)-(xRight-cxRight))*ps;
Z = (b * f)./d;
fprintf("d = %f , Z = %f", d, Z);

% Debug sizes (very helpful)
fprintf("size(Z_b) = %s\n", mat2str(size(Z_b)));
fprintf("size(d)   = %s\n", mat2str(size(d)));

figure;
plot(Z_b(:), d(:), 'LineWidth', 1.5);
xlabel('True depth Z (mm)');
ylabel('Disparity d (mm)');
title('Disparity vs Depth');
grid on;
