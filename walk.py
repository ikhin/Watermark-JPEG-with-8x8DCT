def findpoint(df,r):
	maxrow,maxcol=8,8
	#dire=-1向右上,dire=1向左下
	di={-1:(-1,1),1:(1,-1)}
	xydict={}
	while(r):	
		x,y,dire=df[0],df[1],df[2]
		#边界
		if x==-1:
			df=(0,y-2,1)
			continue
		if y==-1:
			df=(x-2,0,-1)
			continue
		if x==maxrow:
			df=(maxrow-1,y+2,-1)
			continue
		if y==maxcol:
			df=(x+2,maxcol-1,1)
			continue
		r=r-1
		xydict[r]=(x,y)
		dx,dy=x+di[dire][0],y+di[dire][1]
		df=(dx,dy,dire)
	return xydict
def fpg(bsrc):
	for i in range(bsrc.shape[0]):
		for j in range(bsrc.shape[1]):
			yield (i,j)
	while True:#让生成器不会报没东西返回的错
		yield (-1,-1)
	return

if __name__ == '__main__':
	print(findpoint((3,4,-1),24))
	