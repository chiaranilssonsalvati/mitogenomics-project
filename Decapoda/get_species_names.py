import csv
datain = open('mitogenomes.csv', 'r')
txtout = open('species_names.txt', 'w')
din = csv.reader(datain)
for line in din:
	txtout.write(line[1]+'\n')


txtout.close()
datain.close()