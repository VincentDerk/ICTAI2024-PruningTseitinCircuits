%% ProbLog program: PGM 43
%% Created on 2024-03-30 00:25:06.435899
query(dysp).
0.01::asia.
0.5::smoke.
0.05::tub :- asia.
0.01::tub :- \+asia.
0.6::bronc :- smoke.
0.3::bronc :- \+smoke.
0.1::lung :- smoke.
0.01::lung :- \+smoke.
either :- \+lung, tub.
\+either :- \+lung, \+tub.
either :- lung.
0.98::xray :- either.
0.05::xray :- \+either.
0.9::dysp :- bronc, either.
0.8::dysp :- bronc, \+either.
0.7::dysp :- \+bronc, either.
0.1::dysp :- \+bronc, \+either.
