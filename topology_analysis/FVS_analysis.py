# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:26:02 2019

@author: jwKim
"""
import copy


def conversion_of_combination_num_to_list_of_comb(i_num_of_combination, i_sum_selfloopnodes):
    """get a list having position numbers of 1s of binary form i_num_of_combination
    if position of 1 is duplicated to the position of 1 in i_sum_selfloopnodes, don't contain that
    example: i_num_of_combination=26=11010(bin), i_sum_selfloopnodes = 0 -> [1,3,4]
    i_num_of_combination=26=11010(bin), i_sum_selfloopnodes = 8=1000(bin) -> [1,4]"""
    l_list_of_comb = []
    i_position = 0
    while i_num_of_combination:
        if i_num_of_combination%2 == 1:
            l_list_of_comb.append(i_position)
        i_position+=1
        i_num_of_combination = i_num_of_combination>>1
    
    for i,i_node in reversed(list(enumerate(l_list_of_comb))):
        if int(i_sum_selfloopnodes/pow(2,i_node))%2:
            l_list_of_comb.pop(i)
    
    return l_list_of_comb


def check_acyclic_form(l_node_data, lt_links_data):
    """checking whether the network is acylic or not.
    if acyclic, return True, else False
    lt_links_data=[(start_node,end_node),,,]"""
    l_tmp_node_data = l_node_data.copy()
    lt_tmp_links_data = lt_links_data.copy()
    while l_tmp_node_data:
        flownode = l_tmp_node_data.pop(0)
        l_flow_of_node = [flownode]
        while l_flow_of_node:
            flownode = l_flow_of_node[-1]
            for i in range(len(lt_tmp_links_data)-1,-1,-1):
                if lt_tmp_links_data[i][0] == flownode:
                    nextnode = lt_tmp_links_data[i][1]
                    lt_tmp_links_data.pop(i)
                    if nextnode in l_flow_of_node:
                        return False
                        #not FVS!!
                    elif nextnode in l_tmp_node_data:
                        l_flow_of_node.append(nextnode)
                        l_tmp_node_data.pop(l_tmp_node_data.index(nextnode))
                        break
            else:
                l_flow_of_node.pop(-1)
    return True


def check_acyclic_form2(l_node_data, dic_startnode_set_links):
    """checking whether the network is acylic or not.
    if acyclic, return True, else False
    dic_startnode_set_links={start_node:set((startnode,endnode1),(startnode,endnode2),,,)}
    nodes of links in dic_startnode_set_links should be in l_node_data"""
    l_tmp_node_data = l_node_data.copy()
    dic_tmp_startnode_set_links = copy.deepcopy(dic_startnode_set_links)
    while l_tmp_node_data:
        flownode = l_tmp_node_data.pop(0)
        l_flow_of_node = [flownode]
        while l_flow_of_node:
            flownode = l_flow_of_node[-1]
            if dic_tmp_startnode_set_links[flownode]:
                nextnode = dic_tmp_startnode_set_links[flownode].pop()[1]
                if nextnode in l_flow_of_node:
                    return False
                    #not FVS!!
                elif nextnode in l_tmp_node_data:
                    l_flow_of_node.append(nextnode)
                    l_tmp_node_data.pop(l_tmp_node_data.index(nextnode))
            else:
                l_flow_of_node.pop(-1)
    return True


def calculate_next_combination(x,n):
    """
    for integer x, return integer iNext
    when x is described by binary form, x has i number of 1s.
    iNext is the smallest integer which is bigger than x and can be described by binary form using i number of 1s.
    if integer satisfying conditions is bigger than (2^n)-1, then iNext is the integer which can be described by binary form using i+1 num of 1s.
    for example, x = 100, x == 1100100(2). then iNext == 1101000(2) == 104
    """
    if n == 0:
        return False
    if x == 0:
        return(1)
 
    i_position_of_smallest_1 = 0
    i_position_of_smallest_0_after_first_1 = 0
    i_next = x
 
    while x%2 == 0:
        i_position_of_smallest_1 += 1
        x = x >> 1
    x = x >> 1
 
    while x%2 == 1:
        x = x >> 1
        i_next += pow(2,i_position_of_smallest_0_after_first_1) 
        i_next -= pow(2,i_position_of_smallest_1+i_position_of_smallest_0_after_first_1)
        i_position_of_smallest_0_after_first_1 += 1
 
    if i_position_of_smallest_0_after_first_1 == n-1:
        #"every combinations are found"
        return False
    elif i_position_of_smallest_0_after_first_1 > n-1:
        #"it is over the combination range"
        return False
 
    if i_position_of_smallest_1 + i_position_of_smallest_0_after_first_1 == n-1:
        #"one combination ended"
        i_next += pow(2,i_position_of_smallest_0_after_first_1) 
        i_next += pow(2,i_position_of_smallest_0_after_first_1 +1) 
        i_next -= pow(2,i_position_of_smallest_1+i_position_of_smallest_0_after_first_1)
    else:
        i_next -= pow(2,i_position_of_smallest_1+i_position_of_smallest_0_after_first_1) 
        i_next += pow(2,i_position_of_smallest_1+i_position_of_smallest_0_after_first_1+1)

    """
    #test code
    z=iNext
    k = ''
    while z:
        k+=str(z%2)
        z=z>>1
    print(k)
    """
    return i_next

def get_combination_nodes_list(i_combination, l_selflooplessnodes):
    i_position = 0
    l_list_of_comb = []
    while i_combination:
        if i_combination%2 == 1:
            l_list_of_comb.append(i_position)
        i_position+=1
        i_combination = i_combination>>1
    l_nodes_selected = [l_selflooplessnodes[i] for i in l_list_of_comb]
    
    return l_nodes_selected


def FVS_finding_basic(l_nodes_data, lt_links_data, i_combination_start = 0, s_filename_count = None):
    """
    nodes data = [node name1, node name2, ..... node name k] node name should be string
    interaction data = [(node1, node2), (node1, node3)...] 
    (node1, node2) means node1 interacte to node2 i.e. node1 -> node2
    to release the complexity, put SCC network. of course, non SCC network can be analyzed
    """

    li_combinations_making_FVS = []
    
    i_num_of_nodes = len(l_nodes_data)
    li_nodes_data = list(range(i_num_of_nodes))
    dic_name_position = {s_name:i for i,s_name in enumerate(l_nodes_data)}
    dic_i_startnode_settlinks = {}
    for ts_link in lt_links_data:
        ti_link = (dic_name_position[ts_link[0]], dic_name_position[ts_link[1]])
        dic_i_startnode_settlinks.setdefault(ti_link[0],set([])).add(ti_link)
        
    i_len_mFVS = i_num_of_nodes#after getting first mFVS, this value will be changed
    
    i_count_call = 1 #the number of calculated combinations
    i_reporting_number = 10000 

    seti_selfloopnodes =set([])
    for t_link in lt_links_data:
        if t_link[0] == t_link[1]:
            #"self loop! be careful when one node has more than two self loop"
            seti_selfloopnodes.add(dic_i_startnode_settlinks[t_link[0]])
            
    li_selflooplessnodes = list(set(li_nodes_data).difference(seti_selfloopnodes))
    li_selfloopnodes = list(seti_selfloopnodes)
    i_num_of_selfloopless_nodes = i_num_of_nodes - len(seti_selfloopnodes)
    #"self loop finding"

    b_combinationflag = True
    i_combination = i_combination_start
    
    while b_combinationflag:
        li_list_of_comb = get_combination_nodes_list(i_combination, li_selflooplessnodes) + li_selfloopnodes
        if len(li_list_of_comb) > i_len_mFVS:
            break
        
        li_nodes_except_combination = list(set(li_nodes_data).difference(set(li_list_of_comb)))
        lt_tmp_links_data = []
        for i_node in li_nodes_except_combination:
            for ti_link in dic_i_startnode_settlinks[i_node]:
                if ti_link[1] in li_nodes_except_combination:
                    lt_tmp_links_data.append(ti_link)

        if check_acyclic_form(li_nodes_except_combination, lt_tmp_links_data):
            li_combinations_making_FVS.append(i_combination)
            print("combination "+str(i_combination)+" is FVS")
            if len(li_combinations_making_FVS) == 1:
                i_len_mFVS = len(li_list_of_comb)

        i_combination = calculate_next_combination(i_combination,i_num_of_selfloopless_nodes)
        b_combinationflag = i_combination#calculate_next_combination returns False when all possible combinations ends

        if i_count_call%i_reporting_number == 0:#midpoint saving
            if s_filename_count != None:
                with open(s_filename_count,'w') as file_counts:
                    file_counts.write(str(i_count_call)+"th calculation ended. next combination is "+str(i_combination))
            print(str(i_count_call)+"th calculation ended. next combination is "+str(i_combination))
        i_count_call += 1
        

    lli_FVS_nodes = list(map(lambda x: get_combination_nodes_list(x, li_selflooplessnodes), li_combinations_making_FVS))
    ll_FVS = []
    for li_FVS_nodes in lli_FVS_nodes:
        l_FVS = list(map(lambda x: l_nodes_data[x],li_FVS_nodes))+[l_nodes_data[i] for i in li_selfloopnodes]
        ll_FVS.append(l_FVS)

    return(ll_FVS)