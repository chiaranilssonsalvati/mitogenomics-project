def add_nuclear_genes(email):
	import sqlite3 as sq
	import csv
	conn = sq.connect('decapoda.db')
	c = conn.cursor()
	error_file = open('faulty_acc_nums.txt', 'w')

	from Bio import Entrez, SeqIO
	Entrez.email = email
	genes = ['18S', '28S']
	count = 1
	acc_nums = []
	faulty_an = []
	for gene in genes:
		f = open('decapoda_out/out'+gene+'.fasta', 'r')
		lines = f.readlines()
		print gene
		for l in range(len(lines)):
			line = lines[l]
			data = line[1:].split(' ')
			if lines[l][0] == '>':
				acc_num = data[-1].rstrip()
				if acc_num in acc_nums:
					error_file.write(acc_num+'\n')
					faulty_an.append(acc_num)
				else:
					acc_nums.append(acc_num)
				
	for gene in genes:
		f = open('decapoda_out/out'+gene+'.fasta', 'r')
		lines = f.readlines()
		for l in range(len(lines)):
			if lines[l][0] == '>':
				line = lines[l]
				data = line[1:].split(' ')
				acc_num = data[-1].rstrip()

				words = data[:-1]
				species = ' '.join(words)
				seq = lines[l+1].rstrip()

				if acc_num not in faulty_an:
					handle = Entrez.efetch(db="nucleotide", id=acc_num, rettype = "gb", retmode= "text")
					record = SeqIO.parse(handle, "genbank")
					r = next(record)
					try:
						x=r.annotations['references'][-1].journal
						start=x.find('(')
						end=x.find(')')
						authors = r.annotations['references'][-1].authors
						pub = x[end+2:]
						date = x[start+1:end]
					except KeyError:
						authors = ' '
						pub = ' '
						date = ' '
					c.execute("INSERT INTO Sequence_Info VALUES (?, ?, '', 'n', ?, ?, ?, ?, ?, ?)", (acc_num, seq, 'gene'+str(count), species, len(seq), authors, pub, date))
					c.execute("INSERT INTO Genes VALUES (?, ?, 'n')", ('gene'+str(count), gene))
					count += 1
				



		f.close()
	error_file.close()

	conn.commit()
	conn.close()