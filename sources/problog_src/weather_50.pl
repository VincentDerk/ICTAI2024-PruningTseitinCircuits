%Expected outcome:
% weather(rain,50) 0.66664919
% weather(sun,50) 0.33335081
% END
% Source: https://dtai.cs.kuleuven.be/problog/tutorial/tutslides/02_more.html

0.5::weather(sun,0) ; 0.5::weather(rain,0).

0.6::weather(sun,T) ; 0.4::weather(rain,T) :- T>0, Tprev is T-1, weather(sun,Tprev).
0.2::weather(sun,T) ; 0.8::weather(rain,T) :- T>0, Tprev is T-1, weather(rain,Tprev).

query(weather(sun,50)).
