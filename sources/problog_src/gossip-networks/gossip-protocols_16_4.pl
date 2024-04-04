%Expected outcome:
% in(0,4,packet) 1         
% in(1,4,packet) 0.74415588
% in(10,4,packet) 0.49682617
% in(11,4,packet) 0.27452087
% in(12,4,packet) 0.49682617
% in(13,4,packet) 0.27452087
% in(14,4,packet) 0.27452087
% in(15,4,packet) 0.09375   
% in(2,4,packet) 0.74415588
% in(3,4,packet) 0.49682617
% in(4,4,packet) 0.74415588
% in(5,4,packet) 0.49682617
% in(6,4,packet) 0.49682617
% in(7,4,packet) 0.27452087
% in(8,4,packet) 0.74415588
% in(9,4,packet) 0.49682617
% END

failure(nil,nil,nil,nil).
in(X,T,P) :-
  dir_link(Y,X),
  TP is T - 1,
  TP >= 0,
  \+failure(Y,X,TP,P),
  policy(Y,X,TP,P),
  in(Y,TP,P).
in(X,T,P) :- TP is T - 1, TP >= 0, policy(X,X,TP,P), in(X,TP,P).
used_link(Y,X,T,P) :- T >= 0, in(Y,T,P), TN is T + 1, in(X,TN,P).

0.25 :: policy(0,1,TP,P); 0.25 :: policy(0,2,TP,P); 0.25 :: policy(0,4,TP,P); 0.25 :: policy(0,8,TP,P).
0.25 :: policy(1,0,TP,P); 0.25 :: policy(1,3,TP,P); 0.25 :: policy(1,5,TP,P); 0.25 :: policy(1,9,TP,P).
0.25 :: policy(2,3,TP,P); 0.25 :: policy(2,0,TP,P); 0.25 :: policy(2,6,TP,P); 0.25 :: policy(2,10,TP,P).
0.25 :: policy(3,2,TP,P); 0.25 :: policy(3,1,TP,P); 0.25 :: policy(3,7,TP,P); 0.25 :: policy(3,11,TP,P).
0.25 :: policy(4,5,TP,P); 0.25 :: policy(4,6,TP,P); 0.25 :: policy(4,0,TP,P); 0.25 :: policy(4,12,TP,P).
0.25 :: policy(5,4,TP,P); 0.25 :: policy(5,7,TP,P); 0.25 :: policy(5,1,TP,P); 0.25 :: policy(5,13,TP,P).
0.25 :: policy(6,7,TP,P); 0.25 :: policy(6,4,TP,P); 0.25 :: policy(6,2,TP,P); 0.25 :: policy(6,14,TP,P).
0.25 :: policy(7,6,TP,P); 0.25 :: policy(7,5,TP,P); 0.25 :: policy(7,3,TP,P); 0.25 :: policy(7,15,TP,P).
0.25 :: policy(8,9,TP,P); 0.25 :: policy(8,10,TP,P); 0.25 :: policy(8,12,TP,P); 0.25 :: policy(8,0,TP,P).
0.25 :: policy(9,8,TP,P); 0.25 :: policy(9,11,TP,P); 0.25 :: policy(9,13,TP,P); 0.25 :: policy(9,1,TP,P).
0.25 :: policy(10,11,TP,P); 0.25 :: policy(10,8,TP,P); 0.25 :: policy(10,14,TP,P); 0.25 :: policy(10,2,TP,P).
0.25 :: policy(11,10,TP,P); 0.25 :: policy(11,9,TP,P); 0.25 :: policy(11,15,TP,P); 0.25 :: policy(11,3,TP,P).
0.25 :: policy(12,13,TP,P); 0.25 :: policy(12,14,TP,P); 0.25 :: policy(12,8,TP,P); 0.25 :: policy(12,4,TP,P).
0.25 :: policy(13,12,TP,P); 0.25 :: policy(13,15,TP,P); 0.25 :: policy(13,9,TP,P); 0.25 :: policy(13,5,TP,P).
0.25 :: policy(14,15,TP,P); 0.25 :: policy(14,12,TP,P); 0.25 :: policy(14,10,TP,P); 0.25 :: policy(14,6,TP,P).
0.25 :: policy(15,14,TP,P); 0.25 :: policy(15,13,TP,P); 0.25 :: policy(15,11,TP,P); 0.25 :: policy(15,7,TP,P).
dir_link(0,0).
dir_link(0,1).
dir_link(0,2).
dir_link(0,4).
dir_link(0,8).
dir_link(1,1).
dir_link(1,0).
dir_link(1,3).
dir_link(1,5).
dir_link(1,9).
dir_link(2,2).
dir_link(2,3).
dir_link(2,0).
dir_link(2,6).
dir_link(2,10).
dir_link(3,3).
dir_link(3,2).
dir_link(3,1).
dir_link(3,7).
dir_link(3,11).
dir_link(4,4).
dir_link(4,5).
dir_link(4,6).
dir_link(4,0).
dir_link(4,12).
dir_link(5,5).
dir_link(5,4).
dir_link(5,7).
dir_link(5,1).
dir_link(5,13).
dir_link(6,6).
dir_link(6,7).
dir_link(6,4).
dir_link(6,2).
dir_link(6,14).
dir_link(7,7).
dir_link(7,6).
dir_link(7,5).
dir_link(7,3).
dir_link(7,15).
dir_link(8,8).
dir_link(8,9).
dir_link(8,10).
dir_link(8,12).
dir_link(8,0).
dir_link(9,9).
dir_link(9,8).
dir_link(9,11).
dir_link(9,13).
dir_link(9,1).
dir_link(10,10).
dir_link(10,11).
dir_link(10,8).
dir_link(10,14).
dir_link(10,2).
dir_link(11,11).
dir_link(11,10).
dir_link(11,9).
dir_link(11,15).
dir_link(11,3).
dir_link(12,12).
dir_link(12,13).
dir_link(12,14).
dir_link(12,8).
dir_link(12,4).
dir_link(13,13).
dir_link(13,12).
dir_link(13,15).
dir_link(13,9).
dir_link(13,5).
dir_link(14,14).
dir_link(14,15).
dir_link(14,12).
dir_link(14,10).
dir_link(14,6).
dir_link(15,15).
dir_link(15,14).
dir_link(15,13).
dir_link(15,11).
dir_link(15,7).
policy(0,0,TP,P).
policy(1,1,TP,P).
policy(2,2,TP,P).
policy(3,3,TP,P).
policy(4,4,TP,P).
policy(5,5,TP,P).
policy(6,6,TP,P).
policy(7,7,TP,P).
policy(8,8,TP,P).
policy(9,9,TP,P).
policy(10,10,TP,P).
policy(11,11,TP,P).
policy(12,12,TP,P).
policy(13,13,TP,P).
policy(14,14,TP,P).
policy(15,15,TP,P).
in(0,0,packet).

query(in(X,4,packet)) :- in(X,4,packet). %Problem size = 4
