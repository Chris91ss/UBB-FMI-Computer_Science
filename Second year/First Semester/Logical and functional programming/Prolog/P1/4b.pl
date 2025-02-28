% Base case: If the list is empty, the result is also empty.
add_after_even([], []).

% Recursive case: If the head is even, add it to the result followed by 1, and recurse.
add_after_even([Head|Tail], [Head, 1|ResultTail]) :-
    0 is Head mod 2,  % Check if the head is even
    add_after_even(Tail, ResultTail).

% If the head is odd, simply add it to the result and recurse.
add_after_even([Head|Tail], [Head|ResultTail]) :-
    1 is Head mod 2,  % Check if the head is odd
    add_after_even(Tail, ResultTail).
