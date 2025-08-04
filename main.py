import csv
import matplotlib.pyplot as plt
import hypernetx as hnx
import json
import utils as u
import sys
import networkx as nx
from itertools import combinations
import re
import metrics_cathegorized_by_dimensions

def safe_float(cell):
    try:
        # First, replace comma with dot if present
        cell = cell.replace(',', '.')
        return str(float(cell))
    except:
        return cell
    

def mean_value(sum, numbers):
    return round(sum/numbers, 6)
    
#Increase max size for each field (10 MB)
csv.field_size_limit(10000000)
if __name__ == "__main__":
    hyperedges = {}

    dataset_list = []

    domains_datasets_statistics = {}

    with open("./LODCLOUD_Metadata/lod-data.json", "r", encoding="utf-8") as f:
        datasets = json.load(f)

    with open('./Weekly_Data/2023-07-26.csv', mode ="r", encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        counter = 0
        for row in reader:
            if counter == 0:
                counter = counter + 1
                continue
            #print(row)

            #Convert decimal numbers from comma to dot
            try:
                row = [safe_float(cell) for cell in row]
            except ValueError as e:
                print("Error parsing row:", e)
                continue

            domain =None

            try:
                domain = datasets[row[0]].get("domain")           
            except:
                pass

            if(domain != None):
                try:
                    domains_datasets_statistics[domain] += 1
                except (KeyError):
                    domains_datasets_statistics[domain] = 1

            dataset_list.append(row[0])
            new_edges = u.add_KG_data(row)

            if(len(new_edges) > 0):
                counter = counter + 1
                hyperedges.update(new_edges)
            

        print("Successfully read ", counter - 1 ," Datasets\n")

        print("Total number of hyperedges: ", len(hyperedges))

        print("Domains_statistics:\n", domains_datasets_statistics)

        hypergraph = hnx.Hypergraph(hyperedges)

        #creating sub_hypergraph (if needed for fast analysis)
        sub_edges = {k: list(hypergraph.edges[k]) for k in list(hypergraph.edges)[:30000]}

        hypergraph = hnx.Hypergraph(sub_edges)


    #B = hypergraph.bipartite()

    #degrees = dict(B.degree())  # includes both nodes and hyperedges

    #mean_degree = sum(degrees.values()) / len(degrees)

    # Customize node appearance
    #node_sizes = [20 * degrees[n] for n in B.nodes()]
    #node_colors = ['red' if degrees[n] >= mean_degree and n not in dataset_list else 'gray' for n in B.nodes()]

    # Separate node types
    #nodes = [n for n, d in B.nodes(data=True) if d.get('bipartite') == 0]
    #hedges = [n for n in B.nodes if n not in nodes]

    #nodes = [n for n in B.nodes]

    # Layout
    #pos = nx.spring_layout(B, k=0.5, iterations=100)

    # Draw nodes
    #nx.draw_networkx_nodes(B, pos, nodelist=nodes, node_size = node_sizes, node_color = node_colors, alpha=0.8)

    # Draw edges (light and thin)
    #nx.draw_networkx_edges(B, pos, alpha=0.10, width=0.2)

    #nx.draw_networkx_edge_labels(B, pos, edge_labels = {e: e for e in B.edges if e[0] in hedges and e[1] in nodes}, font_size=4, font_color='gray')

    #nx.draw_networkx_labels(B, pos, font_size=5, font_color='black')

    #This dictionary will contain the count of occurrences of a domain for a particular value of quality metric, that will be defined later
    

    #TO BE CONTINUED (Calculate mean values for each metric)
    mean_values = {}

    for edge in hypergraph.edges:
        sum = 0



    domain_count = {}

    metric_per_dimension = 5

    for edge in hypergraph.edges:
        if("Interlinking" in edge):
            for nodeString in hypergraph.edges[edge]:
                #Ignoring Dataset String
                if nodeString == hypergraph.edges[edge][0]:
                    continue

                #print("NodeString: ", nodeString)
                #Defining a regex that will find all integers and floats (if any) in our nodeString
                numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", nodeString)]

                #Check if any are greater than 0.5
                if any(n > 0.7 for n in numbers):
                    edge_with_dataset_domain = hypergraph.edges[hypergraph.edges[edge][0]]
                    domain = edge_with_dataset_domain[1]
                    try:
                        domain_count[domain] = domain_count[domain] + 1
                    except:

                        domain_count[domain] = 1
            

    for domain in list(domain_count):
        domain_count[domain] = round(float(domain_count[domain] / (domains_datasets_statistics[domain] * metric_per_dimension) * 100), 1)


    print("Percentage of datasets(cathegorized by domain) satisfying our quality metric threshold")

    print(domain_count)

    #plt.axis('off')
    #plt.title("Improved Hypergraph (spring layout, faded edges)")
    #plt.show()

    #hnx.drawing.draw(hypergraph, with_node_labels = False, node_labels_kwargs = {'fontsize': 5}, edge_labels_kwargs = {'fontsize': 5}, with_edge_labels = False)   
    #plt.show()