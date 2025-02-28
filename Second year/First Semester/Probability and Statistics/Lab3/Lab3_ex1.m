pkg load statistics

% Parameters
mu = 0;
sigma = 1;

% Part a: Compute P(X <= 0) and P(X >= 0)
p_x_leq_0 = normcdf(0, mu, sigma);
p_x_geq_0 = 1 - p_x_leq_0;

fprintf('P(X <= 0) = %.4f\n', p_x_leq_0);
fprintf('P(X >= 0) = %.4f\n', p_x_geq_0);

% Part b: Compute P(-1 <= X <= 1) and P(X <= -1 or X >= 1)
p_x_between = normcdf(1, mu, sigma) - normcdf(-1, mu, sigma);
p_x_outside = 1 - p_x_between;

fprintf('P(-1 <= X <= 1) = %.4f\n', p_x_between);
fprintf('P(X <= -1 or X >= 1) = %.4f\n', p_x_outside);

% Part c: Compute x_alpha for a given alpha
alpha = input('Enter the value for alpha (0 < alpha < 1): ');
x_alpha = norminv(alpha, mu, sigma);

fprintf('x_alpha for alpha = %.2f: %.4f\n', alpha, x_alpha);

% Part d: Compute x_beta for a given beta
beta = input('Enter the value for beta (0 < beta < 1): ');
x_beta = norminv(1 - beta, mu, sigma);

fprintf('x_beta for beta = %.2f: %.4f\n', beta, x_beta);

