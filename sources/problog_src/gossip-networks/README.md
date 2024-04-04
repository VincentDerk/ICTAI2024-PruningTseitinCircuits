These problems are routing networks, where packets in each timestep can be probabilistically forwarded to other nodes.

### Gossip networks:
A network where a node, in its timestep, shares information with its neighbors (spreading gossip/infecting with a disease/...). The queries posed pertain to the probability that a certain node (X) has the information at a certain time. The timestep in these problems (n) can be changed to increase the size of the problem.

The timestemp (n) can be changed by, for example, changing the `8` in the following code
```prolog
query(in(X,8,packet)) :- in(X,8,packet). %Problem size = 8s
```

Authors: Vincent Derkinderen and Alexander Vandenbroucke @DTAI 2020

