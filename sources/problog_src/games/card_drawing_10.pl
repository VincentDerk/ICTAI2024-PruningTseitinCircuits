% Expected outcome source: ProbLog
% Author: Vincent Derkinderen @DTAI 2022
% description:
% There are 10 cards (cf. allCards(X)).
% You draw a sequence of cards from it, without replacement.
% Relies on findall/3, select_uniform/4, and subtract/3.
:- use_module(library(lists)).

% draw Card at Time
draw(Card,1) :- allCards(AllCards), select_uniform(1,AllCards,Card,_).
draw(Card,Time) :- 
    Time > 1,
    TimePrev is Time - 1,
    availableCards(Cards,Time),
    select_uniform(Time,Cards,Card,_).


% All cards available for drawing at time Time.
% So draw(X,Time) has not 'yet' happened.
availableCards(Cards, Time) :-
    TimePrev is Time - 1,
    findall(Card,(between(1,TimePrev,Time2),draw(Card,Time2)), UsedCards),
    allCards(AllCards),
    subtract(AllCards,UsedCards,Cards).

allCards([1,2,3,4,5,6,7,8,9,10]). %% Changes complexity of the problem


%% Queries

win :- 
    draw(X,1),
    draw(Y,2),
    X > Y.

query(win).
