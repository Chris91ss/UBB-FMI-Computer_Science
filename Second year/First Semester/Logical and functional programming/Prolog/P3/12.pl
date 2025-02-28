% Generates a sequence Seq of length 2*N + 1 satisfying the constraints
sequence(N, Seq) :-
    Length is 2 * N + 1,
    build_sequence(Length, 0, SeqReversed),
    reverse(SeqReversed, Seq).

% Base case: A sequence of length 1 must end with 0
build_sequence(1, 0, [0]).

% Recursive case:  an allowed previous element and build the rest of the sequence
build_sequence(N, Last, [Prev | Rest]) :-
    N > 1,
    allowed_prev(Prev, Last),
    N1 is N - 1,
    build_sequence(N1, Prev, Rest).

% Define allowed transitions based on |a(i+1) - a(i)| = 1 or 2
allowed_prev(Prev, Last) :-
    member(Prev, [-1, 0, 1]),
    (   abs(Last - Prev) =:= 1
    ;   abs(Last - Prev) =:= 2
    ).

generate_all_sequences(N) :-
    sequence(N, Seq),
    writeln(Seq),
    fail.  % Forces backtracking to find all solutions
generate_all_sequences(_).

% Example usage:
% ?- generate_all_sequences(2).
