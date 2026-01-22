% ------- lab 1 ---------- %
% default values from LAB
b = 50; % baseline [mm]
f6 = 6; % focal length [mm]
f10 = 10; % secondary focal length
ps = .006; % pixel size [mm]
xNumPix = 752; % total number of pixels in x direction of the sensor [px]
cxLeft = xNumPix/2; % left camera x center [px]
cxRight = xNumPix/2; % right camera x center [px]

% The "Ball" or Point (P) which is now moving
% P = [1, 0, 10]; % Stationary ball
Z_P = linspace(.1, 10, 100);
N = numel(Z_P);
P = [   ones(1,N);
        zeros(1,N);
        Z_P];

% ============ f6 ================ %
% Create the left camera
camLeft_f6=CentralCamera( ...
    'focal',f6/1000, ...
    'pixel',ps/1000, ...
    'resolution',[xNumPix, 480], ...
    'centre',[cxLeft, 480/2], ...`
    'name','Camera Left');
% Position the left camera
Tcam_Left_f6=SE3(0, 0, 0);
camLeft_f6.T=Tcam_Left_f6;

% Create the right camera
camRight_f6=CentralCamera( ...
    'focal',f6/1000, ...
    'pixel',ps/1000, ...
    'resolution',[xNumPix, 480], ...
    'centre',[cxRight, 480/2], ...
    'name','Camera Right');
% Position the left camera
Tcam_Right_f6=SE3(+b/1000, 0, 0);
camRight_f6.T=Tcam_Right_f6;
% Left Camera project
uv_Left_f6 = camLeft_f6.project(P);
%%%camLeft_f6.plot(P);
xLeft_f6 = uv_Left_f6(1, :)

% Right Camera Project
uv_Right_f6 = camRight_f6.project(P);
%%%camRight_f6.plot(P);
xRight_f6 = uv_Right_f6(1, :)

% ============ f10 ================ %
% Create the left camera
camLeft_f10=CentralCamera( ...
    'focal',f10/1000, ...
    'pixel',ps/1000, ...
    'resolution',[xNumPix, 480], ...
    'centre',[cxLeft, 480/2], ...`
    'name','Camera Left');
% Position the left camera
Tcam_Left_f10=SE3(0, 0, 0);
camLeft_f10.T=Tcam_Left_f10;

% Create the right camera
camRight_f10=CentralCamera( ...
    'focal',f10/1000, ...
    'pixel',ps/1000, ...
    'resolution',[xNumPix, 480], ...
    'centre',[cxRight, 480/2], ...
    'name','Camera Right');
% Position the left camera
Tcam_Right_f10=SE3(+b/1000, 0, 0);
camRight_f10.T=Tcam_Right_f10;

% Left Camera project
uv_Left_f10 = camLeft_f10.project(P);
%%%camLeft_f10.plot(P);
xLeft_f10 = uv_Left_f10(1, :)

% Right Camera Project
uv_Right_f10 = camRight_f10.project(P);
%%%camRight_f10.plot(P);
xRight_f10 = uv_Right_f10(1, :)

% calculate disparity
d_f6 = (abs((xLeft_f6-cxLeft)-(xRight_f6-cxRight))*ps) % disparity [mm]
d_f10 = (abs((xLeft_f10-cxLeft)-(xRight_f10-cxRight))*ps) % disparity [mm] 

%calculate depth
Z_f6 = (b * f6)./d_f6 % depth [mm]
Z_m_f6 = Z_f6 ./ 1000 % depth [m]
Z_m_error_f6 = Z_P - Z_m_f6

Z_f10 = (b * f10)./d_f10 % depth [mm]
Z_m_f10 = Z_f10 ./ 1000 % depth [m]
Z_m_error_f10 = Z_P - Z_m_f10

% Plot disparity
figure
plot(Z_P, d_f6, 'LineWidth', 2)
hold on
plot(Z_P, d_f10, 'LineWidth', 2)
grid on
xlabel('Depth Z [m]')
ylabel('Disparity d [mm]');
title('Depth vs Disparity for varying focal lengths');
legend('f = 6 mm', 'f = 10 mm', 'Location', 'northeast')
hold off

% Plot depth error
figure
plot(Z_P, Z_m_error_f6, 'LineWidth', 2)
hold on
plot(Z_P, Z_m_error_f10, 'LineWidth', 2)
grid on
xlabel('Depth Z [m]')
ylabel('Depth Error [m]')
ylim([-10e-14, 10e-14])
title('Depth Error vs True Depth for varying focal lengths')
legend('f = 6 mm', 'f = 10 mm', 'Location', 'northeast')
hold off