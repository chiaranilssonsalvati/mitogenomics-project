def populate_dec():
	import sqlite3 as sq
	import csv

	conn = sq.connect('decapoda.db')
	c = conn.cursor()

	c.execute('DROP TABLE "MitoGene_Location";')
	c.execute('DROP TABLE "Species_Info";')

	c.execute(
		'''CREATE TABLE "MitoGene_Location"
		('acc_num',
		'gene_name',
		'sequence',
		'length',
		'start',
		'end',
		'orientation',
		'sign')
		'''
	);

	
	c.execute(
	'''CREATE TABLE "Species_Info"
	('species_name' PRIMARY KEY,
	'taxonomy_original',
	'taxonomy_cut')
	'''
	);

	i = open('mitogene_location.csv','r')
	mgl = csv.reader(i)
	j= open('species_info.csv', 'r')
	spec = csv.reader(j)

	for line in mgl:
		c.execute('''
			INSERT INTO MitoGene_Location
			VALUES (?, ?, ?, ?, ?, ?, ?, ?);
			''', (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))

	for line in spec:
		c.execute('''
			INSERT OR IGNORE INTO Species_Info
			VALUES (?, ?, ?)
			''', (line[0], line[1], line[2]))
	
	i.close()
	j.close()
	conn.commit()
	conn.close()