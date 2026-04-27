% Befekir Belayneh
% receive images from blender
% send images to snickerdoodle
% wait for final processed images

function [left_proc, right_proc, uL, vL, uR, vR] = snickerdoodleLink(client, leftImg, rightImg, methodID)

    % get image size
    [height, width, ~] = size(leftImg);

    % format data for python (3, width, height)
    leftStack  = permute(leftImg,  [3 2 1]);
    rightStack = permute(rightImg, [3 2 1]);
    imageStack = cat(1, leftStack, rightStack); 

    % send header
    disp("Sending header");
    header = typecast(uint32([width height]), 'uint8');
    write(client, header);

    % send image data
    disp("Sending image data");
    write(client, imageStack(:), "uint8");

    % send methodID (1 byte)
    disp("Sending methodID");
    write(client, methodID, "uint8");

    % receive processed data
    disp("Reading Left Image");
    imgBytes = width * height;

    left_data  = readExact(client, imgBytes);
    disp("Reading Right Image");
    right_data = readExact(client, imgBytes);

    % Receive centroid data (4 floats)
    disp("Reading centroid");
    centroid_raw = readExact(client, 16);
    disp("parsing centroids");
    centroids = typecast(uint8(centroid_raw), 'single');

    disp("Assigning Outputs");
    uL = double(centroids(1));
    vL = double(centroids(2));
    uR = double(centroids(3));
    vR = double(centroids(4));

    % reshape back to images
    left_proc  = reshape(left_data,  [width, height]);
    right_proc = reshape(right_data, [width, height]);

    % convert to H x W
    left_proc  = permute(left_proc,  [2 1]);
    right_proc = permute(right_proc, [2 1]);

    % fix orientation
    left_proc  = flipud(left_proc);
    right_proc = flipud(right_proc);

end
