cutoff = 10;
order = 2;

image=double(imread('tun.jpg'));

[x, y]=size(image);

%log
image_logued=log2(1+image);

%DFT
image_dft=fft2(image_logued);

%Filter

A=zeros(x,y);
for i=1:x
    for j=1:y
        A(i,j)=(((i-x/2).^2+(j-y/2).^2)).^(.5);
        H(i,j)=1/(1+((d/A(i,j))^(2*n)));
    end
end

Yh=.0999;
Yl=1.01;

H=((Yl-Yh).*H)+Yh;
H=1-H;

image_f=H.*image_dft;

%Inverse DFT
image_n=abs(ifft2(image_f));

%Inverse log
image_final=exp(image_n);

figure, imshow((image_final),[])
