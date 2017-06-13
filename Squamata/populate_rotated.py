def populate_rotated():
	import sqlite3 as sq
	import csv

	conn = sq.connect('squamata.db')
	c = conn.cursor()

	c.execute('DROP TABLE "Rotated_Info";')

	c.execute(
		'''CREATE TABLE "Rotated_Info"
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

	# x = c.execute('''
	# 	INSERT INTO Rotated_Info
	# 	VALUES (?, ?, ?, ?, ?, ?, ?, ?);
	# 	''', (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))

	cox_locs = {}
	for a in c.execute("SELECT start, Sequence_Info.sequence, Sequence_Info.acc_num from MitoGene_Location INNER JOIN Sequence_Info ON MitoGene_Location.acc_num = Sequence_Info.acc_num where MitoGene_Location.gene_name = 'COX1'"):
		cox_locs[a[2]] = [a[0], a[1]] #start of COX1, sequence of genome

	for key in cox_locs.keys():
		info = cox_locs[key]
		rotated = info[1][int(info[0]):]+info[1][:int(info[0])]
		cox_locs[key][1] = rotated

	for an in cox_locs.keys():
		x = c.execute("SELECT * from MitoGene_Location where acc_num = ?", (an,))
		data = []
		for entry in x:
			data.append(entry)
		c.execute('''UPDATE Sequence_Info SET rotated_genome = ? WHERE acc_num = ?;''', (cox_locs[an][1], an))
		len_genome = len(cox_locs[an][1])
		cox_start = int(cox_locs[an][0])
		shift = int(cox_start)
		for line in data:
			c.execute('''INSERT INTO Rotated_Info VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', (line[0], line[1], line[2], line[3], (int(line[4])-shift)%len_genome, (int(line[5])-shift)%len_genome, line[6], line[7]))

	# for line in lines:
		

	conn.commit()
	conn.close()

populate_rotated()
