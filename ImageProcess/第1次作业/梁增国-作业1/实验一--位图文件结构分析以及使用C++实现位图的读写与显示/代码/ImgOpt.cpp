#include <iostream>
#include <Windows.h>
#include <malloc.h>
#include <vector>

using namespace std;

string imgPath = "C:/Users/ZXX-PC/Desktop/lena-24位.bmp";
string saveImgPath = "C:/Users/ZXX-PC/Desktop/lena-24位-save.bmp";

typedef struct {
	BITMAPFILEHEADER bf;
	BITMAPINFOHEADER bi;

	//用于存放8位、24位位图像素点的像素值
	vector<vector<unsigned char>> imgData;

	//用于存放8位位图的调色板项
	vector<vector<unsigned char>> imgPalette;

	//用于存放8位位图数据的调色板索引值
	vector<unsigned char> imgPaletteIndexList;

}ImgInfo;

//根据图片路径读取Bmp图像，生成ImgInfo对象
ImgInfo readBitmap(string imgPath) {
	ImgInfo imgInfo;
	unsigned char* buf;												//定义文件读取缓冲区
	unsigned char* p;

	FILE* fp;
	fopen_s(&fp, imgPath.c_str(), "rb");
	if (fp == NULL) {
		cout << "打开文件失败!" << endl;
		exit(0);
	}

	fread(&imgInfo.bf, sizeof(BITMAPFILEHEADER), 1, fp);
	fread(&imgInfo.bi, sizeof(BITMAPINFOHEADER), 1, fp);

	if (imgInfo.bf.bfType != 0x4d42) {
		cout << "打开文件失败，请打开BMP格式位图！" << endl;
		exit(0);
	}

	if (imgInfo.bi.biBitCount == 8) {
		int headerSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
		fseek(fp, headerSize, 0);

		int paletteSize = imgInfo.bf.bfOffBits - headerSize;				//计算调色板占用字节数			
		buf = (unsigned char*)malloc(paletteSize);
		fread(buf, 1, paletteSize, fp);

		p = buf;
		int paletteNum = paletteSize / 4;

		//读取调色板的颜色值，存放到imgPalette字段中
		for (int i = 0; i < paletteNum; i++) {
			vector<unsigned char> bgr(4);
			bgr[0] = (*(p++));
			bgr[1] = (*(p++));
			bgr[2] = (*(p++));
			bgr[3] = (*(p++));

			imgInfo.imgPalette.push_back(bgr);
		}

		fseek(fp, imgInfo.bf.bfOffBits, 0);
		buf = (unsigned char*)malloc(imgInfo.bi.biSizeImage);
		fread(buf, 1, imgInfo.bi.biSizeImage, fp);

		p = buf;

		int offsetBytes = 4 - (imgInfo.bi.biWidth * imgInfo.bi.biBitCount / 8) % 4;

		//存储位图数据
		for (int y = 0; y < imgInfo.bi.biHeight; y++) {
			for (int x = 0; x < imgInfo.bi.biWidth; x++) {
				unsigned char ch = *(p++);
				//将像素点对应调色板的像素值，存入到imgData字段
				imgInfo.imgData.push_back(imgInfo.imgPalette.at(ch));
				//将像素点对应调色板的索引值，存入到imgPaletteIndexList字段
				imgInfo.imgPaletteIndexList.push_back(ch);

				//做4字节对齐处理
				if (x == imgInfo.bi.biWidth - 1) {
					for (int i = 0; i < offsetBytes; i++) p++;
				}
			}
		}

		fclose(fp);
		return imgInfo;
	}
	else if (imgInfo.bi.biBitCount == 24) {
		fseek(fp, imgInfo.bf.bfOffBits, 0);

		buf = (unsigned char*)malloc(imgInfo.bi.biWidth * imgInfo.bi.biHeight * 3);
		fread(buf, 1, imgInfo.bi.biWidth * imgInfo.bi.biHeight * 3, fp);

		p = buf;

		vector<vector<unsigned char>> imgData;
		//24位BMP图像没有调色板，可直接读取位图的像素值数据
		for (int y = 0; y < imgInfo.bi.biHeight; y++) {
			for (int x = 0; x < imgInfo.bi.biWidth; x++) {
				vector<unsigned char> vRGB;

				vRGB.push_back(*(p++));		//blue
				vRGB.push_back(*(p++));		//green
				vRGB.push_back(*(p++));		//red

				if (x == imgInfo.bi.biWidth - 1) {
					//计算需要跳过多少位填充字节
					int offsetBytes = 4 - int(imgInfo.bi.biWidth * imgInfo.bi.biBitCount / 8) % 4;
					for (int k = 0; k < offsetBytes; k++) p++;
				}
				imgData.push_back(vRGB);
			}
		}
		fclose(fp);
		imgInfo.imgData = imgData;
		return imgInfo;
	}
	else {
		cout << "不支持该格式位图!" << endl;
		exit(0);
	}
}

void showBitmap(ImgInfo imgInfo) {
	HWND hWindow;												 //窗口句柄
	HDC hDc;													 //绘图设备环境句柄
	int yOffset = 150;
	hWindow = GetForegroundWindow();
	hDc = GetDC(hWindow);

	int posX, posY;
	for (int i = 0; i < imgInfo.imgData.size(); i++) {
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

	//保存8位图像
	if (imgInfo.bi.biBitCount == 8) {
		//写入位图的调色板数据
		for (int i = 0; i < imgInfo.imgPalette.size(); i++) {
			for (int j = 0; j < 4; j++) {
				fwrite(&imgInfo.imgPalette[i][j], 1, 1, fpw);
			}
		}
		int offsetBytes = 4 - int(imgInfo.bi.biWidth * imgInfo.bi.biBitCount / 8) % 4;
		//写入像素在调色板中的索引值
		for (int j = 0; j < imgInfo.imgPaletteIndexList.size(); j++) {
			fwrite(&imgInfo.imgPaletteIndexList[j], 1, 1, fpw);
			if (j % imgInfo.bi.biWidth == imgInfo.bi.biWidth - 1) {
				char ch = '0';
				//计算需要加入多少填充字节，实现4字节对齐
				for (int k = 0; k < offsetBytes; k++)  fwrite(&ch, 1, 1, fpw);
			}
		}
	}
	//保存24位图像，直接写入像素的BGR值
	else if (imgInfo.bi.biBitCount == 24) {
		int size = imgInfo.bi.biWidth * imgInfo.bi.biHeight;
		for (int i = 0; i < size; i++) {
			fwrite(&imgInfo.imgData.at(i).at(0), 1, 1, fpw);
			fwrite(&imgInfo.imgData.at(i).at(1), 1, 1, fpw);
			fwrite(&imgInfo.imgData.at(i).at(2), 1, 1, fpw);

			if (i % imgInfo.bi.biWidth == imgInfo.bi.biWidth - 1) {
				char ch = '0';
				//计算需要加入多少填充字节
				int offsetBytes = 4 - int(imgInfo.bi.biWidth * imgInfo.bi.biBitCount / 8) % 4;
				for (int j = 0; j < offsetBytes; j++) {
					fwrite(&ch, 1, 1, fpw);
				}
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
