import pymysql.cursors 
import csv

# Establish a connection with MySQL database
connection = pymysql.connect(host='localhost',
      user = 'root', password = '12345', db = 'isoforms',
      cursorclass = pymysql.cursors.DictCursor)

cursor = connection.cursor()

def readGenes(file):  ## Read the tab-separated gene files and insert into database
    with open(file) as gene:
        for line in csv.reader(gene, delimiter='\t'):  # Read the first line and obtain labels
            labels = line
            break
        list = []
        for line in csv.reader(gene, delimiter='\t'):   # Continue reading the file, this time, the data
            g = dict(zip(labels, line))                 # Labels as keys, data entries as values
            list.append(g)                              # Add the dicts into a list, in case there are more than one
    
    gene = list[0]
    tax_id = gene['tax_id']
    org_name = gene['Org_name']
    gene_id = gene['GeneID']
    name = gene['Symbol']
    query = "INSERT INTO organism(tax_id, name) VALUES(%s, %s);"       # INSERT into organism
    cursor.execute(query, (tax_id, org_name))
    query = "INSERT INTO gene(id, name, organism) VALUES(%s, %s, %s);" # INSERT into gene
    cursor.execute(query, (gene_id, name, tax_id))
    connection.commit()
    
    if (any(label=='map_location' for label in labels)):
        mapped = True
        query = "INSERT into locus(gene, chromosome, map_location, start, end, exon_count) VALUES(%s, %s, %s, %s, %s, %s);"
    else:
        query = "INSERT into locus(gene, chromosome, start, end, exon_count) VALUES(%s, %s, %s, %s, %s);" # No known map location
    
    for elem in list:     # Every dictionary in the list, if only one present, this loop will run once
        chromosome = elem['chromosome']
        start = elem['start_position_on_the_genomic_accession']
        end = elem['end_position_on_the_genomic_accession']
        exon_count = elem['exon_count']
        if(mapped):
            map_location = elem['map_location']
            cursor.execute(query, (gene_id, chromosome, map_location, start, end, exon_count))
            connection.commit()
        else:
            cursor.execute(query, (gene_id, chromosome, start, end, exon_count))
            connection.commit()


def readProteins(file):      ## Read the tab-separated protein files and insert into database
    with open(file) as protein:
        for line in csv.reader(protein, delimiter='\t'):
            labels = line
            break
        for line in csv.reader(protein, delimiter='\t'):
            prot = dict(zip(labels, line))
    
    prot_id = prot['Entry']
    prot_names = prot['Protein names'] if(len(prot['Protein names'])<100) else prot['Protein names'][0:100]
    status = 1 if(prot['Status']=='reviewed') else 0
    length = prot['Length']
    query = "INSERT INTO protein(id, name, reviewed, length) VALUES(%s, %s, %s, %s);"  # insert into protein table
    cursor.execute(query, (prot_id, prot_names, status, length))

    gene_name = prot['Gene names'].split()[0]
    query = 'SELECT id FROM gene WHERE name=%s'
    cursor.execute(query, gene_name)
    gene_id = cursor.fetchone()['id']
    query = 'INSERT INTO gene_protein(gene_id, protein_id) VALUES(%s, %s)'
    cursor.execute(query, (gene_id, prot_id)) 
    connection.commit()

    

def readFasta(file):
    
    fasta = open(file, 'r')
    fasta_lines = fasta.readlines()
    i = 0
    for line in fasta_lines:
        if line[0]=='>':                     # Id string in fasta
            if(i!=0):
                query = "INSERT INTO isoform(protein_id, isoform_num, length, sequence) VALUES(%s, %s, %s, %s)"
                cursor.execute(query, (prot_id, isoform, len(seq), seq))
            identifiers = line.split('|')    # Split by |
            prot = identifiers[1].split('-') # Obtain the protein identifier and the number of isoform, split in two
            prot_id = prot[0]                # The proper protein indentifier
            isoform = prot[1] if (len(prot)>1) else 1  # The isoform number
            seq = ''
            i+=1
        else:                                # Sequence line in fasta
            seq += line.strip('\n')
    cursor.execute(query, (prot_id, isoform, len(seq), seq))
    connection.commit()


readGenes('SK6L_drosophila melanogaster.txt')
readProteins('uniprot-Q9VWQ2+(S6KL_DROME).tab')
readFasta('Q9VWQ2 (S6KL_DROME).fasta')
