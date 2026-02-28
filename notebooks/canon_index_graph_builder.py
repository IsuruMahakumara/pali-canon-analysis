import json
from pathlib import Path


import networkx as nx




def initialize_canon_index_graph():

    G = nx.DiGraph()

    G.add_node("Canon", level=0)

    G.add_node("Sutta", level=1, level_label='Pitaka')
    G.add_node("Vinaya", level=1, level_label='Pitaka')
    G.add_node("Abhidhamma", level=1, level_label='Pitaka')

    G.add_node("Saṁyuttanikāya", level=2, level_label='Nikāya')
    G.add_node("Dīghanikāya", level=2, level_label='Nikāya')
    G.add_node('Majjhimanikāya', level=2, level_label='Nikāya')
    G.add_node('Anguttaranikāya', level=2, level_label='Nikāya')
    G.add_node('Khuddakanikāya', level=2, level_label='Nikāya')


    G.add_node("Dhammasangani", level=2, id=1)
    G.add_node("Vibhanga", level=2, id=2)
    G.add_node("Dhatukatha", level=2, id=3)
    G.add_node("Kathavatthu", level=2, id=4)
    G.add_node("Puggalapannatti", level=2, id=5)
    G.add_node("Yamaka", level=2, id=6)
    G.add_node("Patthana", level=2, id=7)


    relationships = [
        ("Canon", "Sutta"),
        ("Canon", "Vinaya"),
        ("Canon", "Abhidhamma"),

        
        ("Sutta", "Saṁyuttanikāya"),
        ("Sutta", "Dīghanikāya"),
        ("Sutta", "Majjhimanikāya"),
        ("Sutta", "Anguttaranikāya"),
        ("Sutta", "Khuddakanikāya"),

        ("Abhidhamma", "Dhammasangani"),
        ("Abhidhamma", "Vibhanga"),
        ("Abhidhamma", "Dhatukatha"),
        ("Abhidhamma", "Kathavatthu"),
        ("Abhidhamma", "Puggalapannatti"),
        ("Abhidhamma", "Yamaka"),
        ("Abhidhamma", "Patthana"),
    ]

    G.add_edges_from(relationships)

    return G


def build_dn_index_subgraph(G):
    dn_path ='../data/dn-index-tree.json'
    dn_index = json.load(open(dn_path, "r", encoding="utf-8"))


    ## DN Vagga Level = 3
    vagga_list = list(dn_index.keys())

    for node in vagga_list:
        G.add_node( f"dn:{node}", name=node, level=3, level_label='Vagga')

    dn_vagga_relationships = [("Dīghanikāya", f"dn:{node}") for node in vagga_list]

    G.add_edges_from(dn_vagga_relationships)

    ## DN Sutta Level = 4
    dn_sutta_relationships = []

    for vagga, sutta_dict in dn_index.items():
        for sutta_id, sutta_name in sutta_dict.items():
            edge = [(f"dn:{vagga}", f"dn:{sutta_name}")]
            dn_sutta_relationships.extend(edge)



            G.add_node(f"dn:{sutta_name}", name=sutta_name, level=4, level_label='Sutta', reading_unit_id=sutta_id, reading_unit=True)





    G.add_edges_from(dn_sutta_relationships)

    return G


def build_sn_index_subgraph ():
    pass

def build_mn_index_subgraph ():
    pass

def build_an_index_subgraph ():
    pass


def build_kn_index_subgraph ():
    pass