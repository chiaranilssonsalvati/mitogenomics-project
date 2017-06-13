import sqlite3 as sq 

conn = sq.connect('squamata.db')
c = conn.cursor()

# gene = raw_input("Gene input: ")

out = open('ToRotate.fasta', 'w')


outputs = []
count = 0

for x in c.execute('select start, end, Sequence_Info.sequence from MitoGene_Location INNER JOIN Sequence_Info ON MitoGene_Location.acc_num = Sequence_Info.acc_num WHERE MitoGene_Location.gene_name = "COX1" '):
	outputs.append({})
	start = x[0]
	end = x[1]
	seq = x[2]
	outputs[count]['start'] = start
	outputs[count]['end'] = end
	outputs[count]['seq'] = seq

	count += 1

for entry in outputs:
	out.write(entry['start']+' '+entry['end']+' '+entry['seq']+'\n')

out.close()
conn.commit()
conn.close()