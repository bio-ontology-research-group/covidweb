import covidweb.virtuoso as virt
import logging

from uploader.utils import to_prefixed_uri, get_ontology
from uploader.aberowl import find_by_iri

logger = logging.getLogger(__name__)

class Submissions:
    MIME_TYPE_JSON = "application/json"

    def find(self, limit=10, offset=None):
        offsetstr = " OFFSET " + str(offset) if offset else ''
        query = 'PREFIX MainSchema: <http://biohackathon.org/bh20-seq-schema#MainSchema/> \n \
        PREFIX sio: <http://semanticscience.org/resource/> \n \
        PREFIX efo: <http://www.ebi.ac.uk/efo/> \n \
        PREFIX obo: <http://purl.obolibrary.org/obo/> \n \
        PREFIX evs: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> \n \
        PREFIX edam: <http://edamontology.org/> \n \
        \n \
        select * \n \
        where { \n \
        \n \
        { \n \
            select distinct ?sub ?host_species ?sample_id  ?collection_date  \n \
                (group_concat(distinct ?seq_technology;separator="|") as ?seq_technologies)  \n \
                ?virus_species \n \
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
            ?submitter obo:NCIT_C42781 ?author .  \n \
            } LIMIT ' + str(limit) + offsetstr + ' \n \
        } UNION { \n \
            select (count(distinct ?sub) as ?total)  \n \
            FROM <https://workbench.cborg.cbrc.kaust.edu.sa> \n \
            where { \n \
                ?sub MainSchema:host  ?host . \n \
        \n  }\n} \n}'
        logger.debug("Executing query for search criteria")
        result = virt.execute_sparql(query, self.MIME_TYPE_JSON).json()
        submissions = self.pipe_sep_to_string_list(result['results']['bindings'][:-1])
        submissions = self.transform_references(submissions)
        submissions.append(result['results']['bindings'][-1])
        return submissions

    def get_by_iri(self, iri):
        query = 'PREFIX MainSchema: <http://biohackathon.org/bh20-seq-schema#MainSchema/> \n \
        PREFIX sio: <http://semanticscience.org/resource/> \n \
        PREFIX efo: <http://www.ebi.ac.uk/efo/> \n \
        PREFIX obo: <http://purl.obolibrary.org/obo/> \n \
        PREFIX evs: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> \n \
        PREFIX edam: <http://edamontology.org/> \n \
        \n \
        select distinct (<' + iri + '> as ?sub)  \n \
        ?host_id ?host_species ?host_sex ?host_age ?host_age_unit ?host_health_status ?host_treatment (group_concat(distinct ?host_vaccination;separator="|") as ?host_vaccinations) ?ethnicity \n \
        ?sample_id (group_concat(distinct ?specimen_source;separator="|") as ?specimen_sources) ?sample_storage_conditions (group_concat(distinct ?source_database_accession;separator="|") as ?source_database_accessions)  \n \
        ?collector_name ?collection_date ?collecting_institution ?collection_location  \n \
        (group_concat(distinct ?seq_technology;separator="|") as ?seq_technologies) ?sequence_assembly_method (group_concat(distinct ?sequencing_coverage;separator="|") as ?sequencing_coverages)  \n \
        ?virus_species  ?virus_strain \n \
        from <https://workbench.cborg.cbrc.kaust.edu.sa>  \n \
        \n \
        where { \n \
        \n \
        <' + iri + '> MainSchema:host  ?host ; \n \
            MainSchema:sample ?sample ; \n \
            MainSchema:submitter ?submitter ; \n \
            MainSchema:technology ?technology ; \n \
            MainSchema:virus ?virus . \n \
        \n \
        ?host efo:EFO_0000532 ?host_species . \n \
        OPTIONAL { ?host sio:SIO_000115 ?host_id .} \n \
        OPTIONAL { ?host obo:PATO_0000047 ?host_sex .} \n \
        OPTIONAL { ?host obo:PATO_0000011 ?host_age .} \n \
        OPTIONAL { ?host obo:NCIT_C42574 ?host_age_unit .} \n \
        OPTIONAL { ?host obo:NCIT_C25688 ?host_health_status .} \n \
        OPTIONAL { ?host efo:EFO_0000727 ?host_treatment .} \n \
        OPTIONAL { ?host efo:VO_0000002 ?host_vaccination .} \n \
        OPTIONAL { ?host sio:SIO_001014 ?ethnicity .} \n \
        \n \
        ?sample sio:SIO_000115 ?sample_id; \n \
            evs:C25164 ?collection_date . \n \
        OPTIONAL { ?sample obo:OBI_0001479 ?specimen_source .} \n \
        OPTIONAL { ?sample obo:OBI_0001472 ?sample_storage_conditions .} \n \
        OPTIONAL { ?sample edam:data_2091 ?source_database_accession .} \n \
        OPTIONAL { ?sample obo:OBI_0001895 ?collector_name .} \n \
        OPTIONAL { ?sample obo:NCIT_C41206 ?collecting_institution .} \n \
        OPTIONAL { ?sample obo:GAZ_00000448 ?collection_location .} \n \
        \n \
        ?virus edam:data_1875 ?virus_species . \n \
        OPTIONAL { ?virus sio:SIO_010055 ?virus_strain .}  \n \
        \n \
        ?technology obo:OBI_0600047 ?seq_technology . \n \
        OPTIONAL { ?technology efo:EFO_0002699 ?sequence_assembly_method .} \n \
        OPTIONAL { ?technology obo:FLU_0000848 ?sequencing_coverage .} \n \
        }'
        logger.debug("Executing query for submission: %s", iri)
        result = virt.execute_sparql(query, self.MIME_TYPE_JSON).json()
        submissions = result['results']['bindings']
        # appending submitter fields
        if len(submissions) > 0:
            submitter = self.get_submitter(iri)
            if not submitter:
                submissions = self.pipe_sep_to_string_list(submissions)
                submissions = self.transform_references(submissions)
                return submissions[0]

            for key in submitter:
                submissions[0][key] = submitter[key]
            
            submissions = self.pipe_sep_to_string_list(submissions)
            submissions = self.transform_references(submissions)
            return submissions[0]
        else:
            return None

    def get_submitter(self, submission_iri):
        query='PREFIX MainSchema: <http://biohackathon.org/bh20-seq-schema#MainSchema/> \n \
        PREFIX sio: <http://semanticscience.org/resource/> \n \
        PREFIX efo: <http://www.ebi.ac.uk/efo/> \n \
        PREFIX obo: <http://purl.obolibrary.org/obo/> \n \
        PREFIX evs: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> \n \
        PREFIX edam: <http://edamontology.org/> \n \
         \n \
        select (<' + submission_iri + '> as ?sub) \n \
            (group_concat(distinct ?author;separator="|") as ?authors) (group_concat(distinct ?submitter_name;separator="|") as ?submitter_names) ?submitter_address ?originating_lab ?lab_address ?provider_sample_id ?submitter_sample_id ?publication (group_concat(distinct ?submitter_orcid;separator="|") as ?submitter_orcids) \n \
        from <https://workbench.cborg.cbrc.kaust.edu.sa>  \n \
         \n \
        where { \n \
        <' + submission_iri + '> MainSchema:submitter ?submitter . \n \
        ?submitter obo:NCIT_C42781 ?author . \n \
         \n \
        OPTIONAL { ?submitter sio:SIO_000116 ?submitter_name .} \n \
        OPTIONAL { ?submitter sio:SIO_000172 ?submitter_address .} \n \
        OPTIONAL { ?submitter obo:NCIT_C37984 ?originating_lab .} \n \
        OPTIONAL { ?submitter obo:OBI_0600047 ?lab_address .} \n \
        OPTIONAL { ?submitter efo:EFO_0001741 ?provider_sample_id .} \n \
        OPTIONAL { ?submitter obo:NCIT_C19026 ?submitter_sample_id .} \n \
        OPTIONAL { ?submitter obo:NCIT_C19026 ?publication .} \n \
        OPTIONAL { ?submitter sio:SIO_000115 ?submitter_orcid .} \n \
         \n \
        }'    
        logger.debug("Executing query for submission: %s", submission_iri)
        result = virt.execute_sparql(query, self.MIME_TYPE_JSON).json()
        return result['results']['bindings'][0] if len(result['results']['bindings']) > 0 else None

    def transform_references(self, submissions):
        for obj in submissions:
            for key in obj:
                obj[key]['prefixed_value'] = to_prefixed_uri(obj[key]['value'])
        return submissions

    def resolve_references(self, submissions):
        iri_dict = []
        group_uri_keys = ['seq_technologies', 'specimen_sources']
        for obj in submissions:
            for key in obj:
                if obj[key]['type'] == 'uri' or key in group_uri_keys:
                    iri_dict = iri_dict + get_ontology(obj[key]['value'])

        resolved_objs = find_by_iri(iri_dict)
        for obj in submissions:
            for key in obj:
                if obj[key]['type'] == 'uri' and isinstance(obj[key]['value'], str) and obj[key]['value'] in resolved_objs:
                   obj[key]['display'] = resolved_objs[obj[key]['value']]['label']
                
                if key in group_uri_keys and isinstance(obj[key]['value'], list):
                    val_list = []
                    val = obj[key]['value']   
                    for i in range(len(val)):
                        if val[i] in resolved_objs:
                            val_list.append(resolved_objs[val[i]]['label'])
                        else:
                            val_list.append(val[i])
                        
                    obj[key]['display'] = val_list
        
        return submissions

    def pipe_sep_to_string_list(self, submissions):
        for obj in submissions:
            obj['seq_technologies']['value'] = obj['seq_technologies']['value'].split('|') 
            if 'authors' in obj:
                obj['authors']['value'] = obj['authors']['value'].split('|')

            if 'submitter_names' in obj:
                obj['submitter_names']['value'] = obj['submitter_names']['value'].split('|')
            
            if 'submitter_orcids' in obj:
                obj['submitter_orcids']['value'] = obj['submitter_orcids']['value'].split('|')
            
            if 'host_vaccinations' in obj:
                obj['host_vaccinations']['value'] = obj['host_vaccinations']['value'].split('|')
            
            if 'specimen_sources' in obj:
                obj['specimen_sources']['value'] = obj['specimen_sources']['value'].split('|')
            
            if 'source_database_accessions' in obj:
                obj['source_database_accessions']['value'] = obj['source_database_accessions']['value'].split('|')
            
            if 'sequencing_coverages' in obj:
                obj['sequencing_coverages']['value'] = obj['sequencing_coverages']['value'].split('|')
        return submissions
