def Clique_Percolation(G, most_valualble_edge=None):
        cliques_list = []
        for k in range(3, G.number_of_nodes()):
            communities = list(nxalgo.k_clique_communities(G, k))
            if len(communities) == 0:  # stop when there are no more communities with k
                break
            cliques_list.append((k, communities))
        max_mod = (0, 0)
        for clique in cliques_list:
            mod = 0
            for comm in clique[1]:
                total_links_inside = 0
                adj_calc = 0
                if len(comm) == 1:  # in case there is only one node inside a community its modularity is 0
                    mod += 0
                else:
                    for node in comm:
                        num_clusters_belongs_to = 0
                        for comm_check in clique[1]:
                            if node in comm_check:
                                num_clusters_belongs_to += 1
                        in_size = 0
                        out_size = 0
                        node_deg = G.degree(node)
                        neighbor_list_for_calc = list(nx.neighbors(G, node))
                        for neighbor in neighbor_list_for_calc:
                            if neighbor in comm:
                                in_size += 1
                                total_links_inside += 1
                            else:
                                out_size += 1
                        adj_calc += (in_size - out_size) / (node_deg * num_clusters_belongs_to)
                    mod += (1 / len(comm)) * adj_calc * (total_links_inside / 2) / special.binom(len(comm), 2)
            absent_nodes = 0
            absent_nodes_names = []
            for node in G.nodes():
                if any(node in community for community in clique[1]) == False:
                    absent_nodes += 1
                    absent_nodes_names.append([node])
            sum_mod = mod / (len(clique[1]) + absent_nodes)
            if (sum_mod > max_mod[1]):
                max_mod = (clique[0], sum_mod)
                num_partitions = len(clique[1])
                partition = list(map(list, clique[1]))

        result_dic = {
            'num_partitions': num_partitions,
            'modularity': max_mod[1],
            'partition': partition
        }
        return result_dic
