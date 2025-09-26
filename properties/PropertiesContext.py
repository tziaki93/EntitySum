import re
from collections import Counter

def propertiesContext (dataset):
        
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
        properties = []
       
        with open(f"C:/Users/gtrouli/Desktop/src/EntitySum-main/data/{dataset_folder}/{j}/{j}_desc.nt", "r", encoding="utf-8") as file1:
              for line1 in file1:
                    line1 = line1.strip()
                    match1 = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line1)
                    if match1:
                        properties.append(match1.group(2))
            
        # Count the frequency of each property
        property_frequency = Counter(properties)
            
       
        with open(f'C:/Users/gtrouli/Desktop/src/EntitySum-main/centrality_measures/{prop_folder}/properties/properties_{j}.txt', 'w', encoding="utf-8") as output_file:
        
          for prop in properties:
                    output_file.write(f"{prop}\t{property_frequency[prop]}\n")
                    
             
       
          j += 1
#propertiesContext ('dbpedia')