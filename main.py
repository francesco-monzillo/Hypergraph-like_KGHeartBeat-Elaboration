import csv
import matplotlib.pyplot as plt
import hypernetx as hnx
import json
import utils as u
import sys

#Increase max size for each field (10 MB)
csv.field_size_limit(10000000)

if __name__ == "__main__":

    hyperedges = {}

    with open('./Weekly_Data/2025-06-01.csv', mode ="r", encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        counter = 0
        for row in reader:
            if counter == 0:
                counter = counter + 1
                continue
            #print(row)
            new_edges = u.add_KG_data(row)

            if(len(new_edges) > 0):
                counter = counter + 1
                hyperedges.update(new_edges)
            

        print("Successfully read ", counter - 1 ," Datasets\n")

        print("Total number of hyperedges: ", len(hyperedges))


        hypergraph = hnx.Hypergraph(hyperedges)


        sub_edges = {k: list(hypergraph.edges[k]) for k in list(hypergraph.edges)[:80]}

        hypergraph = hnx.Hypergraph(sub_edges)

        print("Nodes:", list(hypergraph.nodes))



        hnx.drawing.draw(hypergraph, with_node_labels=True, with_edge_labels=True)
        plt.show()