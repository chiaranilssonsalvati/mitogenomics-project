import sqlite3 as sq 

def make_mito_fasta():
	conn = sq.connect('squamata.db')
	c = conn.cursor()
	out = open('master_fasta.fasta', 'w')
	for x in c.execute('SELECT Sequence_Info.acc_num, Sequence_Info.rotated_genome, Sequence_Info.species_name, Species_Info.taxonomy_cut FROM Sequence_Info JOIN Species_Info ON Sequence_Info.species_name = Species_Info.species_name WHERE Sequence_Info.seq_type = "m";'):
		acc_num = x[0]
		rotated = x[1]
		genus_species = x[2]
		tax = x[3]
		g_s = genus_species.replace(' ','_')

		for t in tax.split(','):
			if "idae'" in t:
				family = t[2:-1]
		 		break
		out.write('>'+family+'_'+g_s+'$'+acc_num+'\n'+rotated+'\n')
	conn.commit()
	conn.close()
	out.close()
	# -idae
	# taxonomy, species_name, acc_num, rotated genome