import sys
import re 
from tools import *



def get_dataset(properties_pair_file : str, db_wk_sameAs : str) -> None:

    #parse file and get pair of properties
    tuples_properties = parse_properties_file(properties_pair_file)
    for db_prop,wk_prop in tuples_properties:
        db_prop_name = get_prop_name(db_prop)
        wk_prop_name = get_prop_name(wk_prop)
        file_path = wk_prop_name+"-"+db_prop_name #create sub folder for this dataset
        if os.path.isdir("../data/"+file_path): #if folder already exist we already have the dataset for this pair
            continue
        os.system("mkdir ../data/"+file_path)
        #get dbpedia e-v
        db_support_file   = get_support(db_prop,read_json_file(db_wk_sameAs)[0],"dbpedia",file_path)
        #with the dbpedia e-v we get all <e owl:sameAs wk>
        db_wk_prop_sameAs_file = get_sameAs(db_prop_name,wk_prop_name,db_support_file,"wikidata",file_path)
        #we have the wk e now we can fetch the e-v for wikidata
        wk_support_file   = get_support(wk_prop,read_json_file(db_wk_prop_sameAs_file[1]),"wikidata",file_path)

    
def main():

    properties_pair_file = sys.argv[1]
    sameAs_file = sys.argv[2]
    get_dataset(properties_pair_file,sameAs_file)
    #prop = sys.argv[2]
    #database_name = sys.argv[3]
    #query_service = sys.argv[4]
    #get_sameAs_for_pop_hdt_version(sameAs_file, query_service, prop, database_name)
    #find_entity_for_specific_prop_hdt_version(sameAs_file, query_service, prop, database_name) 
    
if __name__=="__main__":
    #print(clean_file("result_prop.json"))
    main()

  