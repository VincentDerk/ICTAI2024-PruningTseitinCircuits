%Expected outcome:
% all_head(1) 0.498
% all_head(3) 0.12402
% all_head(10) 0.00096685592
% head_at_least_once(1) 0.498
% head_at_least_once(2) 0.7476
% head_at_least_once(3) 0.87282
% head_at_least_once(30) 0.99999977
% END
% Source of expected outcome: problog
% Author: Vincent Derkinderen @DTAI 2021
% description:
% some coin tosses

0.01::coin_is_biased.

0.5::unbiased_head(X).
0.3::biased_head(X).

head(X) :- coin_is_biased, biased_head(X).
head(X) :- \+coin_is_biased, unbiased_head(X).

%% Query predicates

% at least once in Y-attempts was the coin toss head.
head_at_least_once(Y) :- between(1,Y,X), head(X).

% at least once in Y-attempts was the coin toss head.
head_at_least_once(Y) :- between(1,Y,X), head(X).

% all Y-attempts were head.
all_head(1) :- head(1).
all_head(Y) :- Y > 1, head(Y), Y2 is Y - 1, all_head(Y2).

query(head_at_least_once(100)).
query(all_head(100)).
