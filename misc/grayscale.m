imagePath = ".\Labs\Lab4\tennisBall.jpg"
img = imread(imagePath);

imshow(img);

imgGray = rgb2gray(img);
imshow(imgGray); imwrite(imgGray, 'grayscaleTennisBallTexture.jpg')