# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:13:09 2024

@author: gtrouli
"""
import numpy as np
import re
from collections import Counter, defaultdict
import math
from collections import defaultdict


def calculate_redundancy_score(triples):
    """
    Calculates redundancy score for a set of triples.
    Score = ratio of unique (subject, object) pairs over total.
    """
    subject_object_pairs = []
    
    for triple in triples:
        triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)', triple)
        if triple_match:
            subject = triple_match.group(1)
            object_ = triple_match.group(3).strip().rstrip('.')
            object_clean = re.sub(r'("@[a-z]+)?$', '', object_.strip('"'))
            subject_object_pairs.append((subject, object_clean))
    
    """
    seen = set()
    duplicates = set()
    for pair in subject_object_pairs:
        if pair in seen:
            duplicates.add(pair)
        else:
            seen.add(pair)
    
    for d_pair in duplicates:
        print(d_pair)
    """
    total_pairs = len(subject_object_pairs)
    unique_pairs = len(set(subject_object_pairs))
    
    if total_pairs == 0:
        return 1.0  
    return unique_pairs / total_pairs



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
        t = algo_rank[pos - 1]
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

def evaluation(approach, output_filename):
    
    total = 0
    
    total_ndcg10=0
    total_ndcg5=0
    total_1= 0
    total_map10=0
    total_map5=0
    total_redundancy5 = 0
    total_redundancy10 = 0
 
    
    if   approach =='linksum'or approach =='relin':
      totalranking='_rank_top10.nt'
    elif approach =='cd':
      totalranking='_top10.nt'
    else:
      totalranking='_rank.nt'
    
    
    j = 1
    while j < 101:
       
       if j == 101:
           j = 141
       totalrank_ordered = []
       rank = set()
       top_10= set()  
       top_5= set() 
       totalrank=set()
      
       with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/runs/"+str(approach)+"/dbpedia/" + str(j) + "/" + str(j) +"_top5.nt", "r", encoding="utf-8") as input_file1:
                   
           for line in input_file1:
                    triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                    if triple_match: 
                        subject = triple_match.group(1)
                        predicate = triple_match.group(2)
                        object_ = triple_match.group(3)
                     
                        top_5.add(str('<'+subject+'> <'+predicate+'> '+object_))
          
                      
                #summ_example1
       with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/runs/"+str(approach)+"/dbpedia/" + str(j) + "/" + str(j) +"_top10.nt", "r", encoding="utf-8") as input_file2:
            for line in input_file2:
                    triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                    if triple_match:
                        subject = triple_match.group(1)
                        
                        predicate = triple_match.group(2)
                        object_ = triple_match.group(3)                
                        top_10.add(str('<'+subject+'> <'+predicate+'> '+object_))
                                                                                                               
       with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/runs/"+str(approach)+"/dbpedia/" + str(j) + "/" + str(j) +totalranking, "r", encoding="utf-8") as input_file3:
            for line in input_file3:
                triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                if triple_match:
                    subject = triple_match.group(1)
                    
                    predicate = triple_match.group(2)
                    object_ = triple_match.group(3)
                    totalrank_ordered.append(str('<'+subject+'> <'+predicate+'> '+object_))
    #==========================================================top5==========================================================================  
            
       top = 5 
    
       fold=0
       total1=0
       total5_map=0
       temp_precision=0
       gold_summaries_for_ndcg5=[]
       while fold < 6:
            golden_standard_triples = set()
            golden_standard_triplesmap=[]
            current_fold_gold_triples5=[]
            with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/data/ESBM_benchmark_v1.0/dbpedia_data/" + str(j) + "/" + str(j) +"_gold_top"+str(top)+"_"+ str(fold)+".nt", "r", encoding="utf-8") as file:
                for line in file:
                    triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                    if triple_match:
                        subject = triple_match.group(1)
                        predicate = triple_match.group(2)
                        object_ = triple_match.group(3)
                     
                        golden_standard_triples.add(str('<'+subject+'> <'+predicate+'> '+object_))
                        golden_standard_triplesmap.append(str('<'+subject+'> <'+predicate+'> '+object_))
                        current_fold_gold_triples5.append(str('<'+subject+'> <'+predicate+'> '+object_))
        
            gold_summaries_for_ndcg5.append(current_fold_gold_triples5)
    
                 
            true_positives = len(set(top_5) & golden_standard_triples)
            false_positives = len(set(top_5) - golden_standard_triples)
            false_negatives = len(golden_standard_triples - set(top_5))
       
            precision = true_positives / (true_positives + false_positives)
                   
            recall = true_positives / (true_positives + false_negatives)
    
            
            if precision + recall == 0:
                f_measure = 0
            else:
                f_measure = 2 * (precision * recall) / (precision + recall)
            temp_precision+= precision
    
            total1 += f_measure
    
           # --- map ---
            ap = 0.0
            relevant_count = 0
            for k, retrieved_item in enumerate(totalrank_ordered,start=1): 
               # print(retrieved_item)
                #print(golden_standard_triplesmap)
                if retrieved_item in golden_standard_triplesmap:
                    relevant_count += 1
                    precision_at_k = relevant_count / k
                    ap += precision_at_k
            
            num_relevant_items_in_golden = len(golden_standard_triplesmap)
            if num_relevant_items_in_golden > 0:
                ap /= num_relevant_items_in_golden
            else:
                ap = 0.0  
            total5_map += ap
            
    
            
            fold += 1
      
       ndcg5_current_loop5 = get_graded_ndcg(gold_summaries_for_ndcg5, totalrank_ordered)
       total_ndcg5 += ndcg5_current_loop5    
       redundancy5 = calculate_redundancy_score(top_5)
       total_redundancy5 += redundancy5  
      
       total+=(total1/6)
       total_map5+=(total5_map/6)
    
         
    #==========================================================top10==========================================================================
        
       top1 = 10
       gold_summaries_for_ndcg = []  
       fold1 = 0
       total2 = 0
       total10_map = 0
        
       while fold1 < 6:
            golden_standard_triples = set()
            golden_standard_triplesmap = []
            current_fold_gold_triples = []
        
            with open("C:/Users/gtrouli/Desktop/src/EntitySum-main/data/ESBM_benchmark_v1.0/dbpedia_data/" + str(j) + "/" + str(j) + "_gold_top" + str(top1) + "_" + str(fold1) + ".nt", "r", encoding="utf-8") as file:
                for line in file:
                    triple_match = re.match(r'<(.+?)>\s+<(.+?)>\s+(.+)\s*\.', line)
                    if triple_match:
                        subject = triple_match.group(1)
                        predicate = triple_match.group(2)
                        object_ = triple_match.group(3)
        
                        triple_str = f'<{subject}> <{predicate}> {object_}'
                        golden_standard_triples.add(triple_str)
                        golden_standard_triplesmap.append(triple_str)
                        current_fold_gold_triples.append(triple_str)
        
            gold_summaries_for_ndcg.append(current_fold_gold_triples)
        
            # F-measure calculation
            true_positives = len(top_10 & golden_standard_triples)
            false_positives = len(top_10 - golden_standard_triples)
            false_negatives = len(golden_standard_triples - top_10)
        
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        
            f_measure = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            total2 += f_measure
        
            # MAP Calculation
            ap = 0.0
            relevant_count = 0
            for k, retrieved_item in enumerate(totalrank_ordered, start=1):
                if retrieved_item in golden_standard_triplesmap:
                    relevant_count += 1
                    precision_at_k = relevant_count / k
                    ap += precision_at_k
        
            num_relevant_items_in_golden = len(golden_standard_triplesmap)
            ap = ap / num_relevant_items_in_golden if num_relevant_items_in_golden > 0 else 0.0
            total10_map += ap
        
            fold1 += 1
        
       ndcg10_current_loop = get_graded_ndcg(gold_summaries_for_ndcg, totalrank_ordered)
       total_ndcg10 += ndcg10_current_loop
       redundancy10 = calculate_redundancy_score(top_10)
       total_redundancy10 += redundancy10
       total_1 += total2 / 6
       total_map10 += total10_map / 6
        
    
    
       j += 1
    
    print (approach,'DBPEDIA(v1.0)')
    print(f'total F-measure(top5): {total / 100}')
    print(f'total F-measure(top10): {total_1 / 100}')
    
    print('total MAP(top5): ',total_map5 / 100)
    print('total MAP(top10): ',total_map10 / 100)
    
    print('total NDCG(top5): ',total_ndcg5 / 100)
    print('total NDCG(top10): ',total_ndcg10 / 100)
    
    print("Average Redundancy(top5): ", 1-(total_redundancy5 / 100))
    print("Average Redundancy(top10): ", 1-(total_redundancy10 / 100))
    print('-----------------------------')
    
    
    content = (
            f"{approach} DBPEDIA(v1.0)\n"
            f"total F-measure(top5): {total / 100}\n"
            f"total F-measure(top10): {total_1 / 100}\n"
            f"total MAP(top5): {total_map5 / 100}\n"
            f"total MAP(top10): {total_map10 / 100}\n"
            f"total NDCG(top5): {total_ndcg5 / 100}\n"
            f"total NDCG(top10): {total_ndcg10 / 100}\n"
            f"Average Redundancy(top5): {1 - (total_redundancy5 / 100)}\n"
            f"Average Redundancy(top10): {1 - (total_redundancy10 / 100)}\n"
            "-----------------------------\n"
        )
    
    with open(output_filename, 'a') as outfile:
        outfile.write(content)
    
#evaluation('degree')