These problems were obtained from the [SCMD Github repository](https://github.com/latower/SCMD). The repository includes the following description for this dataset:

"
state- or country-level connected components extracted from [GridKit: European and North-American extracts](https://zenodo.org/record/47317#.XT9FWlyZZhH), available under the [Open Database License (ODbL) version 1.0](https://github.com/latower/SCMD/blob/master/LICENSE_GridKit).
> Wiegmans, B. (2016). GridKit: European and North-American extracts [Data set]. Zenodo. http://doi.org/10.5281/zenodo.47317
"
A copy of the Open Database License has been included in this directory. The following problem description is present in their [paper](Programming a Stochastic Constraint Optimisation Algorithm, by Optimisation by Daniël Fokkinga, Anna Louise D. Latour, Marie Anastacio, Siegfried Nijssen and Holger Hoos):

>The instances of the transmission grid reliability problem are defined on network models of the European and North-American high-voltage power grids [Wiegmans, 2016], extracted by GridKit. These networks are undirected graphs consisting of power producers, consumers and minor grid nodes (nodes) and powerlines that connect them (edges). For each powergrid from a single European country or North-American state, we extracted the greatest connected components that contain at least one power producer. We selected the components that have at least twenty, and at most one hundred nodes, resulting in a set of 34 networks. The set of interest, consists of a randomly selected set of power consumers for each network. The size of this set is equal to 50% of the total number of power consumers in each network. We used a probability of 0.4 that a powerline remains intact during a natural disaster and 0.875 if it is reinforced [Duenas-Osorio et al., 2017].

The decisions (?::strengthen) in these problems were replaced with a probability of 0.5.


The code in the SCMD repository was written and maintained by 
- Behrouz Babaki ([@Behrouz-Babaki](https://github.com/Behrouz-Babaki))
- Siegfried Nijssen ([@siegfriednijssen](https://github.com/siegfriednijssen))
- Anna Louise Latour ([@latower](https://github.com/latower))
