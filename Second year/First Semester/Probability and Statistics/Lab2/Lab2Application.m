% Given: A coin is tossed 3 times. Let X denote the number of heads that appear.

% Parameters
n = 3;  % Number of trials (coin tosses)
p = 0.5;  % Probability of success (heads)
x = 0:n;  % Possible outcomes (number of heads)

% a) Find the probability distribution function (PDF) of X.
pdf_values = binopdf(x, n, p);
disp('a) PDF values for X:');
disp(pdf_values);

% b) Find the cumulative distribution function (CDF) of X.
cdf_values = binocdf(x, n, p);
disp('b) CDF values for X:');
disp(cdf_values);

% c) Find P(X = 0) and P(X ≠ 1).
P_X_0 = binopdf(0, n, p);  % P(X = 0)
P_X_not_1 = 1 - binopdf(1, n, p);  % P(X ≠ 1)
disp('c) P(X = 0):');
disp(P_X_0);
disp('P(X ≠ 1):');
disp(P_X_not_1);

% d) Find P(X ≤ 2) and P(X < 2).
P_X_leq_2 = binocdf(2, n, p);  % P(X <= 2)
P_X_lt_2 = binocdf(1, n, p);   % P(X < 2)
disp('d) P(X ≤ 2):');
disp(P_X_leq_2);

disp('P(X < 2):');
disp(P_X_lt_2);

% e) Find P(X ≥ 1) and P(X > 1).
P_X_geq_1 = 1 - binocdf(0, n, p);  % P(X >= 1)
P_X_gt_1 = 1 - binocdf(1, n, p);   % P(X > 1)
disp('e) P(X ≥ 1):');
disp(P_X_geq_1);
disp('P(X > 1):');
disp(P_X_gt_1);

% f) Simulate 3 coin tosses and compute the value of X.
num_trials = 3;  % Number of coin tosses
p_success = 0.5;  % Probability of heads
X = binornd(num_trials, p_success);  % Simulate 1 trial of 3 tosses
disp('f) Simulated number of heads:');
disp(X);


% method 2
N = input("Give no. of simulations N = ");
U = rand(3, N);
Y = (U < 0.5); % 1 - heads, 0 - tails
X = sum(Y); % sum the columns of Y
clf;
hist(X);

