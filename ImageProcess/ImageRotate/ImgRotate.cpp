#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>

using namespace std;
using namespace cv;

int main(void)
{
    Mat imgMat = imread("C:/Users/ZXX-PC/Desktop/cat.png");

    float rotateAngle = 33 * 3.14159 / 180.0;
    int imgW = imgMat.cols;
    int imgH = imgMat.rows;

    //计算旋转后的图像的宽与高
    int newImgW = int(imgW * abs(cos(rotateAngle)) + imgH * abs(sin(rotateAngle))) + 1;
    int newImgH = int(imgW * abs(sin(rotateAngle)) + imgH * abs(cos(rotateAngle))) + 1;

    Mat fmapImgMat(newImgH, newImgW, CV_8UC3, Scalar::all(0));
    Mat bmapImgMat1(newImgH, newImgW, CV_8UC3, Scalar::all(0));
    Mat bmapImgMat2(newImgH, newImgW, CV_8UC3, Scalar::all(0));

    //前向映射
    for (int x0 = 0; x0 < imgW; x0++) {
        for (int y = 0; y < imgH; y++) {
            int x1 = int(x0 * cos(rotateAngle) - y * sin(rotateAngle) + (-0.5 * imgW * cos(rotateAngle) + 0.5 * imgH * sin(rotateAngle) + 0.5 * newImgW));
            int y1 = int(x0 * sin(rotateAngle) + y * cos(rotateAngle) + (-0.5 * imgW * sin(rotateAngle) - 0.5 * imgH * cos(rotateAngle) + 0.5 * newImgH));

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

            if (!(x0 > 0 && y0 > 0 && x0 < imgW && y0 < imgH))
                continue;
            bmapImgMat1.at<Vec3b>(y, x)[0] = imgMat.at<Vec3b>(y0, x0)[0];
            bmapImgMat1.at<Vec3b>(y, x)[1] = imgMat.at<Vec3b>(y0, x0)[1];
            bmapImgMat1.at<Vec3b>(y, x)[2] = imgMat.at<Vec3b>(y0, x0)[2];
        }
    }

    //后向映射-双线性插值法
    for (int x = 0; x < newImgW; x++) {
        for (int y = 0; y < newImgH; y++) {
            double x0_d = x * cos(rotateAngle) + y * sin(rotateAngle) + (-0.5 * newImgW * cos(rotateAngle) - 0.5 * newImgH * sin(rotateAngle) + 0.5 * imgW);
            double y0_d = -x * sin(rotateAngle) + y * cos(rotateAngle) + (0.5 * newImgW * sin(rotateAngle) - 0.5 * newImgH * cos(rotateAngle) + 0.5 * imgH);

            int x0 = int(x0_d);
            int y0 = int(y0_d);

            if (!(x0 > 0 && y0 > 0 && x0 < imgW - 1 && y0 < imgH - 1))
                continue;
            int x1 = x0 + 1;
            int y1 = y0 + 1;

            bmapImgMat2.at<Vec3b>(y, x)[0] = imgMat.at<Vec3b>(y0, x0)[0] * (x1 - x0_d) * (y1 - y0_d) +          //Q1
                                             imgMat.at<Vec3b>(y0, x0 + 1)[0] * (x0_d - x0) * (y1 - y0_d) +      //Q4
                                             imgMat.at<Vec3b>(y0 + 1, x0)[0] * (x1 - x0_d) * (y0_d - y0) +      //Q2
                                             imgMat.at<Vec3b>(y0 + 1, x0 + 1)[0] * (x0_d - x0) * (y0_d - y0);   //Q3

            bmapImgMat2.at<Vec3b>(y, x)[1] = imgMat.at<Vec3b>(y0, x0)[1] * (x1 - x0_d) * (y1 - y0_d) + 
                                             imgMat.at<Vec3b>(y0, x0 + 1)[1] * (x0_d - x0) * (y1 - y0_d) + 
                                             imgMat.at<Vec3b>(y0 + 1, x0)[1] * (x1 - x0_d) * (y0_d - y0) + 
                                             imgMat.at<Vec3b>(y0 + 1, x0 + 1)[1] * (x0_d - x0) * (y0_d - y0);

            bmapImgMat2.at<Vec3b>(y, x)[2] = imgMat.at<Vec3b>(y0, x0)[2] * (x1 - x0_d) * (y1 - y0_d) + 
                                             imgMat.at<Vec3b>(y0, x0 + 1)[2] * (x0_d - x0) * (y1 - y0_d) + 
                                             imgMat.at<Vec3b>(y0 + 1, x0)[2] * (x1 - x0_d) * (y0_d - y0) + 
                                             imgMat.at<Vec3b>(y0 + 1, x0 + 1)[2] * (x0_d - x0) * (y0_d - y0);
        }
    }

    // imshow("origin", imgMat);
    imshow("rotate-forward", fmapImgMat);
    imshow("rotate-backward-nearest", bmapImgMat1);
    imshow("rotate-backward-bilinear", bmapImgMat2);

    imwrite("C:/Users/ZXX-PC/Desktop/cat-f.png", fmapImgMat);
    imwrite("C:/Users/ZXX-PC/Desktop/cat-b-nearest.png", bmapImgMat1);
    imwrite("C:/Users/ZXX-PC/Desktop/cat-b-bilinear.png", bmapImgMat2);

    waitKey(0);
    return 0;
}
