"""
edw ypologizontai ta varh me vash ola ta desc kai paragetai 1 arxeio opou me vash 
ayto tha dhmiourghthoun ta properties1,2,3 ktl meta prepei na paw sto 
PropertiesDataset_1(assign properties weights)
"""
from collections import Counter

def read_triples_from_nt_file(file_path):
    triples = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            triple_parts = line.strip().split()
            subject = triple_parts[0]
            predicate = triple_parts[1]
            object = triple_parts[2]
            triples.append((subject, predicate, object))
    return triples


def propertiesDataset (dataset):
    total_triples=[]
        
    if 'dbpedia' in dataset:   
        j = 1
        N=166
        prop_folder='ESBM/dbpedia'
        dataset_folder='ESBM_benchmark_v1.2/dbpedia_data'
    
    elif 'lmdb' in dataset:
        j = 101
        N=176 
        prop_folder='ESBM/LMDB'
        dataset_folder='ESBM_benchmark_v1.2/lmdb_data'
                  
    # elif 'faces' in dataset:
    #      j = 1
    #      N 50:
    #      prop_folder='FACES'
    #      dataset_folder='FACES/faces_data'
        
    while j < N: 
        if 'dbpedia' in dataset and j == 101:
            j = 141
        elif 'lmdb' in dataset and j == 141:
            j = 166         
        desc_file = "C:/Users/gtrouli/Desktop/src/EntitySum-main/data/"+str(dataset_folder)+"/" + str(j) + "/" + str(j) +"_desc.nt"
        desc_triples = read_triples_from_nt_file(desc_file)
        total_triples += desc_triples
        
        j+=1
    # Count frequency of props
    predicate_counts = Counter(triple[1] for triple in total_triples)
    
    # Calculate weights based on frequency
    total_count = sum(predicate_counts.values())
    predicate_weights = {predicate: count / total_count for predicate, count in predicate_counts.items()}
    
    
    with open(f'C:/Users/gtrouli/Desktop/src/EntitySum-main/centrality_measures/{prop_folder}/properties/{dataset}_properties(dataset).txt', 'w',encoding="utf-8") as output_file:

        for predicate, count in predicate_counts.items():
            #print(f"{predicate}: {count}")
            output_file.write(f"{predicate}\t{count}\n")

#propertiesDataset ('dbpedia')