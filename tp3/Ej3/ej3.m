% This is a MATLAB script

% Leo la imagen
image = imread('eight.tif');
imshow(I)

% Agrego ruido a la imagen
image1 = imnoise(image, 'salt & pepper', 0.02);
figure, imshow(image1)


% Filtrada con pasa bajos
image2 = filter2(fspecial('average', 3), image1) / 255;
figure, imshow(image2)

% Con filtro mediana
image3 = medfilt2(image1, [3 3]);
figure, imshow(image3)
