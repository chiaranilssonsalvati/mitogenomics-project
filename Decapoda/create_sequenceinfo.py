def create_sequenceinfo():
	import csv
	datain = open('cleanmetadata.csv', 'r')
	dataout = open('sequence_info.csv', 'w')
	read = csv.reader(datain)
	write = csv.writer(dataout)

	read.next()

	for line in read:
		if "(" in line[1]:
			end = line[1].find('(')
		else:
			end = len(line[1])
		l = line[1][14:end]
		while l[-1] == ' ':
			l = l[:-1]
		write.writerow([line[0], line[-1], 'm', None, l, len(line[-1]), line[3], line[4], line[5]])


	datain.close()
	dataout.close()