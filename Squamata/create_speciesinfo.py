def create_speciesinfo():
	import csv
	import sqlite3 as sq

	conn = sq.connect('squamata.db')
	c = conn.cursor()
	#contains species_name, taxonomy_original, taxonomy_cut
	speciesin=open('cleanmetadata.csv','r')
	read=csv.reader(speciesin)

	speciesout=open('species_info.csv','w')
	write=csv.writer(speciesout)

	read.next()

	for line in read:
		if "(" in line[1]:
			end = line[1].find('(')-1
		else:
			end = len(line[1])
		name=line[1][14:end]

		species_name = name
		taxonomy_original = line[2]

		cut = line[2].find('Squamata')
		taxonomy_cut="['"+line[2][cut:]

		write.writerow([species_name, taxonomy_original, taxonomy_cut])

	speciesin.close()
	speciesout.close()
	conn.commit()
	conn.close()

