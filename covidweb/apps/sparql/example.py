LIST_SUBMISSION_EXAMPLE = 'PREFIX MainSchema: <http://biohackathon.org/bh20-seq-schema#MainSchema/> \n \
PREFIX sio: <http://semanticscience.org/resource/> \n \
PREFIX efo: <http://www.ebi.ac.uk/efo/> \n \
PREFIX obo: <http://purl.obolibrary.org/obo/> \n \
PREFIX evs: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> \n \
PREFIX edam: <http://edamontology.org/> \n \
 \n \
select distinct ?sub ?host_species ?sample_id ?collection_date ?submitter ?seq_technology ?virus_species \n \
from <https://workbench.cborg.cbrc.kaust.edu.sa>  \n \
 \n \
where { \n \
 \n \
  ?sub MainSchema:host  ?host ; \n \
       MainSchema:sample ?sample ; \n \
       MainSchema:submitter ?submitter ; \n \
       MainSchema:technology ?technology ; \n \
       MainSchema:virus ?virus . \n \
 \n \
  ?host efo:EFO_0000532 ?host_species . \n \
 \n \
  ?sample sio:SIO_000115 ?sample_id; \n \
	  evs:C25164 ?collection_date . \n \
 \n \
  ?virus edam:data_1875 ?virus_species . \n \
  ?technology obo:OBI_0600047 ?seq_technology . \n \
 \n \
} ORDER BY 1 LIMIT 10'