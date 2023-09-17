cutoff = 10;
order = 2;

im=double(imread('tun.jpg'));

[x, y]=size(im);


%Butterworth filter
A=zeros(x,y);
for i=1:x
    for j=1:y
        A(i,j)=(((i-x/2).^2+(j-y/2).^2)).^(.5);
        H(i,j)=1/(1+((d/A(i,j))^(2*n)));
    end
end

alphaL=.0999;
aplhaH=1.01;

H=((aplhaH-alphaL).*H)+alphaL;
H=1-H;

%log
im_l=log2(1+im);

%DFT
im_f=fft2(im_l);

%Filter
im_nf=H.*im_f;

%Inverse DFT
im_n=abs(ifft2(im_nf));

%Inverse log
im_e=exp(im_n);

figure, imshow((im_e),[])
