def nuclear_genes(email):
	import sqlite3 as sq
	import csv
	import time

	# to run this file, make sure it starts running during GenBank off-peak hours!
	# time.sleep(21600)

	from Bio import Entrez, SeqIO
	Entrez.email = email

	conn = sq.connect('squamata.db')
	c = conn.cursor()
	
	# values = multiple names for same gene
	# key = gene name that will be stored in fasta file
	genes = {
	'CMOS': ['C-MOS', 'c-mos oocyte maturation factor-like', 'CMOS sarcoma viral oncogene-like protein'],
	'RAG1': ['RAG-1', 'RAG1'],
	'BDNF': ['BDNF', 'BNDF'],
	'GAPD': ['GAPD', 'gapdh'],
	'R35': ['R35', 'GPR149'],
	'RAG2': ['RAG-2', "RAG2"],
	'ACM4': ['ACM4', 'CHRM4'],
	'NT3': ['NT-3', 'NT3', 'NTF3'],
	'KIF24': ['KIF24', 'kinesin family member 24'],
	'SINCAIP': ['SINCAIP', 'SNCAIP'],
	'PTPN': ['PTPN', 'PTPN12'],
	'ECEL': ['ECEL', 'ECEL1'],
	'AMEL': ['amelogenin', 'AMEL']
	}

	# genes that only have one name
	other_genes = ['SCN4a', 'PRLR', 'rhodopsin', 'alpha-enolase', 'PLA2', 'PNN', 'PTGER4', 'NGFB', '18S', 'DNAH3', 'BMP2', 'MKL1', 'SLC30A1', 'TRAF6', 'ZEB2', 'FSHR', 'SLC8A1', 'ZFP36L1', 'FSTL5', 'GPR37', 'LRRN1', 'AHR', 'CAND1', 'ENC1', 'HOXA13', 'VCPIP1', '28S', 'DLL', 'MC1R', 'PDC', 'ADNP']
	for x in c.execute('select species_name from Species_Info'):
		species = x[0]
		for k in genes.keys():
			for name in genes[k]:

				handle = Entrez.esearch(db='nucleotide', retmax=1000, term='"'+species+'"[Organism] AND "'+name+'"[Title] NOT (mito* OR "whole genome")')
				record = Entrez.read(handle)
				ids = record['IdList']
				out = open('Nuclear_Fastas/'+k+'.fasta', 'a')
				for i in ids:
					handle = Entrez.efetch(db="nucleotide", id=i, rettype = "gb", retmode= "text")
					record = SeqIO.parse(handle, "genbank")
					try:
						r = next(record)					
						paren = r.annotations['source'].find('(')
						gb_species_name = r.annotations['source']
						if paren != -1:
							gb_species_name[:paren]
						if species == gb_species_name.rstrip():
							out.write('>'+species+' '+r.annotations['accessions'][0]+'\n'+str(r.seq)+'\n')
					except ValueError:
						pass
				out.close()
		for name in other_genes:

			handle = Entrez.esearch(db='nucleotide', retmax=50, term='"'+species+'"[Organism] AND "'+name+'"[Title] NOT (mito* OR "whole genome")')
			record = Entrez.read(handle)
			ids = record['IdList']
			out = open('Nuclear_Fastas/'+name+'.fasta', 'a')
			for i in ids:
				handle = Entrez.efetch(db="nucleotide", id=i, rettype = "gb", retmode= "text")
				record = SeqIO.parse(handle, "genbank")
				try:
					r = next(record)
					paren = r.annotations['source'].find('(')
					gb_species_name = r.annotations['source']
					if paren != -1:
						gb_species_name[:paren]
					if species == gb_species_name.rstrip():
						out.write('>'+species+' '+r.annotations['accessions'][0]+'\n'+str(r.seq)+'\n')
				except ValueError:
					pass
			out.close()

	conn.commit()
	conn.close()

nuclear_genes('')