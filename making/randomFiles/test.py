with open('test.txt', 'w') as file:
	for x in range(10):
		msg = 'T' if (x%2 == 0) else 'F'
		file.write(msg)
