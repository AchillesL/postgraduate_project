#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main(void)
{
    Mat imgMat = imread("C:/Users/Administrator/Desktop/lena.png");

    float rotateAngle = 10 * 3.14159 / 180.0;
    int imgW = imgMat.cols;
    int imgH = imgMat.rows;
    printf("imgW:%d,imgH:%d",imgW,imgH);
    int newImgW = int(imgW * abs(cos(rotateAngle)) + imgH * abs(sin(rotateAngle))) + 1;
    int newImgH = int(imgW * abs(sin(rotateAngle)) + imgH * abs(cos(rotateAngle))) + 1;

    printf("newImgW:%d,H:%d",newImgW,newImgH);

    Mat newImgMat(newImgH,newImgW,CV_8UC3);

    for(int x0 = 0;x0<imgW;x0++) {
        for(int y0 = 0;y0<imgH;y0++) {
            int x = int(x0 * cos(rotateAngle) - y0 * sin(rotateAngle) + (-0.5 * imgW * cos(rotateAngle) + 0.5 * imgH * sin(rotateAngle) + 0.5 * newImgW));
            int y = int(x0 * sin(rotateAngle) - y0 * cos(rotateAngle) + (-0.5 * imgW * sin(rotateAngle) - 0.5 * imgH * cos(rotateAngle) + 0.5 * newImgH));

            if(x0==0)
            printf("x0:%d,y0:%d,x:%d,y:%d\n",x0,y0,x,y);

            if(x<0 || y<0 || x>newImgW || y>newImgH) continue;
            
            newImgMat.at<Vec3b>(y,x)[0] = imgMat.at<Vec3b>(y0,x0)[0];
            newImgMat.at<Vec3b>(y,x)[1] = imgMat.at<Vec3b>(y0,x0)[1];
            newImgMat.at<Vec3b>(y,x)[2] = imgMat.at<Vec3b>(y0,x0)[2];
        }
    }

    imshow("origin",imgMat);
    imshow("rotate",newImgMat);
    waitKey(0);
    return 0;
}
