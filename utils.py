import json
#import requests
from lodcloud_search_api import search_api 

#url = "https://lod-cloud.net/lod-data.json"
#response = requests.get(url)
#response.raise_for_status()
with open("./LODCLOUD_Metadata/lod-data.json", "r", encoding="utf-8") as f:
    datasets = json.load(f)

# Print dataset name and its domain
#for dataset_id, info in datasets.items():
    #identifier = info.get("identifier", dataset_id)
    #domain = info.get("domain", "N/A")
    #print(f"{identifier} → domain: {domain}")

#print(datasets["arthroscopy"].get("identifier"))


def add_availability(row, domain):
    
    availability_edges = {}

    #Accessibility SPARQL metric
    accessibility_value = row[2]

    if(accessibility_value == "-"):
        accessibility_value = -1

    elif(accessibility_value == "offline"):
        accessibility_value = 0

    else:
        accessibility_value = 1

    #Accessibility SPARQL edge
    availability_edges[row[0] + "_accessibility_SPARQL"] = [row[0], "SPARQL_ENDPOINT_accessibility_value = " + str(accessibility_value), domain]


    #Accessibility RDF dump (metadata) metric
    #Estraggo solo fino alla prima cifra decimale
    accessibility_value = None

    try:
        accessibility_value = round(float(row[4]), 1)
    except (ValueError, TypeError):
        pass

    #Accessibility RDF dump edge
    availability_edges[row[0] + "_accessibility_SPARQL"] = [row[0], "RDF_dump_accessibility_value = " + str(accessibility_value), domain]

    #Dereferenceability of the URI metric
    #Estraggo solo fino alla prima cifra decimale
    deferenceability_value = None

    try:
        deferenceability_value = round(float(row[152]), 1)
    except (ValueError, TypeError):
        pass

    #Dereferenceability of the URI edge
    availability_edges[row[0] + "_Dereferenceability"] = [row[0], "URIs_dereferenceability_value = " + str(deferenceability_value), domain]

    #print(availability_edges)

    return availability_edges


def add_licensing(row, domain):

    licensing_edges = {}

    #Machine readable license (metadata) metric
    machine_readable_license_value = row[42]

    if(machine_readable_license_value =="FALSE"):
        machine_readable_license_value = 0
    else:
        machine_readable_license_value = 1

    licensing_edges[row[0] + "_Machine_Readable_License_Metadata"] = [row[0], "machine_readable_license_metadata_value = " + str(machine_readable_license_value), domain]

    #Machine readable license (query) metric
    machine_readable_license_value = row[43]

    if(machine_readable_license_value =="FALSE" or machine_readable_license_value == "-"):
        machine_readable_license_value = 0
    else:
        machine_readable_license_value = 1

    licensing_edges[row[0] + "_Machine_Readable_License_Query"] = [row[0], "machine_readable_license_query_value = " + str(machine_readable_license_value), domain]


    human_readable_license_value = row[44]

    if(human_readable_license_value == "FALSE" or human_readable_license_value == "-"):
        human_readable_license_value = 0
    else:
        human_readable_license_value = 1


    licensing_edges[row[0] + "_Human_Readable_License"] = [row[0], "human_readable_license_value = " + str(human_readable_license_value), domain]

    return licensing_edges


def add_interlinking(row, domain):

    interlinking_edges = {}

    degree_connection_value = row[65]

    interlinking_edges[row[0] + "_Degree_Connection"] = [row[0], "degree_connection_value = " + str(degree_connection_value), domain]

    clustering_coefficient_value = None

    try:
        clustering_coefficient_value = round(float(row[66]), 1)
    except (ValueError, TypeError):
        pass

    interlinking_edges[row[0] + "_Clustering_Coefficient"] = [row[0], "clustering_coefficient_value = " + str(clustering_coefficient_value), domain]   

    centrality_value = None

    try:
        centrality_value = round(float(row[67]), 1)
    except (ValueError, TypeError):
        pass

    interlinking_edges[row[0] + "_Centrality"] = [row[0], "centrality_value = " + str(centrality_value), domain]

    sameAsChainsNumber = None
    
    try:
        sameAsChainsNumber = int(row[68])
    except (ValueError, TypeError):
        pass

    numberOfTriples_query = None
    
    try:
        numberOfTriples_query = int(row[60])
    except (ValueError, TypeError):
        pass

    sameAs_chains_value = None

    if(sameAsChainsNumber != None and numberOfTriples_query != None):
        sameAs_chains_value = round(sameAsChainsNumber / numberOfTriples_query, 1)

    interlinking_edges[row[0] + "_SameAs_Chains_Frequency"] = [row[0], "sameAs_chains_frequency_value = " + str(sameAs_chains_value), domain]

    skos_mapping_count = None
    
    try:
        skos_mapping_count= int(row[139])
    except (ValueError, TypeError):
        pass

    skos_mapping_frequency_value = None

    if(skos_mapping_count != None and numberOfTriples_query != None):
        skos_mapping_frequency_value = round(skos_mapping_count / numberOfTriples_query, 1)

    interlinking_edges[row[0] + "_Skos_Mapping_Frequency"] = [row[0], "skos_mapping_frequency_value = " + str(skos_mapping_frequency_value), domain]

    return interlinking_edges


def add_security(row, domain):

    security_edges = {}

    authentication_required_value = row[19]

    if(authentication_required_value == "-" or authentication_required_value == "FALSE"):
        authentication_required_value = 0
    else:
        authentication_required_value = 1

    security_edges[row[0] + "_Authentication_Required"] = [row[0], "authentication_required_value = " + str(authentication_required_value), domain]

    https_used_value = row[18]

    if(https_used_value == "-" or https_used_value =="FALSE"):
        https_used_value = 0
    else:
        https_used_value = 1

    security_edges[row[0] + "_HTTPS_Used"] = [row[0], "https_used_value = " + str(https_used_value), domain]

    return security_edges

def add_performance(row, domain):

    performance_edges = {}

    average_latency = None

    try:
        average_latency = round(float(row[50]), 1)
    except (ValueError, TypeError):
        pass

    low_latency_value = None
    if(average_latency != None):
        if(average_latency < 1):
            low_latency_value = 1
        else:
            low_latency_value = round(average_latency / 1000, 1)

    performance_edges[row[0] + "_Low_Latency"] = [row[0], "low_latency_value = " + str(low_latency_value), domain]

    average_throughput = None

    try:
        average_throughput = round(float(row[57]), 1)
    except (ValueError, TypeError):
        pass

    high_throughput_value = None

    if(average_throughput != None):
        if(average_throughput > 5):
            high_throughput_value = 1
        else:
            high_throughput_value = round(average_throughput / 200, 1)

    
    performance_edges[row[0] + "_High_Throughput"] = [row[0], "high_throughput_value = " + str(high_throughput_value), domain]

    return performance_edges


def add_semantic_accuracy(row, domain):
    semantic_accuracy_edges = {}

    triples_with_empty_annotation = None

    try:
        triples_with_empty_annotation = int(row[102])
    except (ValueError, TypeError):
        pass
    

    semantic_accuracy_edges[row[0] + "_Empty_Annotation"] = [row[0], "empty_annotation_value = " + str(triples_with_empty_annotation), domain]

    triples_with_white_spaces = None

    try:
        triples_with_white_spaces = int(row[103])
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_White_Spaces"] = [row[0], "white_spaces_value = " + str(triples_with_white_spaces), domain]

    triples_with_data_type_problem = None

    try:
        triples_with_data_type_problem = round(float(row[104]), 1)
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_Datatype_Consistency"] = [row[0], "datatype_consistency_value = " + str(triples_with_data_type_problem), domain]

    triples_inconsistent_with_functional_property = None
    
    try:
        triples_inconsistent_with_functional_property = round(float(row[105]), 1)
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_Functional_Property_Violation"] = [row[0], "functional_property_violation_value = " + str(triples_inconsistent_with_functional_property), domain]

    triples_with_invalid_inverse_functional_properties = None
    try:
        triples_with_invalid_inverse_functional_properties = round(float(row[106]), 1)
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_Inverse_Functional_Property_Violation"] = [row[0], "inverse_functional_property_violation_value = " + str(triples_with_invalid_inverse_functional_properties), domain]

    return semantic_accuracy_edges


def add_consistency(row, domain):
    consistency_edges ={}

    entities_with_disjoint_classes = None 

    try:
        entities_with_disjoint_classes = round(float(row[94]), 1)
    except (ValueError, TypeError):
        pass

    consistency_edges[row[0]+ "_Entities_As_Members_With_Disjoint_Classes"] = [row[0], "entities_as_members_with_disjoint_classes_value = " + str(entities_with_disjoint_classes), domain]

    triples_misplaces_classes = None

    try:
        triples_misplaces_classes = round(float(row[96]), 1) 
    except (ValueError, TypeError):
        pass

    consistency_edges[row[0]+ "_Misplaced_Classes"] = [row[0], "misplaced_classes_value = " + str(triples_misplaces_classes), domain]


    triples_misplaces_properties = None

    try:
        triples_misplaces_properties = round(float(row[95]), 1)
    except (ValueError, TypeError):
        pass



    consistency_edges[row[0]+ "_Misplaced_Properties"] = [row[0], "misplaced_properties_value = " + str(triples_misplaces_properties), domain]

    #Deprecated class/properties usage
    #deprecated_usage = None
    #try:
    #    deprecated_usage = int(row[93])
    #except (ValueError, TypeError):
    #    pass

    #for the moment, I'll skip this metric since there does not seem to be a "number of classes" column for these data

    triples_with_undefined_classes = None
    
    try:
        triples_with_undefined_classes = round(float(row[98]), 1)
    except (ValueError, TypeError):
        pass


    consistency_edges[row[0]+ "_Undefined_Classes"] = [row[0], "undefined_classes_value = " + str(triples_with_undefined_classes), domain]


    triples_with_undefined_properties = None
    
    try:
        triples_with_undefined_properties = round(float(row[99]), 1)
    except (ValueError, TypeError):
        pass

    consistency_edges[row[0]+ "_Undefined_Properties"] = [row[0], "undefined_properties_value = " + str(triples_with_undefined_properties), domain]

    ontology_hijacking_value = row[97]

    if(ontology_hijacking_value == "-" or ontology_hijacking_value =="FALSE"):
        ontology_hijacking_value = 0
    else:
        ontology_hijacking_value = 1

    consistency_edges[row[0]+ "_Ontology_Hijacking"] = [row[0], "ontology_hijacking_value = " + str(ontology_hijacking_value), domain]

    return consistency_edges


def add_conciseness(row, domain):
    conciseness_edges = {}

    triples_with_intensional_conciseness = None
    
    try:
        triples_with_intensional_conciseness = round(float(row[101]), 1)
    except (ValueError, TypeError):
        pass

    conciseness_edges[row[0] + "_Intensional_Conciseness"] = [row[0], "intensional_conciseness_value = " + str(triples_with_intensional_conciseness), domain]

    triples_with_extensional_conciseness = None
    
    try:
        triples_with_extensional_conciseness = round(float(row[100]), 1)
    except (ValueError, TypeError):
        pass

    conciseness_edges[row[0] + "_Extensional_Conciseness"] = [row[0], "extensional_conciseness_value = " + str(triples_with_extensional_conciseness), domain]

    return conciseness_edges


def add_reputation(row, domain):
    reputation_edges = {}

    pageRank = None
    
    try:
        pageRank = round(float(row[70]))
    except (ValueError, TypeError):
        pass

    reputation_edges[row[0] + "_Reputation(Pagerank)"] = [row[0], "pagerank_value = " + str(pageRank), domain]

    return reputation_edges


def add_believability(row, domain):

    believability_edges = {}

    believability_value = None
    try:
        believability_value = round(float(row[128]), 1)
    except (ValueError, TypeError):
        pass

    believability_edges[row[0] + "_Believability"] = [row[0], "believability_value = " + str(believability_value), domain]

    return believability_edges


def add_verifiability(row, domain):
    verifiability_edges = {}

    #In our data, there doesn't seem to be a column associated with dataset authenticity, so, I'll skip this metric

    authors_value = row[77]

    if(authors_value == "-" or authors_value == "FALSE" or authors_value == "[]"):
        authors_value = 0
    else:
        authors_value = 1

    verifiability_edges[row[0] + "_Authors_Specified"] = [row[0], "authors_specified_value = " + str(authors_value), domain]


    contributors_value = row[78]

    if(contributors_value == "-" or contributors_value == "FALSE" or contributors_value == "[]"):
        contributors_value = 0
    else:
        contributors_value = 1

    verifiability_edges[row[0] + "_Contributors_Specified"] = [row[0], "contributors_specified_value = " + str(contributors_value), domain]

    
    publishers_value = row[79]

    if(publishers_value == "-" or publishers_value == "FALSE" or publishers_value == "[]"):
        publishers_value = 0
    else:
        publishers_value = 1

    verifiability_edges[row[0] + "_Publishers_Specified"] = [row[0], "publishers_specified_value = " + str(publishers_value), domain]


    sources_value = row[80]

    if(sources_value == "-" or sources_value == "FALSE" or sources_value == "[]"):
        sources_value = 0
    else:
        sources_value = 1

    verifiability_edges[row[0] + "_Sources_Specified"] = [row[0], "sources_specified_value = " + str(sources_value), domain]


    signed_value = row[81]

    if(signed_value == "-" or signed_value == "FALSE" or signed_value == "[]"):
        signed_value = 0
    else:
        signed_value = 1

    verifiability_edges[row[0] + "_Signed"] = [row[0], "signed_value = " + str(signed_value), domain]


    return verifiability_edges


def add_currency(row, domain):
    currency_edges = {}

    age_of_data = row[8]

    if(age_of_data == "-" or age_of_data == "FALSE" or age_of_data == "[]"):
        age_of_data = 0
    else:
        age_of_data = 1

    currency_edges[row[0], "_Age_Of_Data_Specified"] = [row[0], "age_of_data_specified_value = " + str(age_of_data), domain]


    modification_date_of_statements = row[9]

    if(modification_date_of_statements == "-" or modification_date_of_statements == "FALSE" or modification_date_of_statements == "[]"):
        modification_date_of_statements = 0
    else:
        modification_date_of_statements = 1

    currency_edges[row[0], "_Modification_Date_Of_Statements_Specified"] = [row[0], "modification_date_of_statements_specified_value = " + str(modification_date_of_statements), domain]

    time_elapsed_since_last_modification = row[11]

    if(time_elapsed_since_last_modification == "-" or time_elapsed_since_last_modification == "FALSE" or time_elapsed_since_last_modification == "[]"):
        time_elapsed_since_last_modification = 0
    else:
        time_elapsed_since_last_modification = 1

    currency_edges[row[0], "_Time_Elapsed_Since_Last_Modification_Specified"] = [row[0], "time_elapsed_since_last_modification_specified_value = " + str(time_elapsed_since_last_modification), domain]

    
    history_of_updates = row[12]

    if(history_of_updates == "-" or history_of_updates == "FALSE" or history_of_updates == "[]"):
        history_of_updates = 0
    else:
        history_of_updates = 1

    currency_edges[row[0], "_History_Of_Updates_Specified"] = [row[0], "history_of_updates_specified_value = " + str(history_of_updates), domain]

    return currency_edges


def add_timeliness(row, domain):
    timeliness_edges = {}

    #Considered as validation
    update_frequency = row[64]

    if(update_frequency == "-" or update_frequency == "FALSE"):
        update_frequency = 0
    else:
        update_frequency = 1

    timeliness_edges[row[0] + "_Update_Frequency"] = [row[0], "update_frequency_value = " + str(update_frequency), domain]

    return timeliness_edges


def add_completeness(row, domain):
    completeness_edges = {}

    interlinking_completeness = None

    try:
        interlinking_completeness = round(float(row[84]), 1)
    except (ValueError, TypeError):
        pass

    completeness_edges[row[0] + "_Interlinking_Completeness"] = [row[0], "interlinking_completeness_value = " + str(interlinking_completeness), domain]

    return completeness_edges


def add_amount_of_data(row, domain):
    amount_of_data_edges = {}

    number_of_triples_query = row[60]

    if(number_of_triples_query == "-" or number_of_triples_query == "FALSE"):
        number_of_triples_query = 0
    else:
        number_of_triples_query = 1

    amount_of_data_edges[row[0] + "Number_Of_Triples_Retrievable"] = [row[0], "number_of_triples_retrievable_value = " + str(number_of_triples_query), domain]

    level_of_detail = row[63]

    if(level_of_detail == "-" or level_of_detail == "FALSE"):
        level_of_detail = 0
    else:
        level_of_detail = 1

    amount_of_data_edges[row[0] + "Level_Of_Detail_Specified"] = [row[0], "level_of_detail_specified_value = " + str(level_of_detail), domain]

    number_of_entities = row[61]
    number_of_entities_with_regex = row[62]

    scope_retrievable = None

    if((number_of_entities == "-" or number_of_entities == "FALSE") and (number_of_entities_with_regex == "-" or number_of_entities_with_regex == "FALSE")):
        scope_retrievable = 0
    else:
        scope_retrievable = 1

    amount_of_data_edges[row[0] + "Scope_Retrievable"] = [row[0], "scope_retrievable_value = " + str(scope_retrievable), domain]

    return amount_of_data_edges


def add_representational_conciseness(row, domain):
    representational_conciseness_edges = {}

    #there is no "keeping URIs short" metric identifiable in our data

    return representational_conciseness_edges


def add_interoperability(row, domain):
    interoperability_edges = {}

    new_vocabolaries = row[85]

    reuse_value = None
    if(new_vocabolaries == "-" or new_vocabolaries == "FALSE" or new_vocabolaries == "[]"):
        reuse_value = 1
    else:
        reuse_value = 0

    interoperability_edges[row[0] + "_Reuse_Of_Existing_Vocabularies"] = [row[0], "_reuse_of_existing_vocabularies_value = " + str(reuse_value), domain]

    #Mismatch on the calculation of this metric between web-app main page and web-app specific algorithm page
    #I'll use the one on the main page

    new_terms = row[86]

    reuse_value = None
    if(new_terms == "-" or new_terms == "FALSE" or new_terms == "[]"):
        reuse_value = 1
    else:
        reuse_value = 0

    interoperability_edges[row[0] + "_Reuse_Of_Existing_Terms"] = [row[0], "_reuse_of_existing_terms_value = " + str(reuse_value), domain]

    return interoperability_edges


def add_understandability(row, domain):
    understandability_edges = {}
    
    num_of_labels = None
    
    try:
        num_of_labels = int(row[87])
    except (ValueError, TypeError):
        pass
    
    num_of_triples_query = None
    
    try:
        num_of_triples_query = int(row[60])
    except (ValueError, TypeError):
        pass

    human_readable_labelling_value = None

    if(num_of_labels != None and num_of_triples_query != None):
        human_readable_labelling_value = round(num_of_labels / num_of_triples_query * 100, 1)

    understandability_edges[row[0] + "_Human_Readable_Labelling"] = [row[0], "human_readable_labelling_value = " + str(human_readable_labelling_value), domain]

    presence_of_examples = row[90]

    if(presence_of_examples == "-" or presence_of_examples == "FALSE"):
        presence_of_examples = 0
    else:
        presence_of_examples = 1

    understandability_edges[row[0] + "_Exemplary_SPARQL_Queries"] = [row[0], "exemplary_sparql_queries_value = " + str(presence_of_examples), domain]

    regex_uri_value = row[89]

    if(regex_uri_value == "-" or regex_uri_value == "FALSE" or regex_uri_value == "[]"):
        regex_uri_value = 0
    else:
        regex_uri_value = 1

    understandability_edges[row[0] + "_Regex_Of_The_URIs"] = [row[0], "regex_of_the_uris_value = " + str(regex_uri_value), domain]

    #For the "indication of vocabularies used in the dataset" i have the same problem as the "authenthicity" metric
    #So, I'll not include it in the edges for the moment

    #Retrieving title (name) description and sources

    title = row[1]
    description = row[71]
    sources = row[80]

    indication_of_metadata_value = None

    if((title == "-" or title == "FALSE" or title == "[]") and (description == "-" or description == "FALSE" or description == "[]") and (sources == "-" or sources == "FALSE" or sources == "[]")):
        indication_of_metadata_value = 0
    else:
        indication_of_metadata_value = 1

    understandability_edges[row[0] + "_Indication_Of_Metadata"] = [row[0], "indication_of_metadata_value = " + str(indication_of_metadata_value), domain]

    return understandability_edges


def add_interpretability(row, domain):
    interpretability_edges = {}

    #No presence of "num of triples without "rdf:type" property" kind of column in our data
    #So, I' won't include edges for "no misinterpretation of missing values" metric

    use_of_rdf_structures = row[41]

    if(use_of_rdf_structures == "-" or use_of_rdf_structures == "FALSE"):
        use_of_rdf_structures = 0
    else:
        use_of_rdf_structures = 1

    interpretability_edges[row[0] + "_Atypical_Use_Of_Collection_Containers_And_Reification"] = [row[0], "_atypical_use_of_collection_containers_and_reification_value = " + str(use_of_rdf_structures), domain]

    return interpretability_edges


def add_versatility(row, domain):
    versatility_edges = {}

    languages = row[13]

    if(languages == "-" or languages == f"{{}}" or languages == "[]" or languages == "FALSE"):
        languages = 0
    else:
        languages = 1

    versatility_edges[row[0] + "_Specification_Of_Used_Languages"] = [row[0], "specification_of_used_languages_value = " + str(languages), domain]


    serialization_formats = row[15]

    if(serialization_formats == "-" or serialization_formats == "[]" or serialization_formats == "FALSE"):
        serialization_formats = 0
    else:
        serialization_formats = 1

    versatility_edges[row[0] + "_Serialization_Formats_Specified"] = [row[0], "serialization_formats_specified_value = " + str(serialization_formats), domain]


    availability_of_sparql_endpoint = row[2]
    availability_of_rdf_dump = row[4]

    accessing_of_data_in_different_ways = None

    if(availability_of_sparql_endpoint == "Available" and availability_of_rdf_dump == "1"):
        accessing_of_data_in_different_ways = 1
    else:
        accessing_of_data_in_different_ways = 0
    
    versatility_edges[row[0] + "_Accessing_Of_Data_In_Different_Ways"] = [row[0], "accessing_of_data_in_different_ways_value = " + str(accessing_of_data_in_different_ways), domain]

    return versatility_edges


def add_KG_data(row):

    edges = {}

    #will return a dictionary of unique edges
    domain = None
    try:
        domain = datasets[row[0]].get("domain")
    except:
        return edges

    #Availability Scores
    edges.update(add_availability(row, domain))
    
    #Licensing Scores
    edges.update(add_licensing(row, domain))

    #Interlinking Scores
    edges.update(add_interlinking(row, domain))

    #Security Scores
    edges.update(add_security(row, domain))

    #Performance Scores
    edges.update(add_performance(row, domain))

    #Semantic Accuracy Scores
    edges.update(add_semantic_accuracy(row, domain))

    #Consistency Scores
    edges.update(add_consistency(row, domain))

    #Conciseness Scores
    edges.update(add_conciseness(row, domain))

    #Reputation Scores
    edges.update(add_reputation(row, domain))

    #Believability Scores
    edges.update(add_believability(row, domain))

    #Verifiability Scores
    edges.update(add_verifiability(row, domain))

    #Currency Scores
    edges.update(add_currency(row, domain))

    #Timeliness Scores
    edges.update(add_timeliness(row, domain))

    #Completeness Scores
    edges.update(add_completeness(row, domain))
    
    #Amount of data Scores
    edges.update(add_amount_of_data(row, domain))

    #Representational Conciseness Scores
    edges.update(add_representational_conciseness(row, domain))

    #Interoperability Scores
    edges.update(add_interoperability(row, domain))

    #Understandability Scores
    edges.update(add_understandability(row, domain))

    #Interpretability Scores
    edges.update(add_interpretability(row, domain))

    #Versatility Scores
    edges.update(add_versatility(row, domain))
    
    return edges
    #TO BE CONTINUED
