import enchant

d = enchant.Dict("en_US")

f = open("SHEFFIELDDAT.txt",'r')
count_lines = 0
count_wrong = 0
count = 0
while 1:
	line = f.readline()
	line = line.strip('\n')
	count = count +1 
	if line :
		count_lines = count_lines + 1
		lineWords = line.split(' ')
		while '' in lineWords:
			lineWords.remove('')
		
		if not d.check(lineWords[1]):
			count_wrong = count_wrong + 1
		else:
			print lineWords
	else:
		break
print count_wrong,count_lines


