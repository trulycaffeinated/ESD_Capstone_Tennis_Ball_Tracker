clear
% Read image from file
image=imread("Pattern.jpg");

% There are differnt edge detection kernels
%   "Sobel" (default)
%   "Prewitt"
%   "Roberts"
%   "log"
%   "zerocross"
%   "Canny"
%   "approxcanny"
SobelEdges=edge(image, 'Sobel');
figure; imshow(SobelEdges); title('Sobel');
SobelEdges=edge(image, 'Prewitt');
figure; imshow(SobelEdges); title('Prewitt');
SobelEdges=edge(image, 'Roberts');
figure; imshow(SobelEdges); title('Roberts');
SobelEdges=edge(image, 'log');
figure; imshow(SobelEdges); title('log');
SobelEdges=edge(image, 'zerocross');
figure; imshow(SobelEdges); title('zerocross');
SobelEdges=edge(image, 'Canny');
figure; imshow(SobelEdges); title('Canny');
SobelEdges=edge(image, 'approxcanny');
figure; imshow(SobelEdges); title('approxcanny');

% Display original image
figure; imshow(image); title('Original');
