%% ------- lab 1 ---------- %
%
%   Jeffrey Taylor
%   CPET 563 - ESD : Capstone
%   Lab 1 - Stereo Imaging
%
% ------- lab 1 ---------- %

% Clears all variables from the script otherwise bad things happen
clearvars; clc;

%% Camera Spec values - Currently Lab Default
% IFWATER USB Camera 1080P High Speed 5-50mm focal lens (amazon.com)
% Using this camera to test the variability of the model -- some key values
%   1920x1080p : 60fps -- pixel size 0.0346mm
%   1280x720p  : 120fps -- pixel size 0.0518mm
%   640x360p   : 240fps -- pixel size 0.1037mm
% higher resolution, less error but less data
b = 50; % baseline [mm]
f = [6, 10];
ps = .06; % pixel size [mm]
xNumPix = 1920; % total number of pixels in x direction of the sensor [px]
FPS = 120; % pictures taken / second
cxLeft = xNumPix/2; % left camera x center [px]
cxRight = xNumPix/2; % right camera x center [px]

%% The "Ball" or Point (P) which is now moving
%   The code is formatted here as such so that any change to Z_P (point
%   depth) will "just work", and no other code will need to be changed to
%   adjust for either the increased size, or increased number of points.
% I'm going to use different Frames/Second values for the depth increments
% Z_Random = randi([1, 100]); % This was used in testing to test varying
%                               depths of the point
Z_P = linspace(.1, 10, FPS); % Depth values (.1 -> 10 in FPS increments)
N = numel(Z_P);
P = [   ones(1,N);
        zeros(1,N);
        Z_P]; % Moving Point

%% Create the cameras, and gather data from focal points
for i = 1:numel(f)
    fi = f(i);

    % Create Left Camera
    camLeft=CentralCamera( ...
        'focal',fi/1000, ...
        'pixel',ps/1000, ...
        'resolution',[xNumPix, 480], ...
        'centre',[cxLeft, 480/2], ...`
        'name','Camera Left');
    % Position the left camera
    left_Tcam=SE3(0, 0, 0);
    camLeft.T=left_Tcam;
    % Project the left camera
    uv = camLeft.project(P);
    xLeft(i, :) = uv(1, :);

    % Create Right Camera
    camRight=CentralCamera(...
        'focal',fi/1000, ...
        'pixel',ps/1000, ...
        'resolution',[xNumPix, 480], ...
        'centre',[cxRight, 480/2], ...`
        'name','Camera Left');
    % Position the right camera
    right_Tcam=SE3(+b/1000, 0, 0);
    camRight.T=right_Tcam;
    % Project the right camera
    uv = camRight.project(P);
    xRight(i, :) = uv(1, :);
end

%% Post data gathering calculations
% calculate disparity
d = (abs((xLeft-cxLeft)-(xRight-cxRight))*ps) % disparity [mm]

%calculate depth
Z = (b .* f(:))./d % depth [mm]
Z_m = Z ./ 1000 % depth [m]
Z_m_error_ = Z_P - Z_m % depth error [m]

%% Plots

% Make the strings for the legend? (Pulled this line from chatGPT)
% I'll admit, no idea what this does or how it works, like what is
% arrayfun ???
legendStrings = arrayfun(@(fk) sprintf('f = %g mm', fk), f, ...
                         'UniformOutput', false);

% Plot disparity
figure
hold on
for i = 1:numel(f)
    plot(Z_P, d(i, :), 'LineWidth', 2)
end
hold off
grid on
xlabel('Depth Z [m]')
ylabel('Disparity d [mm]');
title('Depth vs Disparity for varying focal lengths');
%legend('f = 6 mm', 'f = 10 mm', 'Location', 'northeast')
legend(legendStrings, 'Location', 'northeast')

% Plot depth error
figure
hold on
for i = 1:numel(f)
    plot(Z_P, Z_m_error_(i, :), 'LineWidth', 2)
end
hold off
grid on
xlabel('Depth Z [m]')
ylabel('Depth Error [m]')
title('Depth Error vs True Depth for varying focal lengths')
%legend('f = 6 mm', 'f = 10 mm', 'Location', 'northeast')
legend(legendStrings, 'Location', 'northwest')