import sqlite3 as sq 
import csv
conn = sq.connect('../decapoda.db')
c = conn.cursor()

dataout = open('VizGene.csv', 'w')
write = csv.writer(dataout)

write.writerow(['gene', 'length', 'type', 'strand'])

def generate_type(gene):
	# gene, tRNA, rRNA, d-loop
	if gene == 'control region':
		return 'd-loop'
	elif gene == '12S' or gene == '16S':
		return 'rRNA'
	elif gene == 'COX1' or gene == 'COX2' or gene == 'ATP8' or gene == 'ATP6' or gene == 'NADH3' or gene == 'COX3' or gene == 'NADH5' or gene == "NADH4" or gene == 'NADH4L' or gene == 'NADH6' or gene == 'CYTB' or gene == 'NADH1' or gene == "NADH2":
		return 'gene'
	else:
		return 'tRNA'

for x in c.execute('select gene_name, length, orientation from Rotated_Info where acc_num = ? ORDER BY CAST(start as decimal) ASC', ('KT074365',)): #'KT074365'
	gene_name = x[0]
	length = x[1]
	typegene = generate_type(gene_name)
	strand=x[2]

	write.writerow([gene_name, length, typegene, strand])

dataout.close()
conn.commit()
conn.close()