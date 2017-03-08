import sys
import json

_dict = {}
for line in sys.stdin:
	data = line.strip().split('\t')
	key  = data[0]
	value = data[1]
	_dict[key] = value

print json.dumps(_dict, indent=4)