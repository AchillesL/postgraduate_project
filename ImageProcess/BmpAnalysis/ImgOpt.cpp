// ImgOpt.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include <iostream>
#include <Windows.h>
#include <malloc.h>
#include <vector>

using namespace std;

string imgPath = "C:/Users/ZXX-PC/Desktop/lena-24位.bmp";
string saveImgPath = "C:/Users/ZXX-PC/Desktop/lena-24位-save.bmp";

//自定义了一个ImgInfo的结构体，包含BMP文件头、BMP信息头和像素点的RGB值。
//目前只支持24位图像的读取和显示

typedef struct{
	BITMAPFILEHEADER bf;
	BITMAPINFOHEADER bi;
	vector<vector<char>> imgData;
}ImgInfo;

//根据图片路径读取Bmp图像，生成ImgInfo对象
ImgInfo readBitmap(string imgPath) {
	ImgInfo imgInfo;
	char* buf;												//定义文件读取缓冲区
	char* p;

	FILE* fp;
	fopen_s(&fp, imgPath.c_str(), "rb");
	if (fp == NULL) {
		cout << "打开文件失败!" << endl;
		exit(0);
	}

	fread(&imgInfo.bf, sizeof(BITMAPFILEHEADER), 1, fp);
	fread(&imgInfo.bi, sizeof(BITMAPINFOHEADER), 1, fp);

	if (imgInfo.bi.biBitCount != 24){
		cout << "不支持该格式的BMP位图！" << endl;
		exit(0);
	}

	fseek(fp, imgInfo.bf.bfOffBits, 0);

	buf = (char*)malloc(imgInfo.bi.biWidth * imgInfo.bi.biHeight * 3);
	fread(buf, 1, imgInfo.bi.biWidth * imgInfo.bi.biHeight * 3, fp);

	p = buf;

	vector<vector<char>> imgData;
	for (int y = 0; y < imgInfo.bi.biHeight; y++){
		for (int x = 0; x < imgInfo.bi.biWidth; x++) {
			vector<char> vRGB;

			vRGB.push_back(*(p++));		//blue
			vRGB.push_back(*(p++));		//green
			vRGB.push_back(*(p++));		//red

			if (x == imgInfo.bi.biWidth - 1)
			{
				for (int k = 0; k < imgInfo.bi.biWidth % 4; k++) p++;
			}
			imgData.push_back(vRGB);
		}
	}
	fclose(fp);
	imgInfo.imgData = imgData;
	return imgInfo;
}

void showBitmap(ImgInfo imgInfo) {
	HWND hWindow;												 //窗口句柄
	HDC hDc;													 //绘图设备环境句柄
	int yOffset = 150;						
	hWindow = GetForegroundWindow();
	hDc = GetDC(hWindow);

	int posX, posY;
	for (int i = 0; i < imgInfo.imgData.size(); i++){
		char blue = imgInfo.imgData.at(i).at(0);
		char green = imgInfo.imgData.at(i).at(1);
		char red = imgInfo.imgData.at(i).at(2);

		posX = i % imgInfo.bi.biWidth;
		posY = imgInfo.bi.biHeight - i / imgInfo.bi.biWidth + yOffset;
		SetPixel(hDc, posX, posY, RGB(red, green, blue));
	}
}

void saveBitmap(ImgInfo imgInfo) {
	FILE* fpw;
	fopen_s(&fpw, saveImgPath.c_str(), "wb");
	fwrite(&imgInfo.bf, sizeof(BITMAPFILEHEADER), 1, fpw);  //写入文件头
	fwrite(&imgInfo.bi, sizeof(BITMAPINFOHEADER), 1, fpw);  //写入文件头信息

	int size = imgInfo.bi.biWidth * imgInfo.bi.biHeight;
	for (int i = 0; i < size; i++) {
		fwrite(&imgInfo.imgData.at(i).at(0), 1, 1, fpw);
		fwrite(&imgInfo.imgData.at(i).at(1), 1, 1, fpw);
		fwrite(&imgInfo.imgData.at(i).at(2), 1, 1, fpw);

		if (i % imgInfo.bi.biWidth == imgInfo.bi.biWidth - 1) {
			char ch = '0';
			for (int j = 0; j < imgInfo.bi.biWidth % 4; j++) {
				fwrite(&ch, 1, 1, fpw);
			}
		}
	}
	fclose(fpw);
	cout << "已保存图像至: " + saveImgPath << endl;
}

int main() {
	ImgInfo imgInfo = readBitmap(imgPath);
	showBitmap(imgInfo);
	saveBitmap(imgInfo);
}
