import numpy as np
import re
from collections import Counter, defaultdict
total = 0
top = 10
measure = "degree"
j = 1

while j < 51:
   
   
    
    top_objects = np.array([], dtype=[('object_uri', '<U100'), ('value', float)])  
    top_predicates = np.array([], dtype=[('object_uri', '<U100'), ('value', float)]) 
    top_predicates1 = np.array([], dtype=[('object_uri', '<U100'), ('value', float)]) 
    top_predicates4 = np.array([], dtype=[('object_uri', '<U100'), ('value', float)]) 
    #final_weight = np.array([], dtype=[('uri', 'U1000'), ('value', float)])
    uris = []
    final_weight = np.empty(0, dtype=[('uri', 'U1000'), ('value', float)])


    with open("C:/Users/gtrouli/Desktop/src/centrality_measures/FACES/degree/" + str(measure) + "_" + str(j) + ".txt", "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split("\t")
                if len(parts) < 2:
                    object_uri = " "
                    value1 = 0.0 
                if len(parts) == 3:
                    object_uri = parts[0]
                    value1 = float(parts[1]) if parts[1] != "Key not found" else 0.0
                    value2 = float(parts[2]) if parts[2] != "Key not found" else 0.0
                    if object_uri=='""'  :
                        value1 = 0.0
                        value2 = 0.0

                    if   'http://www.w3.org/2002/07/owl#Thing' in object_uri:
                        value1 =0.0 
                        value2 = 0.0
                    top_objects = np.append(top_objects, np.array([(object_uri, value1+value2)], dtype=top_objects.dtype))
                else:
                    #print(j)
                    object_uri = parts[0]
               
                    
                    value1 = float(parts[1]) if parts[1] != "Key not found" else 0.0
                   
                    if  'http://www.w3.org/2002/07/owl#Thing' in object_uri :
                        value1 =0.0 
                    if  object_uri.strip() == '""' :
                        value1 =0.0 

                    top_objects = np.append(top_objects, np.array([(object_uri, value1)], dtype=top_objects.dtype))
                

       
    with open("C:/Users/gtrouli/Desktop/src/centrality_measures/FACES/degree_" + str(j) + ".txt", "r", encoding="utf-8", errors="ignore") as file1:
        for line in file1:
            line = line.strip()
            if line:
                parts2 = line.split("\t")
                object_uri2 = parts2[0]
                
                value2 = float(parts2[1]) if parts2[1] != "Key not found" else 0.0 
                if object_uri2.strip() == '""' or 'jpg' in object_uri2 or 'png' in object_uri2:
                        
                        value2 = 0.0 
                if  'http://www.w3.org/2002/07/owl#Thing' in object_uri2:
                        value2 = 0.0 
                if  'ontology'  in object_uri2 or 'schema' in object_uri2:
                        value2 =0.0
                top_predicates = np.append(top_predicates, np.array([(object_uri2, value2)], dtype=top_predicates.dtype))

    
    with open("C:/Users/gtrouli/Desktop/src/centrality_measures/FACES/properties" + str(j) + ".txt", "r", encoding="utf-8", errors="ignore") as file3:
        for line in file3:
            line = line.strip()
            if line:
                parts3 = line.split("\t")
                object_uri3 = parts3[0]
                if object_uri3!="":
                    value3 = 1/float(parts3[1])  
                else:  
                    value3 = 0.0
                top_predicates1 = np.append(top_predicates1, np.array([(object_uri3, value3)], dtype=top_predicates1.dtype))
    
    
    with open("C:/Users/gtrouli/Desktop/src/centrality_measures/FACES/properties_" + str(j) + ".txt", "r", encoding="utf-8", errors="ignore") as file4:
        for line in file4:
            line = line.strip()
            if line:
                parts4 = line.split("\t")
            if len(parts4) >= 2:  
                object_uri4 = parts4[0]
                if object_uri4!="":
                    value4 = 1/float(parts4[1])  
                else:  
                    value4 = 0.0
                top_predicates4 = np.append(top_predicates4, np.array([(object_uri4, value4)], dtype=top_predicates4.dtype))
            else:
                value4 = 0.0 

    
   
    max_value_objects = np.max(top_objects['value'])
    max_value_predicates = np.max(top_predicates['value'])
    max_value_predicates1 = np.max(top_predicates1['value'])
    max_value_predicates4 = np.max(top_predicates4['value'])

    #if max_value_objects == 0 or np.isnan(max_value_objects):
    #     top_objects['value'] = 0
        # print (j)
   # else:
    top_objects['value'] /= max_value_objects
    top_predicates['value'] /= max_value_predicates
    top_predicates1['value'] /= max_value_predicates1
    top_predicates4['value'] /= max_value_predicates4


    with open("C:/Users/gtrouli/Desktop/src/data/FACES/faces_data/" + str(j) + "/" + str(j) +"_desc.nt", "r", encoding="utf-8") as file:
        for line in file:
            triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
            if triple_match:
                subject = triple_match.group(1)
                predicate = triple_match.group(2)
                object_ = triple_match.group(3)
                uri = '<' + subject + '> <' + predicate + '> ' + object_
                val = 0.0
                uris.append((uri, val))

    uris_array = np.array(uris, dtype=[('uri', 'U1000'), ('value', float)])
  
    object_counts = Counter([obj for obj, _ in top_objects])
    final_weight = np.array([], dtype=final_weight.dtype)  
    
    tr=0
    #print(len(uris),len(top_objects), len(top_predicates), len(top_predicates1),len(top_predicates4),j)
    for (uri,val),(object_uri1, value1),(object_uri3, value3),(object_uri4, value4) in zip(uris,top_objects,top_predicates1,top_predicates4):
        if object_uri1.strip() == '""' :
            tr = 0.0
            tr2 = 0.0
            tp=0.0
        elif  'http://www.w3.org/2002/07/owl#Thing' in object_uri1   :
            tr =0.0 
            tr2 = 0.0
            tp=0.0
        elif      'thumbnail' in object_uri3  :                    
            
            tr =0.0
            tr2 = 0.0
            tp=0.0
        else:
            tr=value3
            tr2 = value4
            tp=value1
        temp = tp+ tr2
        temp1 = tp+  tr2
        
        if object_counts[object_uri1]>1:
            for x in range(len(top_objects)):
                if object_uri1 == top_objects[x][0] and object_uri4!=top_predicates4[x][1]:#tsekarw an ta object einai idia
                   # print( object_uri1,temp1, top_objects[x][1]+top_predicates4[x][1]) 
                    if temp1 < top_objects[x][1]+top_predicates4[x][1]:
                        print( object_uri1,temp1)
                        temp = 0.0
                        
                    elif temp1 == top_objects[x][1]+top_predicates4[x][1]:
                        
                        top_objects[x][1]=0
                        top_predicates4[x][1] =0
                        temp = temp1
                    else:
                        temp = temp1
                       # print( object_uri1,temp1)
                        
                    
       
        final_weight = np.append(final_weight, np.array([(uri, temp)], dtype=final_weight.dtype))

 
    with open("C:/Program Files/Git/eval/summ_examplefaces/faces/" + str(j) + "/" + str(j) +"_rank.nt", "w", encoding="utf-8") as output_file:

        final_weight_sorted = np.sort(final_weight, order='value')[::-1]
        print(final_weight_sorted)
        for triple, _ in final_weight_sorted:
            output_file.write(f"{triple}.\n")
    #print(final_weight_sorted)
    with open("C:/Program Files/Git/eval/summ_examplefaces/faces/" + str(j) + "/" + str(j) +"_top5.nt", "w", encoding="utf-8") as output_file:

        top_5_objects = [object_uri for object_uri, _ in final_weight_sorted[:5]]
        for triple, _ in final_weight_sorted[:5]:
            output_file.write(f"{triple}.\n")
            
    with open("C:/Program Files/Git/eval/summ_examplefaces/faces/" + str(j) + "/" + str(j) +"_top10.nt", "w", encoding="utf-8") as output_file:

        top_5_objects = [object_uri for object_uri, _ in final_weight_sorted[:top]]
        for triple, _ in final_weight_sorted[:top]:
            output_file.write(f"{triple}.\n")

        
    
    fold=0
    total1=0
    while fold < 6:
        golden_standard_triples = set()
        if j==38 and fold==4:#gia tpo 10
            break
        if j==50 and fold==5:#gia tpo 10
            break
        #    fold+=1
         #   print(j)
        with open("C:/Users/gtrouli/Desktop/src/data/FACES/faces_data/" + str(j) + "/" + str(j) +"_gold_top"+str(top)+"_"+ str(fold)+".nt", "r", encoding="utf-8") as file:
            for line in file:
                triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                if triple_match:
                    subject = triple_match.group(1)
                    predicate = triple_match.group(2)
                    object_ = triple_match.group(3)
                 
                    golden_standard_triples.add('<'+subject+'> <'+predicate+'> '+object_)
        
        #print(top_5_objects)
        
        true_positives = len(set(top_5_objects) & golden_standard_triples)
        false_positives = len(set(top_5_objects) - golden_standard_triples)
        false_negatives = len(golden_standard_triples - set(top_5_objects))
        
        precision = true_positives / (true_positives + false_positives)
        
        recall = true_positives / (true_positives + false_negatives)
        
        if precision + recall == 0:
            f_measure = 0
        else:
            f_measure = 2 * (precision * recall) / (precision + recall)
        
       # print(fold,': ', f_measure)
        total1 += f_measure
        fold += 1
        
  
    total+=(total1/6)
    #print ( j,   total1/6)

    j += 1
print('total F-measure:', total / 50)
