import sys
import re 
from tools import *

def main():
    find_entity_for_specific_prop()
   
        
       
   
    
if __name__=="__main__":
    #print(clean_file("result_prop.json"))
    main()

def find_entity_for_specific_prop(prop : str):
    sameAs_file = sys.argv[1]
    result_file = "../data/result_entity_that_support_p.json"
    name_of_prop = prop.split("/")[-1][0:-1]
    output_file = "../data/prop_"+name_of_prop+"_support_db.ttl"
    slice_size = 500 #number of values in the VALUES keyword in sparql
    db_entity_list, _ = list(map(list,read_sameAs_file(sameAs_file))) #convert the sets back to maps
    
    sliced = property_list_cutting(db_entity_list,slice_size) #cut the big list into slice in a 2D list
    query_values_strings = [] #list of string properties used for VALUES in the sparql query
    for i in sliced:
        query_values_strings.append(query_generate_VALUES(i)) #join all prop in each bucket in a single string
    
    #call with sparql to get all properties used for each entities
    for entity in query_values_strings:
        sparql_query = """select distinct ?e ?p ?v  where {
            values ?e { """+entity+""" }.
            bind("""+prop+""" as ?p)
            ?e ?p ?v.
            }  
            """
    sparql_query = re.sub(r"\n|'","",sparql_query)
    sparql_call(sparql_query, result_file)
    concat_result_files(result_file, output_file, var_names=["e","p","v"])

def count_property_support():
    """
        Count the support for every property supported by entity that have a sameAs link
    """
    sameAs_file = sys.argv[1]
    result_file = "../data/result_prop.json"
    dict_output_file = "../data/property_support.json"
    slice_size = 500 #number of values in the VALUES keyword in sparql

    db_entity_list, _ = list(map(list,read_sameAs_file(sameAs_file))) #convert the sets back to maps
    
    sliced = property_list_cutting(db_entity_list,slice_size) #cut the big list into slice in a 2D list
    query_values_strings = [] #list of string properties used for VALUES in the sparql query
    for i in sliced:
        query_values_strings.append(query_generate_VALUES(i)) #join all prop in each bucket in a single string
    
    #call with sparql to get all properties used for each entities
    for entity in query_values_strings:
        sparql_query = """select distinct ?a ?b  where {
            values ?a { """+entity+""" }.
            ?a ?b ?_.
            }  
            """
    sparql_query = re.sub(r"\n|'","",sparql_query)
    
    sparql_call(sparql_query, result_file)

    read_result_file(result_file, dict_output_file, prop_var_name="b")
    
