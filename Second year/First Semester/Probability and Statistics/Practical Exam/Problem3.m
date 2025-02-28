% Octave solution for nickel particle size analysis

% Given data of nickel particle sizes
particle_sizes = [3.26, 1.89, 2.42, 2.03, 3.07, 2.95, 1.39, 3.06, 2.46, 3.35, 1.56, 1.79, 1.76, 3.82, 2.42, 2.96];
n = length(particle_sizes);  % Number of samples

% PART (a): 95% Confidence Interval for the Mean
% Calculate sample mean and standard deviation
sample_mean = mean(particle_sizes);
sample_std = std(particle_sizes);

% Degrees of freedom
df = n - 1;

% Critical value for a two-tailed t-distribution at 95% confidence level
alpha = 0.05;
t_critical = tinv(1 - alpha/2, df);

% Calculate the margin of error
margin_of_error = t_critical * (sample_std / sqrt(n));

% Calculate the confidence interval
lower_bound = sample_mean - margin_of_error;
upper_bound = sample_mean + margin_of_error;

% Display results for confidence interval
fprintf('95%% Confidence Interval for the Mean:\n');
fprintf('Lower Bound: %.2f\n', lower_bound);
fprintf('Upper Bound: %.2f\n', upper_bound);

% PART (b): Hypothesis Test
% H0: The average size is greater than or equal to 3
% H1: The average size is less than 3
mu_0 = 3;  % Null hypothesis mean

% Calculate the t-statistic
% t = (sample_mean - mu_0) / (sample_std / sqrt(n))
t_stat = (sample_mean - mu_0) / (sample_std / sqrt(n));

% Critical value for a one-tailed t-test at 1% significance level
alpha = 0.01;
t_critical_one_tailed = tinv(alpha, df);

% Display results for hypothesis test
fprintf('\nHypothesis Test:\n');
fprintf('Sample Mean: %.2f\n', sample_mean);
fprintf('Sample Standard Deviation: %.2f\n', sample_std);
fprintf('t-Statistic: %.4f\n', t_stat);
fprintf('Critical Value (t-critical): %.4f\n', t_critical_one_tailed);

if t_stat < t_critical_one_tailed
    fprintf('Result: Reject H0. The data suggests that the average size of nickel particles is smaller than 3 at the 1%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. The data does not provide enough evidence to suggest that the average size of nickel particles is smaller than 3.\n');
end

