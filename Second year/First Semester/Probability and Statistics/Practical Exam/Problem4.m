% Octave solution for nickel particle size analysis

% Given data of nickel particle sizes
particle_sizes = [3.26, 1.89, 2.42, 2.03, 3.07, 2.95, 1.39, 3.06, 2.46, 3.35, 1.56, 1.79, 1.76, 3.82, 2.42, 2.96];
n = length(particle_sizes);  % Number of samples

% PART (a): Hypothesis Test at 5% significance level
% H0: The average size is greater than or equal to 3
% H1: The average size is less than 3
mu_0 = 3;  % Null hypothesis mean

% Calculate sample mean and standard deviation
sample_mean = mean(particle_sizes);
sample_std = std(particle_sizes);

% Calculate the t-statistic
% t = (sample_mean - mu_0) / (sample_std / sqrt(n))
t_stat = (sample_mean - mu_0) / (sample_std / sqrt(n));

% Degrees of freedom
df = n - 1;

% Critical value for a one-tailed t-test at 5% significance level
alpha = 0.05;
t_critical = tinv(alpha, df);

% Display results for hypothesis test
fprintf('Hypothesis Test:\n');
fprintf('Sample Mean: %.2f\n', sample_mean);
fprintf('Sample Standard Deviation: %.2f\n', sample_std);
fprintf('t-Statistic: %.4f\n', t_stat);
fprintf('Critical Value (t-critical): %.4f\n', t_critical);

if t_stat < t_critical
    fprintf('Result: Reject H0. The data suggests that the average size of nickel particles is smaller than 3 at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. The data does not provide enough evidence to suggest that the average size of nickel particles is smaller than 3.\n');
end

% PART (b): 99% Confidence Interval for the Standard Deviation
% Formula for confidence interval for standard deviation:
% Lower Bound = sqrt((n-1) * s^2 / chi2inv(1 - alpha/2, df))
% Upper Bound = sqrt((n-1) * s^2 / chi2inv(alpha/2, df))

alpha = 0.01;  % For 99% confidence interval
chi2_lower = chi2inv(1 - alpha / 2, df);
chi2_upper = chi2inv(alpha / 2, df);

lower_bound = sqrt((df * sample_std^2) / chi2_lower);
upper_bound = sqrt((df * sample_std^2) / chi2_upper);

% Display results for confidence interval
fprintf('\n99%% Confidence Interval for the Standard Deviation:\n');
fprintf('Lower Bound: %.2f\n', lower_bound);
fprintf('Upper Bound: %.2f\n', upper_bound);

