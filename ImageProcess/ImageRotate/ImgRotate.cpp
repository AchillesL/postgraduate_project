#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main(void) {
    Mat imgMat = imread("C:/Users/ZXX-PC/Desktop/lena.png");

    float rotateAngle = 210 * 3.14159 / 180.0;
    int imgW = imgMat.cols;
    int imgH = imgMat.rows;

    //计算旋转后的图像的宽与高
    int newImgW = int(imgW * abs(cos(rotateAngle)) + imgH * abs(sin(rotateAngle))) + 1;
    int newImgH = int(imgW * abs(sin(rotateAngle)) + imgH * abs(cos(rotateAngle))) + 1;

    Mat fmapImgMat(newImgH, newImgW, CV_8UC3, Scalar::all(0));
    Mat bmapImgMat(newImgH, newImgW, CV_8UC3, Scalar::all(0));

    //前向映射
    for (int x0 = 0; x0 < imgW; x0++) {
        for (int y = 0; y < imgH; y++) {
            int x1 = int(x0 * cos(rotateAngle) - y * sin(rotateAngle) + 
                    (-0.5 * imgW * cos(rotateAngle) + 0.5 * imgH * sin(rotateAngle) + 0.5 * newImgW));
            int y1 = int(x0 * sin(rotateAngle) + y * cos(rotateAngle) + 
                    (-0.5 * imgW * sin(rotateAngle) - 0.5 * imgH * cos(rotateAngle) + 0.5 * newImgH));

            fmapImgMat.at<Vec3b>(y1, x1)[0] = imgMat.at<Vec3b>(y, x0)[0];
            fmapImgMat.at<Vec3b>(y1, x1)[1] = imgMat.at<Vec3b>(y, x0)[1];
            fmapImgMat.at<Vec3b>(y1, x1)[2] = imgMat.at<Vec3b>(y, x0)[2];
        }
    }

    //后向映射-最邻近算法
    for (int x = 0; x < newImgW; x++) {
        for (int y = 0; y < newImgH; y++) {
            int x0 = int(x * cos(rotateAngle) + y * sin(rotateAngle) + 
                     (-0.5 * newImgW * cos(rotateAngle) - 0.5 * newImgH * sin(rotateAngle) + 0.5 * imgW) + 0.5);
            int y0 = int(-x * sin(rotateAngle) + y * cos(rotateAngle) + 
                     (0.5 * newImgW * sin(rotateAngle) - 0.5 * newImgH * cos(rotateAngle) + 0.5 * imgH) + 0.5);

            if (!(x0 > 0 && y0 > 0 && x0 < imgW && y0 < imgH)) continue;
            bmapImgMat.at<Vec3b>(y, x)[0] = imgMat.at<Vec3b>(y0, x0)[0];
            bmapImgMat.at<Vec3b>(y, x)[1] = imgMat.at<Vec3b>(y0, x0)[1];
            bmapImgMat.at<Vec3b>(y, x)[2] = imgMat.at<Vec3b>(y0, x0)[2];
        }
    }

    imshow("origin", imgMat);
    imshow("rotate-forward", fmapImgMat);
    imshow("rotate-backward", bmapImgMat);

    imwrite("C:/Users/ZXX-PC/Desktop/lena-f.png",fmapImgMat);
    imwrite("C:/Users/ZXX-PC/Desktop/lena-b.png",bmapImgMat);

    waitKey(0);
    return 0;
}
