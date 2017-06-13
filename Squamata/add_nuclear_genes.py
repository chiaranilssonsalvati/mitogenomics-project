def add_nuclear_genes(email):
	import sqlite3 as sq
	import csv
	conn = sq.connect('squamata.db')
	c = conn.cursor()
	error_file = open('faulty_acc_nums.txt', 'w')

	from Bio import Entrez, SeqIO
	Entrez.email = email
	genes = ['SCN4a', 'PRLR', 'rhodopsin', 'alpha-enolase', 'PLA2', 'PNN', 'PTGER4', 'NGFB', '18S', 'DNAH3', 'BMP2', 'MKL1', 'SLC30A1', 'TRAF6', 'ZEB2', 'FSHR', 'SLC8A1', 'ZFP36L1', 'FSTL5', 'GPR37', 'LRRN1', 'AHR', 'CAND1', 'ENC1', 'HOXA13', 'VCPIP1', '28S', 'DLL', 'MC1R', 'PDC', 'ADNP', 'GAPD', 'AMEL', 'NT3', 'RAG2', 'SINCAIP', 'RAG1', 'ACM4', 'BDNF', 'CMOS', 'KIF24', 'ECEL', 'R35', 'PTPN']
	count = 1
	acc_nums = []
	for gene in genes:
		f = open('squamata_out/out'+gene+'.fasta', 'r')
		lines = f.readlines()
		print gene
		for l in range(len(lines)):
			if lines[l][0] == '>':
				line = lines[l]
				data = line[1:].split(' ')
				acc_num = data[-1].rstrip()
				words = data[:-1]
				species = ' '.join(words)
				seq = lines[l+1].rstrip()
				if acc_num not in acc_nums:
					acc_nums.append(acc_num)
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
				else:
					print acc_num + ' is a bad acc_num!!!'
					error_file.write(acc_num+'\n')
		f.close()

	# record = Entrez.read(handle)
	# ids = record["IdList"]
	# acc_num = []

	# dataOut = open("metadata.csv", "w")
	# writeData = csv.writer(dataOut)
	# headers=['acc_num', 'species', 'taxonomy', 'authors', 'journal', 'date', 'seq']
	# writeData.writerow(headers)


	# for i in ids:
		# handle = Entrez.efetch(db="nucleotide", id=i, rettype = "gb", retmode= "text")
		# record = SeqIO.parse(handle, "genbank")
		# r = next(record)

		# x=r.annotations['references'][-1].journal
		# start=x.find('(')
		# end=x.find(')')
		# info=[(r.annotations['accessions'][0]),(r.annotations['source']), (r.annotations['taxonomy']), (r.annotations['references'][-1].authors), x[end+2:],x[start+1:end], r.seq]
		# writeData.writerow(info)

	# 	# print r.features
	# 	# print r.annotations.keys()
	# 	# print r.annotations['source']

	# dataOut.close()
	conn.commit()
	conn.close()
	error_file.close()