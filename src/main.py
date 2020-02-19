'''
File: main.py
Project: src
File Created: Monday, 10th February 2020 4:26:06 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 19th February 2020 4:11:59 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import networkx as nx
from simulator import Epidemic, EpidemicGraph
import matplotlib.pyplot as plt

if __name__ == "__main__":
    from pathlib import Path
    from datetime import datetime
    img_path: Path = Path("./data/out/images/test1/")
    img_path.mkdir(parents=True, exist_ok=True)

    n: int = 200
    k: int = 3

    G: nx.Graph = nx.fast_gnp_random_graph(n=n, p=k/n)
    ep: Epidemic = Epidemic(recovery_period=2)
    EG: EpidemicGraph = EpidemicGraph(G, ep, infected={i: 0 for i in range(1)}, immune=set([1]))
    
    print("Initialized graph.")
    
    command: str = ""
    changed: bool = True
    i: int = 0
    
    while changed and command != "x":
        print(f"Running step {i}...")

        plt.clf()
        EG.draw()
        plt.axis("off")
        plt.show(block=False)
        plt.savefig(
            img_path / f"{i}.png",
            dpi=400,
            bbox_inches='tight',
            pad_inches=0)

        i += 1
        changed = EG.step()
