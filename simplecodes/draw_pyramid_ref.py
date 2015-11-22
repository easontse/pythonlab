def draw_pyramid(layer):

	last_layer_star_count = layer * 2 - 1

	for current_layer in range(layer):
		star_count = current_layer * 2 - 1
		space_count = (last_layer_star_count - star_count)/2
		print((" " * space_count) + ("*" * star_count))

draw_pyramid(10)
