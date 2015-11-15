a = [1,3,5,5]
if len(a) == len(list(set(a))):
	print("There is no repeated result.")
else:
	print("repeated result found")

#better
result = not(len(a)==len(set(a)))
print(result)

def is_duplicated(sequence):
	return not( len(sequence) == len(set(sequence)) )

print(is_duplicated(a))