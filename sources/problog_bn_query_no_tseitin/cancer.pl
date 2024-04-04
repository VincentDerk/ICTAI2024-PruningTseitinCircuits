%% ProbLog program: PGM 7
%% Created on 2024-03-29 23:56:44.637339
query(dyspnoea).
0.1::pollution.
0.3::smoker.
0.03::cancer :- \+pollution, smoker.
0.001::cancer :- \+pollution, \+smoker.
0.05::cancer :- pollution, smoker.
0.02::cancer :- pollution, \+smoker.
0.65::dyspnoea :- cancer.
0.3::dyspnoea :- \+cancer.
0.1::xray :- cancer.
0.8::xray :- \+cancer.
