namelist = ["18S.fasta", "28S.fasta", "ACM4.fasta", "ADNP.fasta", "AHR.fasta", "alpha-enolase.fasta", "AMEL.fasta", "BDNF.fasta", "BMP2.fasta", "CAND1.fasta", "CMOS.fasta", "DLL.fasta", "DNAH3.fasta", "ECEL.fasta", "ENC1.fasta", "FSHR.fasta", "FSTL5.fasta", "GAPD.fasta", "GPR37.fasta", "HOXA13.fasta", "KIF24.fasta", "LRRN1.fasta", "MC1R.fasta", "MKL1.fasta", "NGFB.fasta", "NT3.fasta", "PDC.fasta", "PLA2.fasta", "PNN.fasta", "PRLR.fasta", "PTGER4.fasta", "PTPN.fasta", "R35.fasta", "RAG1.fasta", "RAG2.fasta", "rhodopsin.fasta", "SCN4a.fasta", "SINCAIP.fasta", "SLC8A1.fasta", "SLC30A1.fasta", "TRAF6.fasta", "VCPIP1.fasta", "ZEB2.fasta", "ZFP36L1.fasta"]

for file in namelist:
	print file
	#reading in a file with multiple species and sequences for one gene
	infile = open('Nuclear_Fastas/'+file, "r")
	# checks a given sequence for IUPAC codes and returns a count of how many there are in the sequence
	# R Y S W K M B D H V N . -
	def IUPACcount(inputString):
		count = 0
		for char in inputString:
			if char == 'R' or char == 'Y' or char == 'S' or char == 'W' or char == 'K' or char == 'M' or char == 'B' or char == 'D' or char == 'H' or char == 'V' or char == 'N' or char == '.' or char == '-':
				count += 1
		return count


	#initialize empty variables: a dictionary, the sequence, the taxon name, and the accession number
	taxa_dic = {}
	seq = ""
	taxon = ""
	accession = ""

	#loop through entire fasta file line by line
	for line in infile:
		# if the line starts with the > (meaning it has the name and accesion info), 
		# split the line into a list of 'words' based on the spaces in the string
		# 'Ctenotus olympicus GQ241619.1' -----> ['Ctenotus','olympicus','GQ241619.1'] 
		if line[0] == ">":
			words = line.split()

			# if the taxon in question is already in the dictionary, we add the sequence and the accesion number
			# the the already established lists
			if taxon in taxa_dic:
				list_of_lists = taxa_dic[taxon]
				# list_of_lists = [[seq1, seq2, seq3],[acc1,acc2,acc3][len1, len2, len3]]
				list_of_lists[0].append(seq) #add seq4
				list_of_lists[1].append(accession) #add acc4
				list_of_lists[2].append(len(seq))
				# list_of_lists = [[seq1,seq2,seq3,seq4],[acc1, acc2, acc3, acc4][len1, len2, len3, len4]]
				# update the dictionary with the new information
				taxa_dic[taxon] = list_of_lists

			# else, make a new entry in the dictionary for the taxon
			# make a new list of lists with the sequence and accession number and sequence length
			else:
				taxa_dic[taxon] = [[seq],[accession],[len(seq)]]

			#clears sequence variable 
			seq = ""

			# grabs the taxon name and accession number from the string
			# assuming the accession number is the last element of the header and the 
			# taxon name is everything preceding it
			last = (len(words) - 1)
			accession = words[last]
			taxon_list = words[:-1]
			taxon = ' '.join(taxon_list)


		# if the line DOESN'T start with >, add that line to the sequence
		else:
			seq += line[:-1]

	# gets the last entry in the file and adds to the dictionary
	# this is necessary because of how the for loop is structured 
	# (code copied from above)
	if taxon in taxa_dic:
		list_of_lists = taxa_dic[taxon]
		list_of_lists[0].append(seq)
		list_of_lists[1].append(accession)
		list_of_lists[2].append(len(seq))
		taxa_dic[taxon] = list_of_lists
	else:
		taxa_dic[taxon] = [[seq],[accession],[len(seq)]]


	# updates the sequence length list in the dictionary for each taxon key 
	# subtracts the number of IUPAC occurances from the total sequence length
	# uses that metric to determind best sequence (sequence length - IUPAC)
	for item in taxa_dic:
		for index in range(len(taxa_dic[item][2])): 
			seq_length = taxa_dic[item][2][index]
			seq_length_without_IUPAC = seq_length - IUPACcount(taxa_dic[item][0][index])
			taxa_dic[item][2][index] = seq_length_without_IUPAC



	# remove the first element of the dictionary "", which is empty
	taxa_dic.pop("")

	out = "out" + file
	# writing to a new file, the best sequence and it's taxon name and accession number
	# new file is called "best_sequences.fasta"
	with open('squamata_out/'+out, "w") as f:

		# loops through every taxon in the dictionary and finds the max (updated)sequence length, 
		# also finds the index of that length, and uses that index to return the best sequence
		# and the accession number of that sequence
		for item in taxa_dic:
			best_length = max(taxa_dic[item][2])
			best_index = taxa_dic[item][2].index(best_length)
			best_seq = taxa_dic[item][0][best_index]
			best_acc = taxa_dic[item][1][best_index]

			# writes this information to file
			f.write(item + " " + best_acc + "\n" + best_seq + "\n")

	# closes file
	f.close() 