# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:45:55 2019

@author: jwKim
"""
import copy

def convert_net_topology_from_basic_to_matrix(ls_nodes, lt_links):
    """convert [s_node1, s_node2,,,] and [(startnode, endnode),,,] form to 
    matrix A such that Aij = 1 means (jth node, ith node) link exist"""
    ll_matrix = []
    lt_tmp_links = copy.deepcopy(lt_links)
    i_num_of_nodes = len(ls_nodes)
    for i, s_node in enumerate(ls_nodes):
        ll_matrix.append([0]*i_num_of_nodes)
        for k in range(len(lt_tmp_links)-1, -1, -1):
            if lt_tmp_links[k][1] == s_node:
                s_startnode = lt_tmp_links.pop(k)[0]
                ll_matrix[i][ls_nodes.index(s_startnode)] += 1
    
    return ll_matrix

def find_input_nodes(ls_nodes, lt_links):
    """find input nodes and return the node names as list"""
    sets_nodes_not_input = set([])
    for t_link in lt_links:
        sets_nodes_not_input.add(t_link[1])
    
    sets_nodes_input = set(ls_nodes).difference(sets_nodes_not_input)
    return list(sets_nodes_input)