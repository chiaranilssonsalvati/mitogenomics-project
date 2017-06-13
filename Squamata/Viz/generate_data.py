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
