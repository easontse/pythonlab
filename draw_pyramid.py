i=0
layer=20
for i in range(layer):
	if i <= layer :
		a='*'*(i*2+1)
		print(a.center(layer*2))
	else:
		break
