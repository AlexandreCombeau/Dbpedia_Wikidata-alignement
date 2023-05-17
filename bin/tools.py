from typing import Tuple,Set,List
from functools import reduce 
import ijson
import json
import os

def property_list_cutting(l: list ,slice_size: int ) -> List[List[str]]:
    """From a list, return slice 2D with n sublist of size "slice_size"

    Args:
        l (_type_): huge 1D list
        slice_size (_type_): 2D list composed of n "slice_size" list

    Returns:
        list : slice_size
    """
    index = 0
    sliced_list = []
    if len(l) < slice_size: return l
    while index<len(l):
        sliced_list.append(l[index:index+slice_size])
        index+=slice_size
    return sliced_list

def query_generate_VALUES(slice: list) -> str:
    """From a list return a string composed of all element of the list joined

    Args:
        slice (list): 1D list

    Returns:
        str : return a string of the type " slice[0] slice[1] slice[2] ... "
    """
    func = lambda acc,x : acc+" "+str(x)
    acc = ""
    joined_string = reduce(func, slice, acc)
    return joined_string


def read_sameAs_file(file: str) -> Tuple[Set[str],Set[str]]:
    """Generate a list of sameAs from Dbpedia and Wikidata, we keep track of how many lines we read 

    Args:
        file (str): sameAs json file name
        nb_lines (int): number of lines we want to read
    """
    f_read = open(file, 'r', encoding="UTF-8")

    first = "DB"
    second = "WK"

    db_entity_list = set()
    wk_entity_list = set()

    for record in ijson.items(f_read, "results.bindings.item"):
        db_entity_list.add(f'<{record[first]["value"]}>')
        wk_entity_list.add(f'<{record[second]["value"]}>')

    f_read.close()
    return db_entity_list,wk_entity_list


def read_result_file(file : str) -> None:
    """Read a result file to fill a dictionary 

    Args:
        file (str): result file in json format
    """
    
    f_read = open(file, 'r', encoding="UTF-8")
    prop = "b" #name of the sparql var
    properties_count_file = "property_support.json" #dict file name
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



def sparql_call(sparql_query: str, result_file : str) -> int :
    """Call a jar file to execute a sparql query on a database for a specified query 

    Args:
        sparql_query (str): sparql query we want to execute on a database
    """
    jar_path = "../soulard/QueryHDT/SparqlToJSON.jar"
    dataset_path = "../soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt"
    result_file_name = result_file
    result_file_path = "./RequestResults/"+result_file_name
    hdt_command = "nohup java -Xmx120G -Xms120G -jar "+jar_path+" "+dataset_path+" \""+sparql_query+"\" > "+result_file_path+" &"
    return os.system(hdt_command)

