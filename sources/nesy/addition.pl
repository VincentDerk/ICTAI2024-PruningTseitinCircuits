0.1::digit(1,0) ; 0.1::digit(1,1) ; 0.1::digit(1,2) ; 0.1::digit(1,3) ; 0.1::digit(1,4) ; 0.1::digit(1,5) ; 0.1::digit(1,6) ; 0.1::digit(1,7) ; 0.1::digit(1,8) ; 0.1::digit(1,9).
0.1::digit(2,0) ; 0.1::digit(2,1) ; 0.1::digit(2,2) ; 0.1::digit(2,3) ; 0.1::digit(2,4) ; 0.1::digit(2,5) ; 0.1::digit(2,6) ; 0.1::digit(2,7) ; 0.1::digit(2,8) ; 0.1::digit(2,9).

addition(X,Y,Z) :- digit(X,X2), digit(Y,Y2), Z is X2+Y2.

query(addition(1,2,10)).