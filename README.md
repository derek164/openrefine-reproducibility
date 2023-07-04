<!-- vscode-markdown-toc -->
* 1. [Dependencies](#Dependencies)
* 2. [Usage](#Usage)
* 3. [Data](#Data)
	* 3.1. [Assumptions](#Assumptions)
	* 3.2. [ER Diagram](#ERDiagram)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc --># openrefine-reproducibility
Based on [nikolausn/OpenRefine-Reproducibility-Demo](https://github.com/nikolausn/OpenRefine-Reproducibility-Demo/blob/master/Python_OpenRefine_Demo.ipynb)

##  1. <a name='Dependencies'></a>Dependencies
[Docker](https://www.docker.com/products/docker-desktop/)

##  2. <a name='Usage'></a>Usage
Clone the repository
```
git clone https://github.com/derek164/openrefine-reproducibility.git && cd openrefine-reproducibility
```

Start OpenRefine server and client
```
docker compose up
```

Execute OpenRefine workflow
```
docker-compose run --rm -it --entrypoint python openrefine-client /app/main.py
```

##  3. <a name='Data'></a>Data
[Wine reviews](https://www.kaggle.com/datasets/zynicide/wine-reviews) scraped from WineEnthusiast. 

###  3.1. <a name='Assumptions'></a>Assumptions
1. Not all wineries make their wine from grapes which they grew or sourced from a local vineyard
2. Each wine is made with grapes from one location of varying specificity, from country to vineyard

###  3.2. <a name='ERDiagram'></a>ER Diagram
<img src='img/ER_Wine_Reviews.svg' width='600'>