import typing
from functools import reduce 
import ijson
import json
import os

QUERY_SERVICE = "~soulard/QueryHDT/SparqlHomemade2.jar"
DATABASE_PATH = {
    "dbpedia"  : "~/soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt",
    "wikidata" : "~/soulard/Graphs_HDT/Wikidata/Wikidata_final.hdt" 
}

def query_generate_VALUES(lst: list) -> str:
    """From a list return a string composed of all element of the list joined

    Returns:
        str : return a string of the type "list[1] list[2] ... list[n]"
    """
    joined_string = reduce(lambda acc,x : acc+" "+str(x), lst, "")
    return joined_string

#TODO
def read_sameAs_file(file: str, var_names : list[str] = ["DB","WK"]) -> tuple[set[str],set[str]]:
    """Generate a list of sameAs from Dbpedia and Wikidata
    Args:
        file (str): sameAs json file name
    """
    f_read = open(file, 'r', encoding="UTF-8")

    first,second = var_names#refactor with var name header from json file

    db_entity_list = set()
    wk_entity_list = set()

    for record in ijson.items(f_read, "results.bindings.item"):
        db_entity_list.add(f'<{record[first]["value"]}>')
        wk_entity_list.add(f'<{record[second]["value"]}>')

    f_read.close()
    return db_entity_list,wk_entity_list


def read_ttl_file(file: str) -> tuple[list[str],list[str],list[str]]:
    """Generate a list entity property value from a ttl file
    Args:
        file (str): sameAs json file name
    """
    f_read = open(file, 'r', encoding="UTF-8").read()

    entity = []
    prop = []
    value = []

    for line in f_read.split("\n"):
        _line = line.split("\t")
        if len(_line) == 3:
            e,p,v = _line
            entity.append(e)
            prop.append(p)
            value.append(v)
        
    return entity,prop,value


def read_result_file(file : str, output_file : str, prop_var_name : str) -> None:
    """Read a result file to fill a dictionary 

    Args:
        file (str): result file in json format
    """
    
    f_read = open(file, 'r', encoding="UTF-8")
    prop = prop_var_name #name of the sparql var
    properties_count_file = output_file #dict file name
    #if file exist open json file and load 
    if os.path.exists(properties_count_file):
        with open(properties_count_file) as json_file:
            property_dictionnary = json.load(json_file)
            
    #else start with empty dict
    else:
        property_dictionnary = {}

    for record in ijson.items(f_read, "results.bindings.item"):
        item = (f'<{record[prop]["value"]}>')
        prop_count = property_dictionnary.get(item)
        if prop_count: property_dictionnary[item] += 1
        else: property_dictionnary[item] = 1

    f_read.close()
    #dump new dict
    with open(properties_count_file, "w") as fp:
        json.dump(property_dictionnary,fp) 

def sparql_call(sparql_query: str, result_file : str, database_name : str = "dbpedia") -> int :
    """Call a jar file to execute a sparql query on a database for a specified query 

    Args:
        sparql_query (str): sparql query we want to execute on a database
    """
    jar_path = "~/../soulard/QueryHDT/SparqlToJSON.jar"
    database_path = {
        "dbpedia" : "~/../soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt",
        "wikidata" : "~/../soulard/Graphs_HDT/Wikidata/Wikidata_final.hdt" 
    }
    dataset_path = database_path[database_name]
    #hdt_command = "nohup java -Xmx120G -Xms120G -jar "+jar_path+" "+dataset_path+" \""+sparql_query+"\" > "+result_file+" &"
    hdt_command = "java -jar "+jar_path+" "+dataset_path+" \""+sparql_query+"\" > "+result_file
    return os.system(hdt_command)

def clean_nohup_file(result_file : str) -> None:
    """Commands to remove unwanted string at the start of nohup resulting files

    Args:
        result_file (str): _description_

    Returns:
        _type_: _description_
    """
    code = 0
    new_res_file = result_file.split(".")[0]+"_clean.json"
    code += os.system("cp "+result_file+" "+new_res_file)
    code += os.system("awk 'NR > 3 { print }' < "+new_res_file+" > "+result_file) #remove first 3 lines of the file
    return code

def concat_result_files(result_file : str, output_file : str, var_names : list) -> None:
    """Concat the json file to the output file

    Args:
        result_file (str): json file 
        output_file (str): ttl format file, append at the end of file
    """
    
    e,p,v = var_names
    f_read = open(result_file, 'r', encoding="UTF-8")
    f_write = open(output_file, 'a', encoding="UTF-8")
    for record in ijson.items(f_read, "results.bindings.item"):
        entity = (f'<{record[e]["value"]}>')
        prop = (f'<{record[p]["value"]}>')
        value = (f'{record[v]["value"]}')
        f_write.write(entity+"\t"+prop+"\t"+value+"\n")
        
    f_read.close()
    f_write.close()



