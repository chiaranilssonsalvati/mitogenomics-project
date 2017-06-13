import create_metadata_csv
import createbadan
import getridofbadan
import create_sequenceinfo
import populate_dec
import features_csv
import create_mitogeneloc
import create_speciesinfo
import populate_dec_pt2
import populate_rotated
import add_nuclear_genes
import make_mito_fasta

email = ''

create_metadata_csv.create_metadata_csv(email)
createbadan.createbadan(email)
getridofbadan.getridofbadan()
create_sequenceinfo.create_sequenceinfo()
features_csv.features_csv(email)
populate_dec.populate_dec()
create_mitogeneloc.create_mitogeneloc()
create_speciesinfo.create_speciesinfo()
populate_dec_pt2.populate_dec()
populate_rotated.populate_rotated()
add_nuclear_genes.add_nuclear_genes(email)
make_mito_fasta.make_mito_fasta()