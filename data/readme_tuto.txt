Command to do sparql query
    nohup java -Xmx120G -Xms120G -jar ./sharewithserver/QueryHDT/SparqlToJSON.jar ./FILE.hdt "QUERY" > ./OUTPUT &

Without nohup
    java -jar ./sharewithserver/QueryHDT/SparqlToJSON.jar ./FILE.hdt "QUERY" > ./OUTPUT &

With Query
    java -jar ./sharewithserver/QueryHDT/SparqlToJSON.jar ./FILE.hdt "SELECT ?DB ?WK WHERE {{?DB sameAs ?WK. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))} UNION {?WK sameAs ?DB. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))}}" > ./OUTPUT &

Exemple de commandes qui marchent
    nohup java -Xmx120G -Xms120G -jar ../soulard/QueryHDT/SparqlToJSON.jar ../soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt 
        "PREFIX owl: <http://www.w3.org/2002/07/owl#> SELECT ?DB ?WK WHERE { {?DB owl:sameAs ?WK. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))} UNION {?WK owl:sameAs ?DB. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))}} limit 10" > ./RequestResults/results2.json &

    java -jar ../soulard/QueryHDT/SparqlToJSON.jar ../soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt "select ?a ?b ?c where { ?a ?b ?c } limit 10" > ./RequestResults/results.json

Pour convertir le resultat json en fichier .nt 
     python3 ../soulard/QueryHDT/From_JSON_to_NT_V3.py RequestResults/results.json ./RequestResults/_tmp.nt

Pour recuperer les données dans le dossier courrant
    scp -r serv:~/Dbpedia_Wikidata-alignement/data/prop_releaseDate_support_db.ttl .

Pour refresh depot git
    git fetch origin master
    git reset --hard FETCH_HEAD
    git clean -df

Commande :
python3 main.py ../data/dbpedia_sameAs_clean.json "<http://dbpedia.org/ontology/releaseDate>" "dbpedia"
python3 main.py ../data/dbpedia_sameAs_clean.json "<http://www.wikidata.org/prop/statement/P10673>" "wikidata"
python3 main.py ../data/dbpedia_sameAs_clean.json "<http://www.wikidata.org/prop/statement/P10673>" "wikidata" ~soulard/QueryHDT/SparqlHomemade2.jar
python3 main.py ../data/dbpedia_sameAs_clean.json "<http://www.wikidata.org/prop/statement/P10673>" "wikidata" ~soulard/QueryHDT/SparqlHomemade2.jar
python3 main.py ../data/prop_.json "<http://www.wikidata.org/prop/statement/P10673>" "wikidata" ~soulard/QueryHDT/SparqlHomemade2.jar
python3 main.py ../data/prop_releaseDate_support_db.ttl "<http://www.wikidata.org/prop/statement/P10673>" "dbpedia" ~soulard/QueryHDT/SparqlHomemade2.jar &