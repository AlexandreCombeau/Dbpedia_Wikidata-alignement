import json
import os
import typing
from functools import reduce

import ijson

QUERY_SERVICE = "~soulard/QueryHDT/SparqlHomemade2.jar"
DATABASE_PATH = {
    "dbpedia": "~/soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt",
    "wikidata": "~/soulard/Graphs_HDT/Wikidata/Wikidata_final.hdt"
}


def list_toStr(lst: list) -> str:
    """From a list return a string composed of all element of the list joined

    Returns:
        str : return a string of the type "list[1] list[2] ... list[n]"
    """
    joined_string = reduce(lambda acc, x: acc+" "+str(x), lst, "")

    return joined_string

def property_list_cutting(l: list ,slice_size: int ) -> list[list[str]]:
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

def read_json_file(file: str) -> list[tuple[set[str], set[str]]]:
    """Return a set of each variable in the json file
    Args:
        file (str): json file path
    """
    with open(file, 'r', encoding="UTF-8") as f:
        vars = [record for record in ijson.items(f, "head.vars")][0]

    # create a dict for each variable in our json file
    values = [set() for _ in range(len(vars))]

    with open(file, 'r', encoding="UTF-8") as f:
        for record in ijson.items(f, "results.bindings.item"):
            for i in range(len(vars)):
                values[i].add(f'<{record[vars[i]]["value"]}>')

    return values


def sparql_call(database: str, query_file: str, output_file: str) -> int:
    """Call a jar file to execute a sparql query on a database for a specified query 
    Args:
        sparql_query (str): sparql query we want to execute on a database
    """
    #jar_path = "~/../soulard/QueryHDT/SparqlToJSON.jar"

    # call with sparql to get all entities for a specific property
    hdt_query_command = "java -Xmx50G -Xms50G -jar "+QUERY_SERVICE + \
        " "+DATABASE_PATH[database]+" "+query_file+" "+output_file
    # get return code to check if query command is fine
    return os.system(hdt_query_command)


def parse_properties_file(properties_pair_file: str) -> str:
    """Parse file containing pair of properties we want to generate a dataset from
    Args:
        Path of properties pair file, <p1>\t<q1>\n<p2>\t<q2>....

    """
    db_wk_pairs = []
    with open(properties_pair_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if len(splited := line.split(" ")) == 2:
                db_wk_pairs.append((splited[0], splited[1]))

    return db_wk_pairs


def get_prop_name(prop: str) -> str:
    return prop.strip().split("/")[-1][0:-1]


def get_support(prop: str, entity_list: list[str], database_name: str, output_file_path: str, output_file_name : str = "") -> str:


    output_file = "../data/"+output_file_path+"/"+database_name+"-"+get_prop_name(prop)+".json"

    if output_file_name:
        output_file = "../data/"+output_file_path+"/"+output_file_name+".json"

    if database_name == "wikidata":
        # transform <http://www.wikidata.org/prop/P11143> into <http://www.wikidata.org/prop/statement/P11143>
        prop = "/".join((x := prop.split("/"))[0:-1])+"/statement/"+x[-1]

    sparql_query = """select distinct ?e ?v where {
        values ?e { """+list_toStr(entity_list)+""" }.
        bind("""+prop+""" as ?p)
        ?e ?p ?v.
        }  
        """

    query_file = "../data/"+output_file_path+"/"+database_name+"-"+get_prop_name(prop)+"_support_query"
    with open(query_file, "w", encoding="utf-8") as f:
        f.write(sparql_query)

    return_code = sparql_call(database_name, query_file, output_file)
    #TODO with return code
    return output_file


def get_sameAs(db_prop_name : str, wk_prop_name : str, support_file : str, database_name : str, output_file_path):

    entities,_ = read_json_file(support_file) #we only get <e,v> files

    output_file = "../data/"+output_file_path+"/"+"db-"+db_prop_name+"_wk-"+wk_prop_name+"_sameAs.json"

    if database_name == "wikidata":
        # transform <http://www.wikidata.org/prop/P11143> into <http://www.wikidata.org/prop/statement/P11143>
        prop = "/".join((x := prop.split("/"))[0:-1])+"/statement/"+x[-1]


    sparql_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#> 
        select distinct ?e ?v  where {
            values ?e { """+list_toStr(entities)+""" }. 
            ?e owl:sameAs ?v.
            FILTER(strstarts(str(?v), 'http://www.wikidata.'))
        }  
    """ 
    #sparql_query 
    query_file = "../data/"+output_file_path+"/"+"db-"+db_prop_name+"_wk-"+wk_prop_name+"_sameAs_query"
    with open(query_file, "w", encoding="utf-8") as f:
        f.write(sparql_query)

    #TODO 
    return_code = sparql_call(database_name, query_file, output_file)
    return output_file


def merge_JsonFiles(filename : list[str], output_file_path : str, prop : str) -> None:
    bindings = list()
    var = list()
    vars_flag = True
    for f1 in filename:
        if vars_flag:
            with open(f1, 'r') as f:
                f_data = json.load(f)
                var = f_data['head']['vars']
                vars_flag = False

        with open(f1, 'r') as f:
            f_data = json.load(f)
            bindings.extend(f_data['results']['bindings'])
            
    # Create the merged JSON object
    merged_data = {
        'head': {
            'vars': var
        },
        'results': {
            'bindings': bindings
        }
    }
    output_file = "../data/"+output_file_path+"/dbpedia-"+get_prop_name(prop)+".json"
    with open('merged_json.json', 'w') as output_file:
        json.dump(merged_data, output_file)


