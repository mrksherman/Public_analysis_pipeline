#!/usr/bin/p/usr/bin/python3
# This program takes a list of gbff files and searches through the genomes on both strands to find motifs based on a
# regular expression and then captures contextual information around the hit.  It collects the gene coordinates, region 
# around the hit (amino acid and nucleotide), stop codon, the proportion of Gs in the downstream 70 basepairs (for rut 
# identification), and sends everything to an output file. 

# To run the script:
# 1. Download a bacterial genome from ncbi in genbank format (full) one by one or in bulk
# 2. Generate a list of the file locations in quotes and separated by commas
# 3. Put the file locations into the filelist variable
# 4. Adjust the regular expression to the anticipated motif
# 5. Execute the script

filelist= [
'D_radiodurans.gb', 'Paenibacillus_sp.gbff', 'E_coli.gbff'
###paste file list here separated by "xxx","xxxx"
###ideally in one line
]

pattern=r"...........[W,Y,F]...........P']"

import Bio, re, os
from Bio import Entrez, SeqIO, GenBank
from Bio.SeqRecord import SeqRecord

import math #Allow for the use of the math library
def motifnextparse(accession): #Define motifnetparse to access the files from ncbi.
    output_file = "motif_hits.csv" #Where it sends the data
    record = '' #record the file names
    startint=0 #start at file no 1.

    with open(accession,"r") as infile:
        record = SeqIO.read(accession, format= "gb") #record the sequence record files in gigabytes
        for i in record.features:#for loop looking at everything in record.features
            if 'organism' in i.qualifiers:
                organism = str((i.qualifiers['organism'])[0])
                print(organism)
                pass          

        with open(output_file,"a") as outfile: #opens the  file
            motifgene=[] #seek out motifs
            strand = 0 #strand of the location starting at 0
            if os.stat(output_file).st_size == 0:
                outfile.write("Accession,Strand,Organism,Hit_gene_start,Hit_gene_end,Gene,Hit_pattern,Translation,Upstream54nt,Psite_codon,Stop_codon,Downstream54nt,Linker_length,G%_in_70_downstream_nt,Linker_sequence,Downstream_gene1_start_pos,Downstream_gene1_end_pos,Downstream_gene1_name,Downstream_gene1_annotation,Downstream_gene2_start_pos,Downstream_gene2_end_pos,Downstream_gene2_name,Downstream_gene2_annotation\n")

#            print("\n")
#            print(str("motifs with XXXXXXXXXXXWXXXDXXXXXXXP @ end"))
#            print("\n")
            #run through in the forward direction to detect forward operons
            spacerbool = 1 #defining new variable spacerbool
            for feature in record.features: #for the feature in record.features
                if motifgene !=[]:#if the motif gene is not there
                    if str("product") in feature.qualifiers: #if the word 'product' is under feature.qualifiers
                        if feature.location.strand == +1: #if it is on the positive strand
                            product = str(feature.qualifiers['product'][0]) #the product is recorded by what follows the prouduct string.
                            if "gene" in feature.qualifiers: #if the gene in feature.qualifiers is present
                                gene= str(feature.qualifiers['gene'][0]) #record the gene that follows gene
                            elif "locus_tag" in feature.qualifiers: #finally, if locus tag is present and gene was not
                                gene = str(feature.qualifiers['locus_tag'][0]) #record the text that follows the locus tag, instead of the gene
                            else:
                                gene = str(["NA"][0]) #if nothing is present, then write 'NA'
                            startds=str(feature.location.start) #the integer of downstream start location
                            endds=str(feature.location.end) #the end integer of the downstream gene
                            startdsint=int(feature.location.start)#rewriting as a start integer
                            while spacerbool:
                                space_seq = record.seq[endint:startdsint] 
                                spacer = startdsint-endint #the size of the spacer region is the start of the (downstream integer- the end integer)
                                Gcount = record.seq[endint:endint+70].count("G")#the Gcount is the number of Guanine base pairs for the first 70 regions of what might be the boxA region.
                                Gperc = round(Gcount*100/70,2) #the Gcount as a percentage.
                                outfile.write(","+str(spacer)+","+str(Gperc)+","+str(space_seq))# write the spacer string and the Gpercentage as in seperate columns of the excel file.
                                spacerbool=0 #start at the beginning.
                            outfile.write(","+ startds +","+ endds +","+ gene+ ","+ product)#Send the information of the start of the downstream, end of downstream, gene, and product, given from code above.
                        else:
                            motifgene=[] #if none of this exists
                            spacerbool=1 
                            pass #mark as pass.
                            outfile.write(str("\n"))#start each line of gene on a new line.
                if feature.type == "CDS" and feature.location.strand == +1: #Looking on the positive strand going forward
                    if str("translation") in feature.qualifiers: #looking at the translation section of the file
                        trans = str(feature.qualifiers['translation'])
                        translation = str(feature.qualifiers['translation'][0])
                        #for motif in re.finditer(r"...........[W,Y,F]...........P']",trans): #in the amino acid sequence, look for a P   
                        for motif in re.finditer(pattern,trans): #in the amino acid sequence, look for a P        
                            mg =motif.group().strip("']") #mg stands for motif group
                            if "gene" in feature.qualifiers: #if the word 'gene' is present
                                gene= str(feature.qualifiers['gene'][0]) #the gene is what is on the line
                                strand = feature.location.strand
                                motifgene=['hit'] #identify the gene as a 'hit'
                            elif "locus_tag" in feature.qualifiers: #if gene isnt present and locus tag is,
                                gene = str(feature.qualifiers['locus_tag'][0]) #make the locus tag the name of the gene
                                motifgene = ['hit']#identify it as a hit
                                strand = feature.location.strand
                            else:
                                gene = str(["NA"][0]) #gene doesn't exist otherwise
                            start=str([int(feature.location.start)][0])#starting integer of the gene
                            end=str([int(feature.location.end)][0])#ending integer of the gene
                            endint=int(feature.location.end) #endint is the last base pair in the strand.
                            stopcod = str(record.seq[feature.location.end-3:feature.location.end])#write what the stop codon is on a seperate line.
                            Psite = str(record.seq[feature.location.end-6:feature.location.end-3])
                            UpstreamAA = str(record.seq[feature.location.end-60:feature.location.end-6])
                            boxA = str(record.seq[feature.location.end:feature.location.end+54])
                            print([strand] + [organism] + [gene] + [start] + [end] + [mg] + feature.qualifiers['translation']+[stopcod]+[Psite]+[UpstreamAA]+[boxA])# print all this information
                            #outfile.write(accession +","+ str(feature.location.strand)+","+ organism +","+ start +","+ end +","+gene+","+mg + ","+ trans +","+ str(feature.qualifiers['translation'][0])+stopcod+Psite+UpstreamAA+boxA)#access all this information in an exported file.
                            outfile.write(accession +","+ str(feature.location.strand)+","+ organism +","+ start +","+ end +","+ gene +","+ mg +","+ translation +","+ UpstreamAA +","+  Psite +","+ stopcod +","+ boxA)#access all this information in an exported file.
            #get the reverse sequence operons
            spacerbool = 1
            for feature in record.features[::-1]: #analyzing the strand going the opposite way
                if motifgene !=[]: #if the motifgene is not present
                    if str('product') in feature.qualifiers: #if the string product is present under feature.qualifiers
                        if feature.location.strand == -1: # and if the location is in the -1 direction
                            product = str(feature.qualifiers['product'][0]) #print the product as the string found in that line
                            if "gene" in feature.qualifiers: #if gene is found, print gene as given
                                gene= str(feature.qualifiers['gene'][0])
                            elif "locus_tag" in feature.qualifiers: #if gene is not found, print the locus tag in place of the gene
                                gene = str(feature.qualifiers['locus_tag'][0])
                            else:
                                gene = str(["NA"][0])#otherwise print 'NA' for the gene column
                            startds=str(feature.location.start)#identifies and names the start of the downstream gene
                            enddsint=int(feature.location.end)#identifies the location of the end of the downstream gene.
                            endds=str(feature.location.end)
                            #print(startds, endds, gene, product)
                            while spacerbool:
                                space_seq = record.seq[enddsint:startint].reverse_complement()
                                spacer = startint-enddsint #quantifies for each genome how long the spacer region is.
                                Gcount = record.seq[startint-70:startint].count("C") #quantifies the amount of Cysteine's in the spacer region***
                                Gperc =round(Gcount*100/70,2) #percentage of Guanines
                                outfile.write(","+str(spacer)+","+str(Gperc)+","+str(space_seq))#writes out the spacer region and the percentage of G's.
                                spacerbool=0
                            outfile.write(","+ startds +","+ endds +","+ gene +","+ product)# write in separate columns the start of the downstream gene, end of it, the name of the gene, and what it makes.
                        else:
                            motifgene=[]
                            spacerbool=1
                            pass
                            outfile.write(str("\n")) #pass it if it spacerbool is one, essentially skipping it until the next round.
                if feature.type == "CDS" and feature.location.strand == -1:
                    if str("translation") in feature.qualifiers:
                        trans = str(feature.qualifiers['translation'])#if the string 'translation' is seen, then name it appropriatly.
                        translation = str(feature.qualifiers['translation'][0])#if the string 'translation' is seen, then name it appropriatly.
                        for motif in re.finditer(pattern,trans): 
                            mg =motif.group().strip("']")
                            if "gene" in feature.qualifiers:
                                gene= str(feature.qualifiers['gene'][0])
                                strand = feature.location.strand
                                motifgene=['hit'] #call it a hit if the gene has a name and meets the qualifications
                            elif "locus_tag" in feature.qualifiers:
                                gene = str(feature.qualifiers['locus_tag'][0])
                                motifgene = ['hit']
                                strand = feature.location.strand #call it a hit if the locus tag is present and meets the qualifications
                            else:#there could be some other name for this
                                gene = str(["NA"][0]) #or call it 'NA' if it cant be found.
                            start=str([int(feature.location.start)][0])#start of sequence
                            end=str([int(feature.location.end)][0])
                            startint=int(feature.location.start)
                            stopcod = str(record.seq[feature.location.start:feature.location.start+3].reverse_complement())
                            Psite = str(record.seq[feature.location.start+3:feature.location.start+6].reverse_complement())
                            UpstreamAA = str(record.seq[feature.location.start+6:feature.location.start+60].reverse_complement())
                            boxA = str(record.seq[feature.location.start-54:feature.location.start].reverse_complement())
                            #print([strand]+organism + gene + [start] + [end] + [mg] + feature.qualifiers['translation']+[stopcod]+[Psite]+[UpstreamAA]+[boxA])
                            outfile.write(accession +"," +str(feature.location.strand) +","+ organism +","+ start +","+ end +","+ gene +","+ mg +","+ translation +","+ UpstreamAA +","+ Psite +","+ stopcod +","+ boxA) #each column will have all of these characteristics for each gene identified.
                            #outfile.write(accession +"," +str(feature.location.strand)+","+ str(organism+start+end+gene+mg+feature.qualifiers['translation']+[stopcod]+[Psite]+[UpstreamAA]+[boxA])) #each column will have all of these characteristics for each gene identified.



for file in filelist:
    motifnextparse(file)
