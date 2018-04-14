import cv2 as cv  
import numpy as np
import math
import walk	
def embed(srcs):
	#正方形水印图片-指纹
	src=cv.imread(srcs)    
	src=cv.bitwise_not(src)  
	#水印图片灰度图
	graysrc=cv.cvtColor(src,cv.COLOR_BGR2GRAY)  
	# cv.imshow('graysrc',graysrc)
	#中值滤波
	medianblurimg=cv.medianBlur(graysrc,3)
	# cv.imshow('medianblurimg',medianblurimg)
	#将灰度图通过一个阈值分割,进行二值化:
	#小于70置为255白,大于70置为0黑
	ret,bsrc = cv.threshold(graysrc,70,255,1)  
	cv.imshow('source',bsrc)
	cv.imwrite('embedfinger.jpg',bsrc,
		[int(cv.IMWRITE_JPEG_QUALITY),100])

	#宿主图片
	host=cv.imread('host.jpg')  
	#宿主图片YUV化
	hostyuv=cv.cvtColor(host,cv.COLOR_RGB2YUV)  
	#转成float32是DCT必要条件
	hostf=hostyuv.astype('float32')

	#嵌入过程
	#目标完成图
	finishwm=hostf
	#目标完成的8x8划分观察图
	#发现如果wmblocks=hostf,那么修改wmblocks等于修改hostf,这说明这两是指针,这里指向图像的变量都是指针
	wmblocks=np.zeros([hostf.shape[0],hostf.shape[1],3],np.float32)
	wmblocks[:,:,:]=hostf[:,:,:]
	#8x8块作为单位而拼成的矩阵的行数,列数
	part8x8rownum=int(host.shape[0]/8)
	part8x8colnum=int(host.shape[1]/8)
	#指纹像素点总数
	fingernum=bsrc.shape[0]*bsrc.shape[1]
	#r是每个8x8块要存的指纹像素点数目
	# r=math.ceil(fingernum/(part8x8rownum*part8x8colnum))
	r=math.ceil(fingernum/(part8x8rownum*part8x8colnum))
	print("r=",r)
	#在8x8块的单位格子,分别与其中心的对称的单位格子,成一对
	#每一对的大小关系(前者比后者大,前者比后者小)用来记录要存的指纹像素点的黑与白
	#从中间往右上方走格子,为产生格子对做准备
	xydict=walk.findpoint((3,4,-1),r)
	#指纹像素点生成器
	fpgij=walk.fpg(bsrc)
	#遍历8x8块
	count=0
	flag=0
	for parti in range(part8x8rownum):
		if (flag):
			break
		for partj in range(part8x8colnum):
			if (flag):
				break
			#8x8块进行DCT
			part8x8=cv.dct(hostf[8*parti:8*parti+8,8*partj:8*partj+8,0])
			#不考虑不够8x8大小的块
			if (part8x8.shape[0]<8)|(part8x8.shape[1]<8):
				continue
			#每个8x8dct块存r个指纹像素点
			for t in range(r):
				if (flag):
					break
				#通过生成器得到此刻要存的指纹像素点
				i,j=next(fpgij)
				if (i==-1&j==-1):
					flag=1
				#指纹像素点要用的格子坐标
				rx,ry=xydict[t]
				#修改r1和r2的大小关系,来反映水印像素点黑白情况
				r1=part8x8[rx,ry]
				r2=part8x8[7-rx,7-ry]#r1的中心对称格子
				detat=abs(r1-r2)
				p=float(detat+0.1)#嵌入深度
				if bsrc[i,j]==0:#0黑的,指纹主体,用r1>r2来记录
					if(r1<=r2):#一定要让r1大于r2
						part8x8[rx,ry]+=p
				else:#255白的,用r1<r2来记录
					if(r1>=r2):
						part8x8[7-rx,7-ry]+=p
				if not flag:
					count+=1
			#存完r个指纹像素点后,对此8x8块进行逆DCT
			finishwm[8*parti:8*parti+8,8*partj:8*partj+8,0]=cv.idct(part8x8)
			wmblocks[8*parti:8*parti+8,8*partj:8*partj+8,0]=finishwm[8*parti:8*parti+8,8*partj:8*partj+8,0]
			#&要用括号连接,给8x8划线
			if (wmblocks.shape[0]>8*parti+7)&(wmblocks.shape[1]>8*partj+7):
				wmblocks[8*parti:8*parti+8,8*partj+7,0]=100
				wmblocks[8*parti+7,8*partj:8*partj+8,0]=100
	wmrgb=cv.cvtColor(finishwm.astype('uint8'),cv.COLOR_YUV2RGB) 	
	#划线图
	cv.imshow('wmblocks',cv.cvtColor(wmblocks.astype('uint8'),cv.COLOR_YUV2RGB) )
	cv.waitKey(0)  
	cv.destroyAllWindows()	
	#图像保存的质量,要为100,默认为95
	for x in range(6):
		name="finishwm"+str(x)
		filename=name+".jpg"
		cv.imwrite(filename,wmrgb,[int(cv.IMWRITE_JPEG_QUALITY),100-x])
		img=cv.imread(filename)
		cv.namedWindow(name,0)	
		k=480
		cv.resizeWindow(name,k,int(k*img.shape[0]/img.shape[1]));
		cv.imshow(name,img)

	print("countembed=",count)


def main():
	embed('fingerprint.jpg')
	cv.waitKey(0)  
	cv.destroyAllWindows()
if __name__ == '__main__':
	main()
