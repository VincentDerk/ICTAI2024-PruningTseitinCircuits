0.7::burglary.
0.2::earthquake.

0.9::alarm :- burglary.
0.3::alarm :- earthquake.

0.8::calls(john) :- alarm.
0.1::calls(john) :- \+alarm.

query(calls(john)).
