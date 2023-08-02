import sys
import re 
import subprocess
from tools import *

def get_dataset_all_data(properties_pair_file : str, db_wk_sameAs : str) -> None:

    #parse file and get pair of properties
    tuples_properties = parse_properties_file(properties_pair_file)
    for db_prop,wk_prop in tuples_properties:
        db_prop_name = get_prop_name(db_prop)
        wk_prop_name = get_prop_name(wk_prop)
        print(db_prop_name,wk_prop_name)
        file_path = wk_prop_name+"_"+db_prop_name #create sub folder for this dataset

        if not(os.path.isdir("../data/"+file_path)): #if folder already exist we already have the dataset for this pair
            #continue
            subprocess.Popen(["mkdir ", "../data/"+file_path])#TODO add subprocess instead of system
        
        db_support_file = "../data/"+file_path+"/dbpedia-"+db_prop_name+".json"
        if not(os.path.isfile(db_support_file)) or is_file_empty(db_support_file):
            db_entity_list = list(read_json_file(db_wk_sameAs)[0])
            sliced_support_file = []
            #slice list into smaller slice
            for index,slice_db_list in enumerate(property_list_cutting(db_entity_list,5000)):
                #query smaller list
                file_name = "sliced_dbpedia-"+db_prop_name+"_"+str(index)
                db_slice_support_file = get_support(db_prop,slice_db_list,"dbpedia",file_path,output_file_name=file_name) #get dbpedia e-v
                #store file path
                sliced_support_file.append(db_slice_support_file)

            #merge all file into one json 
            db_support_file = merge_JsonFiles(sliced_support_file,file_path,db_prop_name)
            print(db_support_file)
            for file_path in sliced_support_file:
                subprocess.Popen(["rm ",file_path])
        #with the dbpedia e-v we get all <e owl:sameAs wk>
        
        db_wk_prop_sameAs_file = "../data/"+file_path+"/"+"db-"+db_prop_name+"_wk-"+wk_prop_name+"_sameAs.json"
        print("path sameAs file :",db_wk_prop_sameAs_file)
        print("db support file :",db_support_file) 
        
        if not(os.path.isfile(db_wk_prop_sameAs_file)) or is_file_empty(db_wk_prop_sameAs_file) :
            print("exec get_sameAs")
            db_wk_prop_sameAs_file = get_sameAs(db_prop_name,wk_prop_name,db_support_file,"dbpedia",file_path)
        
        
        wk_support_file = "../data/"+file_path+"/wikidata-"+db_prop_name+".json"
        if not(os.path.isfile(wk_support_file)) or is_file_empty(wk_support_file):
            #we have the wk e now we can fetch the e-v for wikidata
            print("read json wk")
            wk_entity_list = read_json_file(db_wk_prop_sameAs_file)[1]
            print("get_support wk")
            wk_support_file = get_support(wk_prop,wk_entity_list,"wikidata",file_path)
            print(wk_support_file)
    

def get_dataset(properties_pair_file : str, db_wk_sameAs : str) -> None:

    #parse file and get pair of properties
    tuples_properties = parse_properties_file(properties_pair_file)
    for db_prop,wk_prop in tuples_properties:
        db_prop_name = get_prop_name(db_prop)
        wk_prop_name = get_prop_name(wk_prop)
        print(db_prop_name,wk_prop_name)
        file_path = wk_prop_name+"_"+db_prop_name #create sub folder for this dataset

        if os.path.isdir("../data/"+file_path): #if folder already exist we already have the dataset for this pair
            continue
        subprocess.Popen(["mkdir ", "../data/"+file_path])
        db_entity_list = list(read_json_file(db_wk_sameAs)[0])[0:10000] #way too big need to split


        db_support_file = get_support(db_prop,db_entity_list,"dbpedia",file_path) #get dbpedia e-v
        print(db_support_file)
        #with the dbpedia e-v we get all <e owl:sameAs wk>
        db_wk_prop_sameAs_file = get_sameAs(db_prop_name,wk_prop_name,db_support_file,"wikidata",file_path)
        print(db_wk_prop_sameAs_file)
        #we have the wk e now we can fetch the e-v for wikidata
        wk_support_file = get_support(wk_prop,read_json_file(db_wk_prop_sameAs_file)[1],"wikidata",file_path)
        print(wk_support_file)
    
def main():

    properties_pair_file = sys.argv[1]
    sameAs_file = sys.argv[2]
    get_dataset_all_data(properties_pair_file,sameAs_file)

if __name__=="__main__":
    #print(clean_file("result_prop.json"))
    main()

  
