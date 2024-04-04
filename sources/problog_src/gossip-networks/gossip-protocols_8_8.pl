%Expected outcome:
% in(0,8,packet) 1         
% in(1,8,packet) 0.99653865
% in(2,8,packet) 0.99653865
% in(3,8,packet) 0.99245199
% in(4,8,packet) 0.99653865
% in(5,8,packet) 0.99245199
% in(6,8,packet) 0.992452  
% in(7,8,packet) 0.98774003
% END
% Source of expected outcome: problog
% Author: Vincent Derkinderen and Alexander Vandenbroucke, 2020

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

0.33333333 :: policy(0,1,TP,P)
; 0.333333335 :: policy(0,2,TP,P)
; 0.333333335 :: policy(0,4,TP,P).
0.33333333 :: policy(1,0,TP,P)
; 0.333333335 :: policy(1,3,TP,P)
; 0.333333335 :: policy(1,5,TP,P).
0.33333333 :: policy(2,3,TP,P)
; 0.333333335 :: policy(2,0,TP,P)
; 0.333333335 :: policy(2,6,TP,P).
0.33333333 :: policy(3,2,TP,P)
; 0.333333335 :: policy(3,1,TP,P)
; 0.333333335 :: policy(3,7,TP,P).
0.33333333 :: policy(4,5,TP,P)
; 0.333333335 :: policy(4,6,TP,P)
; 0.333333335 :: policy(4,0,TP,P).
0.33333333 :: policy(5,4,TP,P)
; 0.333333335 :: policy(5,7,TP,P)
; 0.333333335 :: policy(5,1,TP,P).
0.33333333 :: policy(6,7,TP,P)
; 0.333333335 :: policy(6,4,TP,P)
; 0.333333335 :: policy(6,2,TP,P).
0.33333333 :: policy(7,6,TP,P)
; 0.333333335 :: policy(7,5,TP,P)
; 0.333333335 :: policy(7,3,TP,P).
dir_link(0,0).
dir_link(0,1).
dir_link(0,2).
dir_link(0,4).
dir_link(1,1).
dir_link(1,0).
dir_link(1,3).
dir_link(1,5).
dir_link(2,2).
dir_link(2,3).
dir_link(2,0).
dir_link(2,6).
dir_link(3,3).
dir_link(3,2).
dir_link(3,1).
dir_link(3,7).
dir_link(4,4).
dir_link(4,5).
dir_link(4,6).
dir_link(4,0).
dir_link(5,5).
dir_link(5,4).
dir_link(5,7).
dir_link(5,1).
dir_link(6,6).
dir_link(6,7).
dir_link(6,4).
dir_link(6,2).
dir_link(7,7).
dir_link(7,6).
dir_link(7,5).
dir_link(7,3).
policy(0,0,TP,P).
policy(1,1,TP,P).
policy(2,2,TP,P).
policy(3,3,TP,P).
policy(4,4,TP,P).
policy(5,5,TP,P).
policy(6,6,TP,P).
policy(7,7,TP,P).
in(0,0,packet).

query(in(X,8,packet)) :- in(X,8,packet). %Problem size = 8s
