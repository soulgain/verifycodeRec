import os
import base64

dir = os.getcwd()

for _, _, paths in os.walk(dir):
	for path in paths:
		if path.split('/')[-1] == 'gen.py':
			continue

		f = open(path, 'r')
		o = open(path.replace('.txt', ''), 'w')
		o.write(base64.b64decode(f.read()))
		o.close()
		f.close()
