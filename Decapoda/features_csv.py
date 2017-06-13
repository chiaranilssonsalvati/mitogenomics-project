def clean_gene_name(gn):
	if gn == "cytochrome oxidase subunit 1" or gn == 'cytochrome c oxidase subunit 1' or gn == 'cytochrome c oxidase subunit I' or gn == 'cytochrome oxidase subunit I':
		gn = 'COX1'
	elif gn[:4] == 'tRNA':
		gn = gn[-3:]
	elif gn == 'cytochrome oxidase subunit 2' or gn == 'cytochrome c oxidase subunit 2' or gn == 'cytochrome c oxidase subunit II' or gn == 'cytochrome oxidase subunit II':
		gn = 'COX2'
	elif gn == 'ATP synthase F0 subunit 8' or gn == 'ATPase subunit 8' or gn == 'ATP synthase subunit 8' or gn == 'ATPase8':
		gn = 'ATP8'
	elif gn == 'ATP synthase F0 subunit 6' or gn == 'ATPase subunit 6' or gn == 'ATP synthase subunit 6' or gn == 'ATPase6':
		gn = 'ATP6'
	elif gn == 'NADH dehydrogenase subunit 4L' or gn == 'NADH dehydrogenase subunit 4l':
		gn = 'NADH4L'
	elif 'NADH dehydrogenase subunit' in gn:
		gn = 'NADH'+gn[-1]
	elif gn == 'cytochrome c oxidase subunit 3' or gn == 'cytochrome c oxidase subunit III' or gn == 'cytochrome oxidase subunit III' or gn == 'cytochrome oxidase subunit 3':
		gn = 'COX3'
	elif gn == 'cytochrome b':
		gn = 'CYTB'
	elif gn == "16S ribosomal RNA" or gn == 'large subunit ribosomal RNA' or gn == '16S large subunit ribosomal RNA' or gn == 'l-rRNA':
		gn = '16S'
	elif gn == '12S ribosomal RNA' or gn == 'small subunit ribosomal RNA' or gn == '12S small subunit ribosomal RNA' or gn == 's-rRNA':
		gn = '12S'
	
	return gn

def features_csv(email):
	import csv
	from Bio import Entrez, SeqIO
	Entrez.email = email

	g = open('cleanmetadata.csv', 'r')
	f = open('geneposition.csv', 'w')
	write = csv.writer(f)
	read = csv.reader(g)
	write.writerow(["acc_num", 'gene', 'location'])

	ids = []
	read.next()
	for line in read:
		ids.append(line[0])

	for i in ids:
		handle = Entrez.efetch(db="nucleotide", id=i, rettype = "gb", retmode= "text")
		record = SeqIO.parse(handle, "genbank")
		r = next(record)

		for x in r.features:
			if 'product' in x.qualifiers.keys():
				write.writerow([r.annotations['accessions'][0], clean_gene_name(x.qualifiers['product'][0]), x.location])

			elif 'note' in x.qualifiers.keys():
				if 'control region' in x.qualifiers['note'][0]:
					write.writerow([r.annotations['accessions'][0], 'control region', x.location])
			elif x.type.lower() == 'd-loop':
				write.writerow([r.annotations['accessions'][0], 'control region', x.location])

	f.close()