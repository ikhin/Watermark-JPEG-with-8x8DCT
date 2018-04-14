import cv2 as cv  
import numpy as np  
import math
import walk
def extract(src,dst):
	wmrgb=cv.imread(src)
	wmyuv=cv.cvtColor(wmrgb,cv.COLOR_RGB2YUV) 
	wmf=wmyuv.astype('float32')
	part8x8rownum=int(wmf.shape[0]/8)
	part8x8colnum=int(wmf.shape[1]/8)
	#由r和宿主图像暂时猜测最大的正方形水印图像大小
	r=5
	fingernum=230
	extractxydict=walk.findpoint((3,4,-1),r)
	#还原水印的最大空载体
	finishfinger=np.zeros([fingernum,fingernum,3],np.uint8)
	i,j=0,0
	count=0
	flag=0
	for parti in range(part8x8rownum):
		for partj in range(part8x8colnum):
			#不考虑不够8x8大小的块
			part8x8=cv.dct(wmf[8*parti:8*parti+8,8*partj:8*partj+8,0])
			if (part8x8.shape[0]<8)|(part8x8.shape[1]<8):
				continue
			#每个8x8dct块存r个指纹像素点
			for t in range(r):
				if (i==fingernum):
					break
				#指纹像素点应该在的格子坐标
				rx,ry=extractxydict[t]
				#观察r1和r2的大小关系,得出水印像素点黑白情况
				r1=part8x8[rx,ry]
				r2=part8x8[7-rx,7-ry]#r1的中心对称格子
				if r1>r2:
					finishfinger[i,j]=0#黑
				else:
					if r1<r2:
						finishfinger[i,j]=255#白
				j+=1
				if (j==fingernum):
					j=0
					i=i+1
				count+=1
	print("countextract=",count)
	cv.imwrite(dst,finishfinger,[int(cv.IMWRITE_JPEG_QUALITY),100])
def main():
	for x in range(6):
		wmname="finishwm"+str(x)
		exname=str(x)+"extractfinger"
		extract(wmname+".jpg",exname+".jpg")
		img=cv.imread(exname+".jpg")
		cv.namedWindow(exname,0)	
		k=240
		cv.resizeWindow(exname,k,int(k*img.shape[0]/img.shape[1]));
		cv.imshow(exname,img)


if __name__ == '__main__':
	main()
	cv.waitKey(0)  
	cv.destroyAllWindows()