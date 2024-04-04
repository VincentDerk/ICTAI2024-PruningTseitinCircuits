%Expected outcome:
% all_head(1) 0.5
% all_head(3) 0.125
% head_at_least_once(1) 0.5
% head_at_least_once(2) 0.75
% head_at_least_once(3) 0.875
% END
% Source of expected outcome: problog
% Author: Vincent Derkinderen @DTAI 2021
% description:
% some coin tosses

0.5::head(X).

%% Query predicates

% at least once in Y-attempts was the coin toss head.
head_at_least_once(Y) :- between(1,Y,X), head(X).

% at least once in Y-attempts was the coin toss head.
head_at_least_once(Y) :- between(1,Y,X), head(X).

% all Y-attempts were head.
all_head(1) :- head(1).
all_head(Y) :- Y > 1, head(Y), Y2 is Y - 1, all_head(Y2).


query(head_at_least_once(100)).
