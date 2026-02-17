clear all
% Read the image from the file
image = imread('Pattern.jpg');
% Define the kernel - Edge Detection
kernel = [-1 -1 -1;
          -1  8 -1;
          -1 -1 -1];
% Perform convolution
convolvedImage = conv2(image,kernel);
% Display resulting image
figure; imshow(convolvedImage); title('Edges');
% Define the kernel - Sharpen
kernel = [ 0 -1  0;
          -1  5 -1;
           0 -1  0];
% Perform convolution
convolvedImage = conv2(image,kernel);
% Display resulting image
figure; imshow(convolvedImage); title('Sharpen');
% Display original image
figure; imshow(image); title('Original');
