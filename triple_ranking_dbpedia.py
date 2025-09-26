import numpy as np
import re
from collections import Counter, defaultdict
import math

def get_graded_ndcg(gold_summaries, algo_rank):
    triple_grade = {}
    for gold_sum in gold_summaries: 
        for t in gold_sum:         
            triple_grade[t] = triple_grade.get(t, 0) + 1 

    grade_list = sorted(triple_grade.values(), reverse=True) 

    dcg = 0.0
    idcg = 0.0
    max_rank_pos = len(algo_rank)
    max_ideal_pos = len(grade_list) 

    for pos in range(1, max_rank_pos + 1):
        t = algo_rank[pos - 1]['uri']
        rel = triple_grade.get(t, 0) 
        dcg_item = rel / (math.log(pos + 1) / math.log(2))
        dcg += dcg_item

        if pos <= max_ideal_pos:
            idea_rel = grade_list[pos - 1]
            idcg += idea_rel / (math.log(pos + 1) / math.log(2))

    if idcg == 0:
        return 0.0
    ndcg = dcg / idcg
    return ndcg

def triple_ranking_dbpedia(measure,prop_measure):
    total_ndcg10=0
    total = 0
    total_map=0
    top = 10
    
    if 'Context' in prop_measure:
        prop_folder='properties/properties_'   
    elif 'Dataset' in prop_measure:
        prop_folder='properties/properties'
    
    
    
    j = 1
    
    while j < 166:
       
        if j == 101:
            j = 141
            
        
        top_objects = np.array([], dtype=[('object_uri', '<U100'), ('value', float)])  
        top_predicates4 = np.array([], dtype=[('object_uri', '<U100'), ('value', float)]) 
        uris = []
        final_weight = np.empty(0, dtype=[('uri', 'U1000'), ('value', float)])
    
    
        with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/centrality_measures/ESBM/DBPEDIA/" + str(measure) + "/" + str(measure) + "_" + str(j) + ".txt", "r", encoding="utf-8", errors="ignore") as file:
           
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split("\t")
                    if len(parts) < 2:
                        object_uri = " "
                        value1 = 0.0 
                       #=============================hits===================================================================
                    if len(parts) == 3:
                        object_uri = parts[0]
                        value1 = float(parts[1]) if parts[1] != "Key not found" else 0.0
                        value2 = float(parts[2]) if parts[2] != "Key not found" else 0.0
                        if object_uri=='""'  :
                            value1 = 0.0
                            value2 = 0.0
                        top_objects = np.append(top_objects, np.array([(object_uri, value1+value2)], dtype=top_objects.dtype))
                        #========================================================================================================
                    else:
                        object_uri = parts[0]          
                        value1 = float(parts[1]) if parts[1] != "Key not found" else 0.0
                        top_objects = np.append(top_objects, np.array([(object_uri, value1)], dtype=top_objects.dtype))
                   
        
        with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/centrality_measures/ESBM/DBPEDIA/"+ str(prop_folder) + str(j) + ".txt", "r", encoding="utf-8", errors="ignore") as file4:
            for line in file4:
                line = line.strip()
                if line:
                    parts4 = line.split("\t")
                if len(parts4) >= 2:  
                    object_uri4 = parts4[0]
                    if object_uri4!="":
                        if 'Infrequent' in prop_measure:
                             value4 = 1/float(parts4[1]) 
                        elif 'Frequent' in prop_measure:
                            value4 = float(parts4[1])  
                    else:  
                        value4 = 0.0
                    top_predicates4 = np.append(top_predicates4, np.array([(object_uri4, value4)], dtype=top_predicates4.dtype))
                else:
                    value4 = 0.0
      
       
        max_value_objects = np.max(top_objects['value'])
        max_value_predicates4 = np.max(top_predicates4['value'])
    
        top_objects['value'] /= max_value_objects
        top_predicates4['value'] /= max_value_predicates4
    

        with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/data/ESBM_benchmark_v1.2/dbpedia_data/" + str(j) + "/" + str(j) +"_desc.nt", "r", encoding="utf-8") as file:
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
        for (uri,val),(object_uri1, value1),(object_uri4, value4) in zip(uris,top_objects,top_predicates4):
            
            if object_uri1.strip() == '""' :
              
                tr2 = 0.0
                tp=0.0
            elif  'http://www.w3.org/2002/07/owl#Thing' in object_uri1   :
             
                tr2 = 0.0
                tp=0.0
            elif      'thumbnail' in object_uri4  :                    
                
                
                tr2 = 0.0
                tp=0.0
            else:
              
                tr2 = value4
                tp=value1
            temp = tp+ tr2
            temp1 = tp+  tr2
            
            
            if object_counts[object_uri1]>1:
                for x in range(len(top_objects)):
                    if object_uri1 == top_objects[x][0] and object_uri4!=top_predicates4[x][1]:#tsekarw an ta object einai idia
                        
                       # print( object_uri1,temp1, top_objects[x][1]+top_predicates4[x][1]) 
                        if temp1 < top_objects[x][1]+top_predicates4[x][1]:
                            #print( object_uri1,temp1)#typwnw ta idia
                            temp = 0.0
                         #   print(object_uri1,temp,temp1)
                        elif temp1 == top_objects[x][1]+top_predicates4[x][1]:
                            #print(object_uri1,temp1)
                            top_objects[x][1]=0
                            top_predicates4[x][1] =0
                            temp = temp1
                        else:
                            temp = temp1
                            top_objects[x][1]=0
                            top_predicates4[x][1] =0
                            
                           
                            #print( object_uri1,temp1)
                            
                        
           
            final_weight = np.append(final_weight, np.array([(uri, temp)], dtype=final_weight.dtype))
    
     
        with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/runs/"+ str(measure) +"/dbpedia/" + str(j) + "/" + str(j) +"_rank.nt", "w", encoding="utf-8") as output_file:
    
            final_weight_sorted = np.sort(final_weight, order='value')[::-1]
           # print(final_weight_sorted)gia na dw ta triples
            for triple, _ in final_weight_sorted:
                output_file.write(f"{triple}.\n")
        #print(final_weight_sorted)
        with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/runs/"+ str(measure) +"/dbpedia/" + str(j) + "/" + str(j) +"_top5.nt", "w", encoding="utf-8") as output_file:
    
            top_5_objects = [object_uri for object_uri, _ in final_weight_sorted[:5]]
            for triple, _ in final_weight_sorted[:5]:
                output_file.write(f"{triple}.\n")
                
        with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/runs/"+ str(measure) +"/dbpedia/" + str(j) + "/" + str(j) +"_top10.nt", "w", encoding="utf-8") as output_file:
    
            top_5_objects = [object_uri for object_uri, _ in final_weight_sorted[:top]]
            top_objects_all=[object_uri for object_uri, _ in final_weight_sorted[:125]]
            for triple, _ in final_weight_sorted[:top]:
                output_file.write(f"{triple}.\n")
    
         #====================================evaluation==================================================   
        """
        fold=0
        total1=0
        total1_map=0
        total1_map_new=0
        total1recall = 0
        total1prec = 0
        gold_summaries_for_ndcg = []  
        while fold < 6:
            golden_standard_triples = set()
            current_fold_gold_triples = []
     
            with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/data/ESBM_benchmark_v1.2/dbpedia_data/" + str(j) + "/" + str(j) +"_gold_top"+str(top)+"_"+ str(fold)+".nt", "r", encoding="utf-8") as file:
                for line in file:
                    triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                    if triple_match:
                        subject = triple_match.group(1)
                        predicate = triple_match.group(2)
                        object_ = triple_match.group(3)
                     
                        golden_standard_triples.add(str('<'+subject+'> <'+predicate+'> '+object_))
                        current_fold_gold_triples.append(str('<'+subject+'> <'+predicate+'> '+object_))
        
            gold_summaries_for_ndcg.append(current_fold_gold_triples)
            
            
            
            true_positives = len(set(top_5_objects) & golden_standard_triples)
            false_positives = len(set(top_5_objects) - golden_standard_triples)
            false_negatives = len(golden_standard_triples - set(top_5_objects))
            
            precision = true_positives / (true_positives + false_positives)
            total1prec += precision      
            
            recall = true_positives / (true_positives + false_negatives)
            total1recall += recall
              
            if precision + recall == 0:
                f_measure = 0
            else:
                f_measure = 2 * (precision * recall) / (precision + recall)
            
            total1 += f_measure
            
            # --- map ---
            ap = 0.0
            relevant_count = 0
            for k, (retrieved_item, _) in enumerate(final_weight_sorted, start=1):  
    
                if retrieved_item in golden_standard_triples:
                    relevant_count += 1
                    precision_at_k = relevant_count / k
                    ap += precision_at_k
            
            num_relevant_items_in_golden = len(golden_standard_triples)
            if num_relevant_items_in_golden > 0:
                ap /= num_relevant_items_in_golden
            else:
                ap = 0.0 
            
            total1_map += ap	
            
            fold += 1
            
        # --- ndcg ---    
        ndcg10_current_loop = get_graded_ndcg(gold_summaries_for_ndcg, final_weight_sorted)
        
        total_ndcg10 += ndcg10_current_loop
        total+=(total1/6)
        total_map+=(total1_map/6)
        """
        j += 1
   # print('total F-measure:', total / 125)
   # print('total MAP: ',total_map / 125)
   # print('total NDCG(top10): ',total_ndcg10 / 125)

#triple_ranking_dbpedia('radiality','InfrequentPropertiesContext')
