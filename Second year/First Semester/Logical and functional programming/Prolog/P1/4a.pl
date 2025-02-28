% Base case: If the first list is empty, the result is also empty.
set_difference([], _, []).

% Recursive case: If the head of the first list is not in the second list,
% add it to the result and recurse on the tail.
set_difference([Head|Tail], B, [Head|ResultTail]) :-
    \+ member(Head, B),
    set_difference(Tail, B, ResultTail).

% If the head of the first list is in the second list, skip it and recurse.
set_difference([Head|Tail], B, Result) :-
    member(Head, B),
    set_difference(Tail, B, Result).
