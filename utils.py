import json
import re 


#import requests
#from lodcloud_search_api import search_api 

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

    availability_edges[row[0] + "_Availability"] = [row[0]]

    #Accessibility SPARQL metric
    accessibility_value = row[2]

    if(accessibility_value == "-"):
        accessibility_value = -1

    elif(accessibility_value == "offline"):
        accessibility_value = 0

    else:
        accessibility_value = 1

    #Accessibility SPARQL edge
    #availability_edges[row[0] + "_accessibility_SPARQL"] = [row[0], "SPARQL_ENDPOINT_accessibility_value = " + str(accessibility_value), domain]
    availability_edges[row[0] + "_Availability"] += ["SPARQL_ENDPOINT_accessibility_value = " + str(accessibility_value)]


    #Accessibility RDF dump (metadata) metric
    #Estraggo solo fino alla prima cifra decimale
    accessibility_value = None

    try:
        accessibility_value = round(float(row[4]), 1)
    except (ValueError, TypeError):
        pass

    #Accessibility RDF dump edge
    #availability_edges[row[0] + "_Accessibility_RDF_Dump"] = [row[0], "RDF_dump_accessibility_value = " + str(accessibility_value), domain]
    availability_edges[row[0] + "_Availability"] += ["RDF_dump_accessibility_value = " + str(accessibility_value)]

    #Dereferenceability of the URI metric
    #Estraggo solo fino alla prima cifra decimale
    deferenceability_value = None

    try:
        deferenceability_value = round(float(row[118]), 1)
    except (ValueError, TypeError):
        pass

    #Dereferenceability of the URI edge
    availability_edges[row[0] + "_Availability"] += ["URIs_dereferenceability_value = " + str(deferenceability_value)]

    #print(availability_edges)

    return availability_edges


def add_licensing(row, domain):

    licensing_edges = {}

    licensing_edges[row[0] + "_Licensing"] = [row[0]]

    #Machine readable license (metadata) metric
    machine_readable_license_value = row[42]

    if(machine_readable_license_value =="FALSE"):
        machine_readable_license_value = 0
    else:
        machine_readable_license_value = 1

    licensing_edges[row[0] + "_Licensing"] += ["machine_readable_license_metadata_value = " + str(machine_readable_license_value)]

    #Machine readable license (query) metric
    machine_readable_license_value = row[43]

    if(machine_readable_license_value =="FALSE" or machine_readable_license_value == "-"):
        machine_readable_license_value = 0
    else:
        machine_readable_license_value = 1

    licensing_edges[row[0] + "_Licensing"] += ["machine_readable_license_query_value = " + str(machine_readable_license_value)]


    human_readable_license_value = row[44]

    if(human_readable_license_value == "FALSE" or human_readable_license_value == "-"):
        human_readable_license_value = 0
    else:
        human_readable_license_value = 1


    licensing_edges[row[0] + "_Licensing"] += ["human_readable_license_value = " + str(human_readable_license_value)]

    return licensing_edges


def add_interlinking(row, domain):

    interlinking_edges = {}

    interlinking_edges[row[0] + "_Interlinking"] = [row[0]]

    degree_connection_value = row[65]

    interlinking_edges[row[0] + "_Interlinking"] += ["degree_connection_value = " + str(degree_connection_value)]

    clustering_coefficient_value = None

    try:
        clustering_coefficient_value = round(float(row[66]), 1)
    except (ValueError, TypeError):
        pass

    interlinking_edges[row[0] + "_Interlinking"] += ["clustering_coefficient_value = " + str(clustering_coefficient_value)]   

    centrality_value = None

    try:
        centrality_value = round(float(row[67]), 1)
    except (ValueError, TypeError):
        pass

    interlinking_edges[row[0] + "_Interlinking"] += ["centrality_value = " + str(centrality_value if centrality_value == None else f"{centrality_value:.4f}")]

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

    interlinking_edges[row[0] + "_Interlinking"] += ["sameAs_chains_frequency_value = " + str(sameAs_chains_value)]

    skos_mapping_count = None
    
    try:
        skos_mapping_count= int(row[139])
    except (ValueError, TypeError, IndexError):
        pass

    skos_mapping_frequency_value = None

    if(skos_mapping_count != None and numberOfTriples_query != None):
        skos_mapping_frequency_value = round(skos_mapping_count / numberOfTriples_query, 1)

    interlinking_edges[row[0] + "_Interlinking"] += ["skos_mapping_frequency_value = " + str(skos_mapping_frequency_value)]

    return interlinking_edges


def add_security(row, domain):

    security_edges = {}

    security_edges[row[0] + "_Security"] = [row[0]] 

    authentication_required_value = row[19]

    if(authentication_required_value == "-" or authentication_required_value == "FALSE"):
        authentication_required_value = 0
    else:
        authentication_required_value = 1

    security_edges[row[0] + "_Security"] += ["authentication_required_value = " + str(authentication_required_value)]

    https_used_value = row[18]

    if(https_used_value == "-" or https_used_value =="FALSE"):
        https_used_value = 0
    else:
        https_used_value = 1

    security_edges[row[0] + "_Security"] += ["https_used_value = " + str(https_used_value)]

    return security_edges

def add_performance(row, domain):

    performance_edges = {}

    performance_edges[row[0] + "_Performance"] = [row[0]]

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

    performance_edges[row[0] + "_Performance"] += ["low_latency_value = " + str(low_latency_value)]

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

    
    performance_edges[row[0] + "_Performance"] += ["high_throughput_value = " + str(high_throughput_value)]

    return performance_edges


def add_semantic_accuracy(row, domain):
    semantic_accuracy_edges = {}

    semantic_accuracy_edges[row[0] + "_Semantic_Accuracy"] = [row[0]]

    triples_with_empty_annotation = None

    try:
        triples_with_empty_annotation = int(row[102])
    except (ValueError, TypeError):
        pass
    

    semantic_accuracy_edges[row[0] + "_Semantic_Accuracy"] += ["empty_annotation_value = " + str(triples_with_empty_annotation)]

    triples_with_white_spaces = None

    try:
        triples_with_white_spaces = int(row[103])
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_Semantic_Accuracy"] += ["white_spaces_value = " + str(triples_with_white_spaces)]

    triples_with_data_type_problem = None

    try:
        triples_with_data_type_problem = round(float(row[104]), 1)
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_Semantic_Accuracy"] += ["datatype_consistency_value = " + str(triples_with_data_type_problem)]

    triples_inconsistent_with_functional_property = None
    
    try:
        triples_inconsistent_with_functional_property = round(float(row[105]), 1)
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_Semantic_Accuracy"] += ["functional_property_violation_value = " + str(triples_inconsistent_with_functional_property)]

    triples_with_invalid_inverse_functional_properties = None
    try:
        triples_with_invalid_inverse_functional_properties = round(float(row[106]), 1)
    except (ValueError, TypeError):
        pass

    semantic_accuracy_edges[row[0] + "_Semantic_Accuracy"] += ["inverse_functional_property_violation_value = " + str(triples_with_invalid_inverse_functional_properties)]

    return semantic_accuracy_edges


def add_consistency(row, domain):
    consistency_edges ={}

    consistency_edges[row[0] + "_Consistency"] = [row[0]]

    entities_with_disjoint_classes = None 

    try:
        entities_with_disjoint_classes = round(float(row[94]), 1)
    except (ValueError, TypeError):
        pass

    consistency_edges[row[0]+ "_Consistency"] += ["entities_as_members_with_disjoint_classes_value = " + str(entities_with_disjoint_classes)]

    triples_misplaces_classes = None

    try:
        triples_misplaces_classes = round(float(row[96]), 1) 
    except (ValueError, TypeError):
        pass

    consistency_edges[row[0]+ "_Consistency"] += ["misplaced_classes_value = " + str(triples_misplaces_classes)]


    triples_misplaces_properties = None

    try:
        triples_misplaces_properties = round(float(row[95]), 1)
    except (ValueError, TypeError):
        pass



    consistency_edges[row[0]+ "_Consistency"] += ["misplaced_properties_value = " + str(triples_misplaces_properties)]

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


    consistency_edges[row[0]+ "_Consistency"] += ["undefined_classes_value = " + str(triples_with_undefined_classes)]


    triples_with_undefined_properties = None
    
    try:
        triples_with_undefined_properties = round(float(row[99]), 1)
    except (ValueError, TypeError):
        pass

    consistency_edges[row[0]+ "_Consistency"] += ["undefined_properties_value = " + str(triples_with_undefined_properties)]

    ontology_hijacking_value = row[97]

    if(ontology_hijacking_value == "-" or ontology_hijacking_value =="FALSE"):
        ontology_hijacking_value = 0
    else:
        ontology_hijacking_value = 1

    consistency_edges[row[0]+ "_Consistency"] += ["ontology_hijacking_value = " + str(ontology_hijacking_value)]

    return consistency_edges


def add_conciseness(row, domain):
    conciseness_edges = {}

    conciseness_edges[row[0] + "_Conciseness"] = [row[0]]

    triples_with_intensional_conciseness = None
    
    try:
        #matches
        match = re.search(r"\d+(?:\.\d+)?", row[101])
        triples_with_intensional_conciseness = round(float(match.group()), 1)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass

    conciseness_edges[row[0] + "_Conciseness"] += ["intensional_conciseness_value = " + str(triples_with_intensional_conciseness)]

    triples_with_extensional_conciseness = None
    
    try:
        match = re.search(r"\d+(?:\.\d+)?", row[100])
        triples_with_extensional_conciseness = round(float(match.group()), 1)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass

    conciseness_edges[row[0] + "_Conciseness"] += ["extensional_conciseness_value = " + str(triples_with_extensional_conciseness)]

    return conciseness_edges


def add_reputation(row, domain):
    reputation_edges = {}

    reputation_edges[row[0] + "_Reputation"] = [row[0]]

    pageRank = None
    try:
        pageRank = round(float(row[70]), 6)
    except (ValueError, TypeError) as e:
        print(e)



    reputation_edges[row[0] + "_Reputation"] += ["pagerank_value = " + str(pageRank if pageRank == None else f"{pageRank:.6f}")]

    return reputation_edges


def add_believability(row, domain):

    believability_edges = {}

    believability_edges[row[0] + "_Believability"] = [row[0]]

    believability_value = None
    try:
        believability_value = round(float(row[128]), 1)
    except (ValueError, TypeError, IndexError):
        pass

    believability_edges[row[0] + "_Believability"] += ["believability_value = " + str(believability_value)]

    return believability_edges


def add_verifiability(row, domain):
    verifiability_edges = {}

    verifiability_edges[row[0] + "_Verifiability"] = [row[0]]

    #In our data, there doesn't seem to be a column associated with dataset authenticity, so, I'll skip this metric

    authors_value = row[77]

    if(authors_value == "-" or authors_value == "FALSE" or authors_value == "[]" or authors_value == "endpoint absent" or authors_value == "endpoint offline"):
        authors_value = 0
    else:
        authors_value = 1

    verifiability_edges[row[0] + "_Verifiability"] += ["authors_specified_value = " + str(authors_value)]


    contributors_value = row[78]

    if(contributors_value == "-" or contributors_value == "FALSE" or contributors_value == "[]" or contributors_value == "endpoint absent" or contributors_value == "endpoint offline"):
        contributors_value = 0
    else:
        contributors_value = 1

    verifiability_edges[row[0] + "_Verifiability"] += ["contributors_specified_value = " + str(contributors_value)]

    
    publishers_value = row[79]

    if(publishers_value == "-" or publishers_value == "FALSE" or publishers_value == "[]" or publishers_value == "endpoint absent" or publishers_value == "endpoint offline"):
        publishers_value = 0
    else:
        publishers_value = 1

    verifiability_edges[row[0] + "_Verifiability"] += ["publishers_specified_value = " + str(publishers_value)]


    sources_value = row[80]

    if(sources_value == "-" or sources_value == "FALSE" or sources_value == "[]" or sources_value == "endpoint absent" or sources_value == "endpoint offline"):
        sources_value = 0
    else:
        sources_value = 1

    verifiability_edges[row[0] + "_Verifiability"] += ["sources_specified_value = " + str(sources_value)]


    signed_value = row[81]

    if(signed_value == "-" or signed_value == "FALSE" or signed_value == "[]" or signed_value == "endpoint absent" or signed_value == "endpoint offline"):
        signed_value = 0
    else:
        signed_value = 1

    verifiability_edges[row[0] + "_Verifiability"] += ["signed_value = " + str(signed_value)]


    return verifiability_edges


def add_currency(row, domain):
    currency_edges = {}

    currency_edges[row[0] + "_Currency"] = [row[0]]

    age_of_data = row[8]

    if(age_of_data == "-" or age_of_data == "FALSE" or age_of_data == "[]" or age_of_data == "endpoint absent" or age_of_data == "endpoint offline" or age_of_data == "insufficient data" or age_of_data == "Could not process formulated query on indicated endpoint"):
        age_of_data = 0
    else:
        age_of_data = 1

    currency_edges[row[0] + "_Currency"] += ["age_of_data_specified_value = " + str(age_of_data)]


    modification_date_of_statements = row[9]

    if(modification_date_of_statements == "-" or modification_date_of_statements == "FALSE" or modification_date_of_statements == "[]" or modification_date_of_statements == "endpoint absent" or modification_date_of_statements == "endpoint offline" or modification_date_of_statements == "insufficient data" or modification_date_of_statements == "Could not process formulated query on indicated endpoint"):
        modification_date_of_statements = 0
    else:
        modification_date_of_statements = 1

    currency_edges[row[0] + "_Currency"] += ["modification_date_of_statements_specified_value = " + str(modification_date_of_statements)]

    time_elapsed_since_last_modification = row[11]

    if(time_elapsed_since_last_modification == "-" or time_elapsed_since_last_modification == "FALSE" or time_elapsed_since_last_modification == "[]" or time_elapsed_since_last_modification == "endpoint absent" or time_elapsed_since_last_modification == "endpoint offline" or time_elapsed_since_last_modification == "insufficient data" or time_elapsed_since_last_modification == "Could not process formulated query on indicated endpoint"):
        time_elapsed_since_last_modification = 0
    else:
        time_elapsed_since_last_modification = 1

    currency_edges[row[0] + "_Currency"] += ["time_elapsed_since_last_modification_specified_value = " + str(time_elapsed_since_last_modification)]

    
    history_of_updates = row[12]

    if(history_of_updates == "-" or history_of_updates == "FALSE" or history_of_updates == "[]" or history_of_updates == "endpoint absent" or history_of_updates == "endpoint offline" or history_of_updates == "insufficient data" or history_of_updates == "Could not process formulated query on indicated endpoint"):
        history_of_updates = 0
    else:
        history_of_updates = 1

    currency_edges[row[0] + "_Currency"] += ["history_of_updates_specified_value = " + str(history_of_updates)]

    return currency_edges


def add_timeliness(row, domain):
    timeliness_edges = {}

    timeliness_edges[row[0] + "_Timeliness"] = [row[0]]

    #Considered as validation
    update_frequency = row[64]

    if(update_frequency == "-" or update_frequency == "FALSE" or update_frequency =="endpoint absent" or update_frequency == "endpoint offline" or update_frequency == "absent"):
        update_frequency = 0
    else:
        update_frequency = 1

    timeliness_edges[row[0] + "_Timeliness"] += ["update_frequency_value = " + str(update_frequency)]

    return timeliness_edges


def add_completeness(row, domain):
    completeness_edges = {}

    completeness_edges[row[0] + "_Completeness"] = [row[0]]

    interlinking_completeness = None

    try:
        interlinking_completeness = round(float(row[84]), 1)
    except (ValueError, TypeError):
        pass

    completeness_edges[row[0] + "_Completeness"] += ["interlinking_completeness_value = " + str(interlinking_completeness)]

    return completeness_edges


def add_amount_of_data(row, domain):
    amount_of_data_edges = {}

    amount_of_data_edges[row[0] + "_Amount_Of_Data"] = [row[0]]

    number_of_triples_query = row[60]

    if(number_of_triples_query == "-" or number_of_triples_query == "FALSE"):
        number_of_triples_query = 0
    else:
        number_of_triples_query = 1

    amount_of_data_edges[row[0] + "_Amount_Of_Data"] += ["number_of_triples_retrievable_value = " + str(number_of_triples_query)]

    level_of_detail = row[63]

    if(level_of_detail == "-" or level_of_detail == "FALSE"):
        level_of_detail = 0
    else:
        level_of_detail = 1

    amount_of_data_edges[row[0] + "_Amount_Of_Data"] += ["level_of_detail_specified_value = " + str(level_of_detail)]

    number_of_entities = row[61]
    number_of_entities_with_regex = row[62]

    scope_retrievable = None

    if((number_of_entities == "-" or number_of_entities == "FALSE") and (number_of_entities_with_regex == "-" or number_of_entities_with_regex == "FALSE")):
        scope_retrievable = 0
    else:
        scope_retrievable = 1

    amount_of_data_edges[row[0] + "_Amount_Of_Data"] += ["scope_retrievable_value = " + str(scope_retrievable)]

    return amount_of_data_edges


def add_representational_conciseness(row, domain):
    representational_conciseness_edges = {}

    #representational_conciseness_edges[row[0] + "_Representational_Conciseness"] = [row[0]]

    #there is no "keeping URIs short" metric identifiable in our data

    return representational_conciseness_edges


def add_interoperability(row, domain):
    interoperability_edges = {}

    interoperability_edges[row[0] + "_Interoperability"] = [row[0]]

    new_vocabolaries = row[85]

    reuse_value = None
    if(new_vocabolaries == "-" or new_vocabolaries == "FALSE" or new_vocabolaries == "[]"):
        reuse_value = 1
    else:
        reuse_value = 0

    interoperability_edges[row[0] + "_Interoperability"] += ["_reuse_of_existing_vocabularies_value = " + str(reuse_value)]

    #Mismatch on the calculation of this metric between web-app main page and web-app specific algorithm page
    #I'll use the one on the main page

    new_terms = row[86]

    reuse_value = None
    if(new_terms == "-" or new_terms == "FALSE" or new_terms == "[]"):
        reuse_value = 1
    else:
        reuse_value = 0

    interoperability_edges[row[0] + "_Interoperability"] += ["_reuse_of_existing_terms_value = " + str(reuse_value)]

    return interoperability_edges


def add_understandability(row, domain):
    understandability_edges = {}
    
    understandability_edges[row[0] + "_Understandability"] = [row[0]]

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
        human_readable_labelling_value = round(float(num_of_labels / num_of_triples_query * 100), 1)

    understandability_edges[row[0] + "_Understandability"] += ["human_readable_labelling_value = " + str(human_readable_labelling_value)]

    presence_of_examples = row[90]

    if(presence_of_examples == "-" or presence_of_examples == "FALSE"):
        presence_of_examples = 0
    else:
        presence_of_examples = 1

    understandability_edges[row[0] + "_Understandability"] += ["exemplary_sparql_queries_value = " + str(presence_of_examples)]

    regex_uri_value = row[89]

    if(regex_uri_value == "-" or regex_uri_value == "FALSE" or regex_uri_value == "[]"):
        regex_uri_value = 0
    else:
        regex_uri_value = 1

    understandability_edges[row[0] + "_Understandability"] += ["regex_of_the_uris_value = " + str(regex_uri_value)]

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

    understandability_edges[row[0] + "_Understandability"] += ["indication_of_metadata_value = " + str(indication_of_metadata_value)]

    return understandability_edges


def add_interpretability(row, domain):
    interpretability_edges = {}

    interpretability_edges[row[0] + "_Interpretability"] = [row[0]]

    #No presence of "num of triples without "rdf:type" property" kind of column in our data
    #So, I' won't include edges for "no misinterpretation of missing values" metric

    use_of_rdf_structures = row[41]

    if(use_of_rdf_structures == "-" or use_of_rdf_structures == "FALSE"):
        use_of_rdf_structures = 0
    else:
        use_of_rdf_structures = 1

    interpretability_edges[row[0] + "_Interpretability"] += ["_atypical_use_of_collection_containers_and_reification_value = " + str(use_of_rdf_structures)]

    return interpretability_edges


def add_versatility(row, domain):
    versatility_edges = {}

    versatility_edges[row[0] + "_Versatility"] = [row[0]]

    languages = row[13]

    if(languages == "-" or languages == f"{{}}" or languages == "[]" or languages == "FALSE"):
        languages = 0
    else:
        languages = 1

    versatility_edges[row[0] + "_Versatility"] += ["specification_of_used_languages_value = " + str(languages)]


    serialization_formats = row[15]

    if(serialization_formats == "-" or serialization_formats == "[]" or serialization_formats == "FALSE"):
        serialization_formats = 0
    else:
        serialization_formats = 1

    versatility_edges[row[0] + "_Versatility"] += ["serialization_formats_specified_value = " + str(serialization_formats)]


    availability_of_sparql_endpoint = row[2]
    availability_of_rdf_dump = row[4]

    accessing_of_data_in_different_ways = None

    if(availability_of_sparql_endpoint == "Available" and availability_of_rdf_dump == "1"):
        accessing_of_data_in_different_ways = 1
    else:
        accessing_of_data_in_different_ways = 0
    
    versatility_edges[row[0] + "_Versatility"] += ["accessing_of_data_in_different_ways_value = " + str(accessing_of_data_in_different_ways)]

    return versatility_edges


def add_KG_data(row):

    edges = {}

    #will return a dictionary of unique edges
    domain = None
    try:
        domain = datasets[row[0]].get("domain")
    except:
        return edges
    
    
    edges[row[0]] = [row[0], domain]

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
