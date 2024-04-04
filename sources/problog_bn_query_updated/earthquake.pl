%% ProbLog program: PGM 11
%% Created on 2024-03-30 00:19:31.774501
query(johnCalls).
0.02::earthquake.
0.01::burglary.
0.95::alarm :- burglary, earthquake.
0.94::alarm :- burglary, \+earthquake.
0.29::alarm :- \+burglary, earthquake.
0.001::alarm :- \+burglary, \+earthquake.
0.7::maryCalls :- alarm.
0.01::maryCalls :- \+alarm.
0.9::johnCalls :- alarm.
0.05::johnCalls :- \+alarm.
