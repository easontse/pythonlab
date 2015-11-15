i=0
layer=10
for i in range(layer):
	if i <= layer :
		a='*'*(i*2+1)
		print(a.center(layer*2))
	else:
		break

def draw_pyrameid(layer):

	last_layer_star_count = layer * 2 - 1

	for current_layer in range(layer):
		star_count = current_layer * 2 - 1
		space_count = (last_layer_star_count - star_count)/2
		print((" " * space_count) + ("*" * star_count))

draw_pyrameid(10)