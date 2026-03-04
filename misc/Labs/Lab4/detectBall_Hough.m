function [x,y,radius] = detectBall_Hough(img)
% This function detects a bright ball in an RGB image using
% MATLAB's imfindcircles function

% convert image to grayscale
gray = rgb2gray(img);
% enhance local contrast
eq = adapthisteq(gray);
% detect circles using circular hough transform
[centers, radii] = imfindcircles(eq, ...
    [5,25], ...                   % radius search range
    'ObjectPolarity','bright',...   % detect bright circles
    'Sensitivity',0.95);              % detection sensitivity

% error handling if nothing is found
if isempty(centers)
    error('No circles detected');
end

% search for dark circles if no bright ball is detected
if radii < 13
    [centers, radii] = imfindcircles(eq, ...
    [5,25], ...                   % radius search range
    'ObjectPolarity','dark',...   % detect dark circles
    'Sensitivity',0.97);          % detection sensitivity
end

% strongest detected circle
centroid = centers(1,:);
radius = radii(1);

% return centroid coordinates
x = centroid(1);
y = centroid(2);

end