def getridofbadan():
	import csv
	bigdata = open('metadata.csv', 'r')
	readbig = csv.reader(bigdata)
	badan = open('badan.csv', 'r')
	readbad = csv.reader(badan)
	new = open('cleanmetadata.csv', 'w')
	writenew = csv.writer(new)

	writenew.writerow(readbig.next())
	readbad.next()

	bad = []
	for line in readbad:
		bad.append(line[0])

	for line in readbig:
		a_n = line[0]
		if a_n not in bad:
			writenew.writerow(line)


	bigdata.close()
	badan.close()
	new.close()