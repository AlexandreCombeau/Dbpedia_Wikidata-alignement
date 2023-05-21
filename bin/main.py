import sys
import re 
from tools import *

def main():
    sameAs_file = sys.argv[1]
    #sameAs_file = "dbpedia_sameAs_clean.json"
    db_entity_list, wk_entity_list = list(map(list,read_sameAs_file(sameAs_file))) #convert the sets back to maps
    
    
    slice_size = 500 #number of values in the VALUES keyword in sparql
    sliced = property_list_cutting(db_entity_list,slice_size) #cut the big list into slice in a 2D list
    query_values_strings = [] #list of string properties used for VALUES in the sparql query
    for i in sliced:
        query_values_strings.append(query_generate_VALUES(i)) #join all prop in each bucket in a single string
    
    #call with sparql to get all properties used for each entities
    for index, prop in enumerate(query_values_strings):
        result_file = "result_prop.json"
        #result_file = "result_prop"+str(index)+".json"

        sparql_query ="""select distinct ?a ?b  where {
        values ?a { """+prop+""" }.
        ?a ?b ?_.
        }  
        """
        sparql_query = re.sub(r"\n|'","",sparql_query)
        
        return_code = sparql_call(sparql_query, result_file)
        if return_code != 0:
            raise Exception("Query command error")
        read_result_file(result_file)
        #todo waiting routine
        #need wait command to process result file before calling new sparql query
        
    
if __name__=="__main__":
    
    main()