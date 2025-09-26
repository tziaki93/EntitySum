# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 14:25:10 2025

@author: gtrouli
"""
    
import centrality_measures.centrality_meas_dbpedia
import centrality_measures.centrality_meas_lmdb

import properties.PropertiesContext
import properties.PropertiesDataset
import properties.PropertiesDataset_1

import triple_ranking_dbpedia
import triple_ranking_lmdb

import evaluation.fmeas_map_ndcg_dbpedia1_0
import evaluation.fmeas_map_ndcg_dbpedia1_2
import evaluation.fmeas_map_ndcg_lmdb1_0
import evaluation.fmeas_map_ndcg_lmdb1_2



def main():

    output_filename = 'results.txt'
    datasets=['dbpedia','lmdb']
    obj_measures=['degree', 'pagerank', 'hits', 'radiality', 'betweeness']
    prop_categories=['PropertiesDataset','PropertiesContext']
    prop_measures=['FrequentPropertiesDataset','InfrequentPropertiesDataset','FrequentPropertiesContext','InfrequentPropertiesContext']

    """ 
    #Uncomment only if you want to compute the important measures from scratch
    #calculate object's importance
    for obj_measure in obj_measures:
        print("Generating weights for objects for dbpedia using",obj_measure,'measure')
        centrality_measures.centrality_meas_dbpedia.generate_centrality_measures_dbpedia(obj_measure)
        print("Generating weights for objects for lmdb using",obj_measure,'measure')
        centrality_measures.centrality_meas_lmdb.generate_centrality_measures_lmdb(obj_measure)
    """          
    #calculate property's importance
    for prop_category in prop_categories:
        for dataset in datasets:      
            if prop_category=='PropertiesContext':
                print("Generating weights for properties within Entity's context for ", dataset)
                properties.PropertiesContext.propertiesContext(dataset)
            elif prop_category=='PropertiesDataset':
                print("Generating weights for properties within dataset for ", dataset)
                properties.PropertiesDataset.propertiesDataset(dataset)
                properties.PropertiesDataset_1.propertiesDataset_1(dataset)
    print("-----------------------------\n")
              
    
    # EntitySum
    for prop_measure in prop_measures:
        content = (f"Property Method: {prop_measure}\n-----------------------------\n")
        print(content)
        with open(output_filename, 'a') as outfile:
                outfile.write(content)
        for obj_measure in obj_measures:
             triple_ranking_dbpedia.triple_ranking_dbpedia(obj_measure,prop_measure)
             triple_ranking_lmdb.triple_ranking_lmdb(obj_measure,prop_measure)

           #Evaluation and Comparison    
             evaluation.fmeas_map_ndcg_dbpedia1_0.evaluation(obj_measure, output_filename )
             evaluation.fmeas_map_ndcg_dbpedia1_2.evaluation(obj_measure, output_filename)
             evaluation.fmeas_map_ndcg_lmdb1_0.evaluation(obj_measure, output_filename)
             evaluation.fmeas_map_ndcg_lmdb1_2.evaluation(obj_measure, output_filename)
     


if __name__ == "__main__":
    main()