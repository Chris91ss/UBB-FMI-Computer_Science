% sum_lists(L1, L2, Sum)
% Sum is the list representation of the sum of numbers represented by lists L1 and L2.

sum_lists(L1, L2, Sum) :-
    reverse(L1, RevL1),
    reverse(L2, RevL2),
    add_lists(RevL1, RevL2, 0, RevSum),
    reverse(RevSum, Sum).

% add_lists(L1, L2, CarryIn, SumList)
% Helper predicate to add two reversed lists of digits with a carry.

add_lists([], [], 0, []).
add_lists([], [], Carry, [Carry]) :- Carry > 0.
add_lists([D1|T1], [], CarryIn, [D|SumTail]) :-
    Sum is D1 + CarryIn,
    D is Sum mod 10,
    CarryOut is Sum // 10,
    add_lists(T1, [], CarryOut, SumTail).
add_lists([], [D2|T2], CarryIn, [D|SumTail]) :-
    Sum is D2 + CarryIn,
    D is Sum mod 10,
    CarryOut is Sum // 10,
    add_lists([], T2, CarryOut, SumTail).
add_lists([D1|T1], [D2|T2], CarryIn, [D|SumTail]) :-
    Sum is D1 + D2 + CarryIn,
    D is Sum mod 10,
    CarryOut is Sum // 10,
    add_lists(T1, T2, CarryOut, SumTail).
