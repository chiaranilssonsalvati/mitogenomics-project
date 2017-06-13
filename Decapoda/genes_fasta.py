import sqlite3 as sq 

conn = sq.connect('decapoda.db')
c = conn.cursor()

gene = raw_input("Gene input: ")

out = open('Genes_Fastas/'+gene.replace(' ', '_')+'.fasta', 'w')

outputs = []
count = 0

for x in c.execute('select * from MitoGene_Location where gene_name = ?', (gene,)):
	outputs.append({})
	acc_num = x[0]
	seq = x[2]
	outputs[count]['acc_num'] = acc_num
	outputs[count]['seq'] = seq
	count += 1

print outputs

for num in range(len(outputs)):
	a = outputs[num]['acc_num']
	for y in c.execute('select species_name from Sequence_Info where acc_num = ?', (a,)):
			outputs[num]['species'] = y[0]

for entry in outputs:
	out.write('>'+entry['species']+' '+entry['acc_num']+'\n'+entry['seq']+'\n')

out.close()
conn.commit()
conn.close()