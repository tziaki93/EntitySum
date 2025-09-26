"""
 edw dhmiourgw ta properties1,2,3
"""
import re

def propertiesDataset_1 (dataset):
        
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
           
        with open(f"C:/Users/gtrouli/Desktop/src/EntitySum-main/data/{dataset_folder}/{j}/{j}_desc.nt", "r", encoding="utf-8") as file1:
           for line1 in file1:
                line1 = line1.strip()
                match1 = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line1)
                if match1:
                    predicate = match1.group(2)
                    valueprop = 0.0  
                    with open(f'C:/Users/gtrouli/Desktop/src/EntitySum-main/centrality_measures/{prop_folder}/properties/{dataset}_properties(dataset).txt', "r", encoding="utf-8", errors="ignore") as file2:  
                        for line2 in file2:
                            line2 = line2.strip()
                            if line2:
                                parts2 = line2.split("\t")
                                
                               # print('<'+predicate+'>')
                               # print(parts2[0])
                                with open(f"C:/Users/gtrouli/Desktop/src/EntitySum-main/centrality_measures/{prop_folder}/properties/properties{j}.txt", 'a', encoding="utf-8") as output_file:

                                    if '<'+predicate+'>' == parts2[0]:
                                        #print(parts2[0],predicate)
                                        valueprop = parts2[1]                                
                                        output_file.write(f"{predicate}\t{valueprop}\n")
                                        break
        j += 1

#propertiesDataset_1 ('dbpedia')
