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
person(11).
person(12).
person(13).
person(14).
person(15).
person(16).
person(17).
person(18).
person(19).
person(20).


friend(1,2).
friend(2,1).
friend(2,4).
friend(3,2).
friend(4,2).

friend(6,7).
friend(7,6).
friend(8,10).
friend(9,8).
friend(7,8).

friend(11,12).
friend(12,11).
friend(12,14).
friend(13,12).
friend(14,12).

friend(16,17).
friend(17,16).
friend(18,20).
friend(20,19).
friend(18,19).

friend(1,20).
friend(1,19).
friend(7,14).
friend(15,14).
friend(14,15).
friend(14,16).
friend(16,14).

query(smokes(X)).
query(asthma(X)).
