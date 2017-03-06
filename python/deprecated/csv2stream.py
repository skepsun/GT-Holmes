import sys
import csv
import StringIO

csv.field_size_limit(sys.maxsize)

tag = sys.argv[1]
for line in sys.stdin:
	line = StringIO.StringIO(line)
	data = list(csv.reader(line, skipinitialspace=True))[0]
	data = [data[1], tag, data[5]]
	data = map(lambda x: ' '.join(x.split('\t')), data)
	data = map(lambda x: ' '.join(x.split('\n')), data)
	print '\t'.join(data)