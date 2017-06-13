def populate_squam():
	import sqlite3 as sq
	import csv

	conn = sq.connect('squamata.db')
	c = conn.cursor()

	c.execute('DROP TABLE "Sequence_Info";')
	c.execute('DROP TABLE "Genes";')
	c.execute(
		'''CREATE TABLE "Sequence_Info"
		('acc_num' PRIMARY KEY,
		'sequence',
		'rotated_genome',
		'seq_type',
		'gene_ID',
		'species_name',
		'length',
		'authors',
		'publication',
		'date')
		'''
	);

	c.execute(
	'''CREATE TABLE "Genes"
	('gene_ID' PRIMARY KEY,
	'gene_name',
	'gene_type')
	'''
	);
	

	f = open('sequence_info.csv')
	sin = csv.reader(f)

	for line in sin:
		c.execute('''
			INSERT INTO Sequence_Info
			VALUES (?, ?, '', ?, ?, ?, ?, ?, ?, ?);
			''', (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8]))


	f.close()
	conn.commit()
	conn.close()

populate_squam()