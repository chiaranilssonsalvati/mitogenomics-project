def nuclear_genes(email):
	import sqlite3 as sq
	import csv
	import time

	# to run this file, make sure it starts running during GenBank off-peak hours!
	time.sleep(14400)

	from Bio import Entrez, SeqIO
	Entrez.email = email

	conn = sq.connect('decapoda.db')
	c = conn.cursor()
	
	# genes that only have one name
	other_genes = ['18S', '28S']

	for x in c.execute('select species_name from Species_Info'):

		species = x[0]
		
		for name in other_genes:
			handle = Entrez.esearch(db='nucleotide', retmax=1000, term='"'+species+'"[Organism] AND "'+name+'"[Title] NOT (mito* OR "whole genome")')
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

nuclear_genes('email')