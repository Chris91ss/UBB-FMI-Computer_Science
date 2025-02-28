% sum_sublists(List, SumDigits)
% SumDigits is the list representation of the sum of all numbers represented as sublists in List.

sum_sublists(List, SumDigits) :-
    extract_sublists(List, Sublists),
    sum_list_of_lists(Sublists, [0], SumDigits).

% sum_list_of_lists(Sublists, Acc, TotalSum)
% Helper predicate to sum a list of digit lists.

sum_list_of_lists([], Sum, Sum).
sum_list_of_lists([Digits|Rest], Acc, TotalSum) :-
    sum_lists(Acc, Digits, NewAcc),
    sum_list_of_lists(Rest, NewAcc, TotalSum).

% extract_sublists(List, Sublists)
% Extracts all sublists from the heterogeneous list.

extract_sublists([], []).
extract_sublists([H|T], [H|Sublists]) :-
    is_list(H), !,
    extract_sublists(T, Sublists).
extract_sublists([_|T], Sublists) :-
    extract_sublists(T, Sublists).

% sum_lists(L1, L2, Sum)
% Reuse the predicate from part a to sum two lists of digits.

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
