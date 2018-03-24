# -*- coding: utf-8 -*-
"""
Eclat Algorithm
"""
# Author: Nikolay Bashlykov <bashnick@gmail.com>
# License: GNU GPL

import numpy as np

class Eclat:
    def __init__(self, min_support = 5, max_items = 5, min_items = 2):
        self.min_support = min_support
        self.max_items = max_items
        self.min_items = min_items
        self.item_lst = list()
        self.item_len = 0
        self.item_dict = dict()
        self.final_dict = dict()
    
    def read_data(self, dataset):
        for index, row in dataset.iterrows():
            row_wo_na = row.dropna().unique()
            for item in row_wo_na:
                item = item.strip()
                if item in self.item_dict:
                    self.item_dict[item][0] += 1
                else:
                    self.item_dict.setdefault(item, []).append(1)
                self.item_dict[item].append(index) #later a more sofisticated data structure can be used to search more efficient
        #set instance variables
        self.item_lst = list(self.item_dict.keys())
        self.item_len = len(self.item_lst)
        
    def recur_eclat(self, item_name, tids_array, minsupp, num_items, k_start):
        if tids_array[0] >= minsupp and num_items <= self.max_items:
            for k in range(k_start+1, self.item_len):
                if self.item_dict[self.item_lst[k]][0] >= minsupp:
                    new_item = item_name + " | " + self.item_lst[k]
                    new_tids = np.intersect1d(tids_array[1:], self.item_dict[self.item_lst[k]][1:])
                    new_tids_size = new_tids.size
                    new_tids = np.insert(new_tids, 0, new_tids_size)
                    if new_tids_size >= minsupp:
                        if num_items >= self.min_items: self.final_dict.update({new_item: new_tids})
                        self.recur_eclat(new_item, new_tids, minsupp, num_items+1, k)
        
    def fit(self, dataset):
        i = 0
        self.read_data(dataset)
        for w in self.item_lst:
            self.recur_eclat(w, self.item_dict[w], self.min_support, 2, i)
            i+=1
        return self
        
    def transform(self):
        return {k: v[0] for k, v in self.final_dict.items()}    