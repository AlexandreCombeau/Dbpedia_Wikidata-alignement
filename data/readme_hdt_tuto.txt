Command to do sparql query
    nohup java -Xmx120G -Xms120G -jar ./sharewithserver/QueryHDT/SparqlToJSON.jar ./FILE.hdt "QUERY" > ./OUTPUT &

Without nohup
    java -jar ./sharewithserver/QueryHDT/SparqlToJSON.jar ./FILE.hdt "QUERY" > ./OUTPUT &

With Query
    java -jar ./sharewithserver/QueryHDT/SparqlToJSON.jar ./FILE.hdt "SELECT ?DB ?WK WHERE {{?DB sameAs ?WK. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))} UNION {?WK sameAs ?DB. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))}}" > ./OUTPUT &

Exemple de commandes qui marchent
    nohup java -Xmx120G -Xms120G -jar ../soulard/QueryHDT/SparqlToJSON.jar ../soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt "PREFIX owl: <http://www.w3.org/2002/07/owl#> SELECT ?DB ?WK WHERE { {?DB owl:sameAs ?WK. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))} UNION {?WK owl:sameAs ?DB. FILTER(strstarts(str(?WK), 'http://www.wikidata.'))}} limit 10" > ./RequestResults/results2.json &

    java -jar ../soulard/QueryHDT/SparqlToJSON.jar ../soulard/Graphs_HDT/DBpedia/DBpedia_en.hdt "select ?a ?b ?c where { ?a ?b ?c } limit 10" > ./RequestResults/results.json

Pour convertir le resultat json en fichier .nt 
     python3 ../soulard/QueryHDT/From_JSON_to_NT_V3.py RequestResults/results.json ./RequestResults/_tmp.nt

