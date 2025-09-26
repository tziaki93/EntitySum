import re
import time
import networkx as nx
from SPARQLWrapper import SPARQLWrapper, JSON
from timeit import default_timer as timer



def calculate_radiality_centrality(graph, node):
    total_distance = 0
    shortest_paths = nx.single_source_shortest_path_length(graph, node)
    for target_node, shortest_path_length in shortest_paths.items():
        if target_node != node:
            total_distance += shortest_path_length
    num_nodes = len(graph.nodes()) - 1
    radiality_centrality = (num_nodes - 1) / total_distance
    return radiality_centrality

def generate_centrality_measures_lmdb(meas):
    cycles=0
    k=0
    file_name='C:/Users/gtrouli/Desktop/src/EntitySum-main/centrality_measures/ESBM/LMDB/ENTITIES/lmdb_entities.txt'
    entities=[]
    
    with open(file_name, "r") as file:
        for line in file:
            entities.append(line.strip())
    
    i = 101
    
    while i < 176:
        if i == 141:
            i = 166
    
        sparql_endpoint = "http://localhost:8890/sparql"
        
        graph = nx.Graph()
        entity_labels = []
        
        with open(f"C:/Users/gtrouli/Desktop/src/EntitySum-main/data/ESBM_benchmark_v1.2/lmdb_data/{i}/{i}_desc.nt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                if match:
                    #object_ = match.group(3)
                
                    if match.group(3)=='<'+entities[k]+'> ':
                        object_ = '<'+match.group(1)+'> '
                       # print(object_,'sub')
                    else:
                        object_ = match.group(3)
                        #print(object_,'obj')
                    
                    entity_labels.append(object_)
        
        sparql = SPARQLWrapper(sparql_endpoint)
        
        for node in entity_labels:
            try:
                if (node.startswith("<http://") or node.startswith("http://") ) and "^^" not in node :
                        
                    match_uri1 = node.replace("> ", "")
                    node = match_uri1.replace("<", "")
                    if "http://data.linkedmdb.org/resource/movie/film" in node:
                            node = node.replace("http://data.linkedmdb.org/resource/movie/film", "https://triplydb.com/Triply/linkedmdb/vocab/Film")
                    
                    if "http://data.linkedmdb.org/resource/movie/director" in node:
                            node = node.replace("http://data.linkedmdb.org/resource/movie/director", "https://triplydb.com/Triply/linkedmdb/vocab/Director")
                    
                    if "http://data.linkedmdb.org/resource/movie/actor" in node:
                            node = node.replace("http://data.linkedmdb.org/resource/movie/actor", "https://triplydb.com/Triply/linkedmdb/vocab/Actor")
                    
                    
                
                    if "http://data.linkedmdb.org/resource/" in node:
                            node = node.replace("http://data.linkedmdb.org/resource/", "https://triplydb.com/Triply/linkedmdb/id/")
                    
                   
                    match_uri=  node
                        
                    query = f"""                 
                        
                    CONSTRUCT {{ <{match_uri}> ?p ?o . ?s ?p <{match_uri}> . }}
                    WHERE {{ {{ <{match_uri}> ?p ?o . }} UNION {{ ?s ?p <{match_uri}> .  }} }}
     
                    """
                    print(query)
                else:
                    literal_value = node
                    if "^^<" in literal_value:
                        literal_value = node.replace(" ", "")
                        query = f"""
                            CONSTRUCT {{ ?s ?p {literal_value} . }}
                            WHERE {{ ?s ?p {literal_value} . }} 
                        """
                        
                    elif re.match(r'".*"@.*$', literal_value):
                        lang_tag = literal_value.split('@')[1].replace("'", "").strip() 
                        literal_value = literal_value.split('"')[1]
                        literal_value_escaped = literal_value.replace("'", "").strip()
                        query = f"""
                            CONSTRUCT {{ ?s ?p "{literal_value_escaped}"@{lang_tag} . }} 
                            WHERE {{ ?s ?p "{literal_value_escaped}"@{lang_tag} . }}
                        """
                       
                    else:
                        literal_value_escaped = literal_value.replace('"', '').replace("'", "").strip()
                        query = f"""
                            CONSTRUCT {{ ?s ?p "{literal_value_escaped}" . }}
                            WHERE {{ ?s ?p "{literal_value_escaped}" . }} 
                        """
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    subject = result["s"]["value"]
                    predicate = result["p"]["value"]
                    object_ = result["o"]["value"]
                    graph.add_edge(subject, object_)
                 #   print(predicate,object_)
            except: 
                continue
        
        if meas == 'pagerank':
            print('pagerank')
            start = timer()
            measure = nx.pagerank(graph)
            end = timer()
            cycles =(end-start)
            
            print ('execution time in seconds: %f' %(cycles))
            
            with open('centrality_measures/ESBM/LMDB/pagerank/pagerank_'+ str(i)+'.txt', 'w',encoding="utf-8") as output_file:
                for node in entity_labels:
                    if  (node.startswith("<http://") or node.startswith("http://") ) and "^^" not in node :  
                        match_uri1 = node.replace("> ","")
                        match_uri = match_uri1.replace("<","") 
                        if "http://data.linkedmdb.org/resource/movie/film" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/film", "https://triplydb.com/Triply/linkedmdb/vocab/Film")
                        
                        if "http://data.linkedmdb.org/resource/movie/director" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/director", "https://triplydb.com/Triply/linkedmdb/vocab/Director")
                        
                        if "http://data.linkedmdb.org/resource/movie/actor" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/actor", "https://triplydb.com/Triply/linkedmdb/vocab/Actor")
 
                        if "http://data.linkedmdb.org/resource/" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/", "https://triplydb.com/Triply/linkedmdb/id/")                      
                       
                    elif "^^<" in node:
                        match_uri = node.split('"')[1] 
                        print(match_uri)
                    elif "@" in node:
                        lang_tag = node.split('@')[1].replace("'", "").strip() 
                        literal_value = node.split('"')[1]
                        match_uri = literal_value
                        print(match_uri)
                    else:
                        match_uri = node.replace('"', '').replace("'", "").strip() 
                        print(match_uri)
                        
                    if match_uri in measure:
                        if match_uri!="":
                            output_file.write(f"{match_uri}\t{measure[match_uri]}\n")  
                        else:
                            output_file.write(f'""\t{0.0}\n')
                    else:
                        if match_uri!="":
                            output_file.write(f"{match_uri}\t0.0\n")
                        else:
                            output_file.write(f'""\t{0.0}\n')
        elif meas == 'degree':
            print('degree')
            start = timer()
            measure = nx.degree(graph)
            end = timer()
            cycles =(end-start)
            
            print ('execution time in seconds: %f' %(cycles))
            
            with open('centrality_measures/ESBM/LMDB/degree/degree'+ str(i)+'.txt', 'w',encoding="utf-8") as output_file:
                for node in entity_labels:
                    if  (node.startswith("<http://") or node.startswith("http://") ) and "^^" not in node :  
                        match_uri1 = node.replace("> ","")
                        match_uri = match_uri1.replace("<","") 
                        if "http://data.linkedmdb.org/resource/movie/film" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/film", "https://triplydb.com/Triply/linkedmdb/vocab/Film")
                        
                        if "http://data.linkedmdb.org/resource/movie/director" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/director", "https://triplydb.com/Triply/linkedmdb/vocab/Director")
                        
                        if "http://data.linkedmdb.org/resource/movie/actor" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/actor", "https://triplydb.com/Triply/linkedmdb/vocab/Actor")

                        if "http://data.linkedmdb.org/resource/" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/", "https://triplydb.com/Triply/linkedmdb/id/")
                        
                       
                    elif "^^<" in node:
                        match_uri = node.split('"')[1] 
                        print(match_uri)
                    elif "@" in node:
                        lang_tag = node.split('@')[1].replace("'", "").strip() 
                        literal_value = node.split('"')[1]
                        match_uri = literal_value
                        print(match_uri)
                    else:
                        match_uri = node.replace('"', '').replace("'", "").strip() 
                        print(match_uri)
                        
                    if match_uri in measure:
                        if match_uri!="":
                            output_file.write(f"{match_uri}\t{measure[match_uri]}\n")  
                        else:
                            output_file.write(f'""\t{0.0}\n')
                    else:
                        if match_uri!="":
                            output_file.write(f"{match_uri}\t0.0\n")
                        else:
                            output_file.write(f'""\t{0.0}\n')
        elif meas == 'betweeness':
                print('betweenness')
                start = timer()
                measure = nx.betweeness(graph)
                end = timer()
                cycles =(end-start)
                
                print ('execution time in seconds: %f' %(cycles))
                
                with open('centrality_measures/ESBM/LMDB/betweeness/betweeness'+ str(i)+'.txt', 'w',encoding="utf-8") as output_file:
                    for node in entity_labels:
                        if  (node.startswith("<http://") or node.startswith("http://") ) and "^^" not in node :  
                            match_uri1 = node.replace("> ","")
                            match_uri = match_uri1.replace("<","") 
                            if "http://data.linkedmdb.org/resource/movie/film" in match_uri:
                                    match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/film", "https://triplydb.com/Triply/linkedmdb/vocab/Film")
                            
                            if "http://data.linkedmdb.org/resource/movie/director" in match_uri:
                                    match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/director", "https://triplydb.com/Triply/linkedmdb/vocab/Director")
                            
                            if "http://data.linkedmdb.org/resource/movie/actor" in match_uri:
                                    match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/actor", "https://triplydb.com/Triply/linkedmdb/vocab/Actor")
    
                            if "http://data.linkedmdb.org/resource/" in match_uri:
                                    match_uri = match_uri.replace("http://data.linkedmdb.org/resource/", "https://triplydb.com/Triply/linkedmdb/id/")
                            
                           
                        elif "^^<" in node:
                            match_uri = node.split('"')[1] 
                            print(match_uri)
                        elif "@" in node:
                            lang_tag = node.split('@')[1].replace("'", "").strip() 
                            literal_value = node.split('"')[1]
                            match_uri = literal_value
                            print(match_uri)
                        else:
                            match_uri = node.replace('"', '').replace("'", "").strip() 
                            print(match_uri)
                            
                        if match_uri in measure:
                            if match_uri!="":
                                output_file.write(f"{match_uri}\t{measure[match_uri]}\n")  
                            else:
                                output_file.write(f'""\t{0.0}\n')
                        else:
                            if match_uri!="":
                                output_file.write(f"{match_uri}\t0.0\n")
                            else:
                                output_file.write(f'""\t{0.0}\n')

        elif meas == 'radiality':
            print('radiality')
            radiality_centralities = {}
            start = timer()
            output_filename = 'centrality_measures/ESBM/LMDB/radiality/radiality_' + str(i) + '.txt'
            with open(output_filename, 'w', encoding="utf-8") as output_file:
                for node in entity_labels:
                    if node.startswith("<http://") or node.startswith("http://"):
                        if "^^" not in node:
                            match_uri1 = node.replace("> ", "")
                            match_uri = match_uri1.replace("<", "")
                
                            if "http://data.linkedmdb.org/resource/movie/film" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/film", "https://triplydb.com/Triply/linkedmdb/vocab/Film")
                
                            if "http://data.linkedmdb.org/resource/movie/director" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/director", "https://triplydb.com/Triply/linkedmdb/vocab/Director")
                
                            if "http://data.linkedmdb.org/resource/movie/actor" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/actor", "https://triplydb.com/Triply/linkedmdb/vocab/Actor")
                
                            if "http://data.linkedmdb.org/resource/" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/", "https://triplydb.com/Triply/linkedmdb/id/")
                        
                    elif "^^<" in node:
                        match_uri = node.split('"')[1]
                
                    elif "@" in node:
                        lang_tag = node.split('@')[1].replace("'", "").strip()
                        literal_value = node.split('"')[1]
                        match_uri = literal_value
                        
                    else:
                        match_uri = node.replace('"', '').replace("'", "").strip()
                
                    if match_uri in graph:
                        if match_uri!="":
                            
                            radiality_centralities[match_uri] = calculate_radiality_centrality(graph, match_uri)
                            temp=radiality_centralities[match_uri]
                            output_file.write(f"{match_uri}\t{temp}\n")
                        else:
                            output_file.write(f'""\t{0.0}\n')
                    else:
                        if match_uri!="":
                            radiality_centralities[match_uri] = 0.0
                            output_file.write(f"{match_uri}\t{0.0}\n")
                        else:
                            output_file.write(f'""\t{0.0}\n')
                
            end = timer()
            cycles = (end - start)
            print('Execution time in seconds: %f' % (cycles))
        
        elif meas=='hits':
            print('hits')
            start = timer()
            authority, hub = nx.hits(graph)
            end = timer()
            cycles =(end-start)
            print ('execution time in seconds: %f' %(cycles))
            with open('centrality_measures/ESBM/LMDB/hits/hits_'+ str(i)+'.txt', 'w',encoding="utf-8") as output_file:
                for node in entity_labels:
            
                    if node.startswith("<http://") or node.startswith("http://"):
                        if "^^" not in node:
                            match_uri1 = node.replace("> ", "")
                            match_uri = match_uri1.replace("<", "")
                
                            if "http://data.linkedmdb.org/resource/movie/film" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/film", "https://triplydb.com/Triply/linkedmdb/vocab/Film")
                
                            if "http://data.linkedmdb.org/resource/movie/director" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/director", "https://triplydb.com/Triply/linkedmdb/vocab/Director")
                
                            if "http://data.linkedmdb.org/resource/movie/actor" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/movie/actor", "https://triplydb.com/Triply/linkedmdb/vocab/Actor")
                
                            if "http://data.linkedmdb.org/resource/" in match_uri:
                                match_uri = match_uri.replace("http://data.linkedmdb.org/resource/", "https://triplydb.com/Triply/linkedmdb/id/")
                        
                    elif "^^<" in node:
                        match_uri = node.split('"')[1]
                
                    elif "@" in node:
                        lang_tag = node.split('@')[1].replace("'", "").strip()
                        literal_value = node.split('"')[1]
                        match_uri = literal_value
                        
                    else:
                        match_uri = node.replace('"', '').replace("'", "").strip()
                    if match_uri in authority:
                        if match_uri!='':
                            output_file.write(f"{match_uri}\t{authority[match_uri]}\t{hub[match_uri]}\n")  
                        else:
                            output_file.write(f'""\t{0.0}\n')
                    else:
                        if match_uri!='':
                            output_file.write(f"{match_uri}\tKey not found\n")
                        else:
                           output_file.write(f'""\t{0.0}\n')
                  
        else: print ('wrong measure name')

        i += 1
        k += 1
