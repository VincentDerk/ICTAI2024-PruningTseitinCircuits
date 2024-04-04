
0.1::digit(1,0) ; 0.1::digit(1,1) ; 0.1::digit(1,2) ; 0.1::digit(1,3) ; 0.1::digit(1,4) ; 0.1::digit(1,5) ; 0.1::digit(1,6) ; 0.1::digit(1,7) ; 0.1::digit(1,8) ; 0.1::digit(1,9).
0.1::digit(2,0) ; 0.1::digit(2,1) ; 0.1::digit(2,2) ; 0.1::digit(2,3) ; 0.1::digit(2,4) ; 0.1::digit(2,5) ; 0.1::digit(2,6) ; 0.1::digit(2,7) ; 0.1::digit(2,8) ; 0.1::digit(2,9).
0.1::digit(3,0) ; 0.1::digit(3,1) ; 0.1::digit(3,2) ; 0.1::digit(3,3) ; 0.1::digit(3,4) ; 0.1::digit(3,5) ; 0.1::digit(3,6) ; 0.1::digit(3,7) ; 0.1::digit(3,8) ; 0.1::digit(3,9).
0.1::digit(4,0) ; 0.1::digit(4,1) ; 0.1::digit(4,2) ; 0.1::digit(4,3) ; 0.1::digit(4,4) ; 0.1::digit(4,5) ; 0.1::digit(4,6) ; 0.1::digit(4,7) ; 0.1::digit(4,8) ; 0.1::digit(4,9).

sum([A,B,C,D], E) :- digit(1,A), digit(2,B), digit(3,C), digit(4,D), E is A+B+C+D.

query(sum([A,B,C,D], X)).
