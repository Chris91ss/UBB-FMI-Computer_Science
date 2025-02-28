add_digit_helper([], 0, []).

add_digit_helper([], Carry, [Carry]) :- Carry > 0.

add_digit_helper([Head|Tail], Carry, [NewHead|NewTail]) :-
    Sum is Head + Carry,
    NewHead is Sum mod 10,   
    NewCarry is Sum // 10,   
    add_digit_helper(Tail, NewCarry, NewTail). 

add_digit(List, Digit, Result) :-
    reverse(List, ReversedList),             
    add_digit_helper(ReversedList, Digit, ReversedResult),
    reverse(ReversedResult, Result).  

%Examples:
%add_digit([1, 9, 3, 5, 9, 9], 2, Result).
%add_digit([], 3, Result).
%add_digit([], 0, Result).
