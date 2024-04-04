0.3::stress(X) :- person(X).
0.2::influences(X,Y) :- person(X), person(Y).

smokes(X) :- stress(X).
smokes(X) :- friend(X,Y), influences(Y,X), smokes(Y).

0.4::asthma(X) :- smokes(X).

person(1).
person(2).
person(3).
person(4).
person(5).
person(6).
person(7).
person(8).
person(9).
person(10).


%
% generated using
%
%>>> import random
%>>> def random_links(persons, prob):
%...     results = list()
%...     for person in persons:
%...             if random.random() <= prob:
%...                     results.append(person)
%...     return results
%>>> def generate(num_ppl, prob):
%...     for i in range(num_ppl):
%...             friends = random_links(range(num_ppl), prob)
%...             for j in friends:
%...                     if i != j:
%...                             print(f"friend({i+1},{j+1}).")
%...
%>>> generate(10, 0.25)

friend(1,6).
friend(3,1).
friend(3,2).
friend(3,5).
friend(3,8).
friend(4,2).
friend(4,3).
friend(4,6).
friend(4,9).
friend(5,3).
friend(5,7).
friend(6,5).
friend(6,8).
friend(7,3).
friend(7,5).
friend(8,6).
friend(8,7).
friend(9,5).
friend(9,7).
friend(10,2).
friend(10,5).
friend(10,8).


query(smokes(X)).
query(asthma(X)).
