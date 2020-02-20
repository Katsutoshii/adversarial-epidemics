'''
File: main.py
Project: src
File Created: Monday, 10th February 2020 4:26:06 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Thursday, 20th February 2020 1:14:18 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

if __name__ == "__main__":
    import networkx as nx
    from simulator import Epidemic, EpidemicGraph
    import matplotlib.pyplot as plt
    from pathlib import Path
    from datetime import datetime
    
    img_path: Path = Path("./data/out/images/test1/")
    img_path.mkdir(parents=True, exist_ok=True)

    n: int = 200
    k: int = 3

    G: nx.Graph = nx.fast_gnp_random_graph(n=n, p=k/n)
    ep: Epidemic = Epidemic(recovery_period=2)
    EG: EpidemicGraph = EpidemicGraph(
        G=G,
        ep=ep,
        infected={i: 0 for i in range(3)},
        immune=set([1, 2, 3]))
    
    print("Initialized graph.")
    
    command: str = ""
    i: int = 0
    
    while command != "x":
        print(f"Running step {i}...")
        i += 1
        EG.savefig(img_path / f"{i}.pdf", dpi=200)
        if EG.step(): break
 