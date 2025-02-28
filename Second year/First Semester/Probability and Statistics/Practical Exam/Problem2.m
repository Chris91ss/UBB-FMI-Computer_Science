% Octave solution for muzzle velocity analysis

% Given data of muzzle velocities (in m/s)
velocities = [1001.7, 975.0, 978.3, 988.3, 978.7, 988.9, 1000.3, 979.2, 968.9, 983.5, 992.2, 985.6];
n = length(velocities);  % Number of samples

% PART (a): Hypothesis Test
% H0: The average velocity is less than or equal to 995 m/s
% H1: The average velocity is greater than 995 m/s
mu_0 = 995;  % Null hypothesis mean

% Calculate sample mean and standard deviation
sample_mean = mean(velocities);
sample_std = std(velocities);

% Calculate the t-statistic
% t = (sample_mean - mu_0) / (sample_std / sqrt(n))
t_stat = (sample_mean - mu_0) / (sample_std / sqrt(n));

% Degrees of freedom
df = n - 1;

% Critical value for a one-tailed t-test at 5% significance level
alpha = 0.05;
t_critical = tinv(1 - alpha, df);

% Display results for hypothesis test
fprintf('Hypothesis Test:\n');
fprintf('Sample Mean: %.2f m/s\n', sample_mean);
fprintf('Sample Standard Deviation: %.2f m/s\n', sample_std);
fprintf('t-Statistic: %.4f\n', t_stat);
fprintf('Critical Value (t-critical): %.4f\n', t_critical);

if t_stat > t_critical
    fprintf('Result: Reject H0. The data suggests that the muzzles are faster than 995 m/s at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. The data does not provide enough evidence to suggest that the muzzles are faster than 995 m/s.\n');
end

% PART (b): 95% Confidence Interval for the Standard Deviation
% Formula for confidence interval for standard deviation:
% Lower Bound = sqrt((n-1) * s^2 / chi2inv(1 - alpha/2, df))
% Upper Bound = sqrt((n-1) * s^2 / chi2inv(alpha/2, df))

chi2_lower = chi2inv(1 - alpha/2, df);
chi2_upper = chi2inv(alpha/2, df);

lower_bound = sqrt((df * sample_std^2) / chi2_lower);
upper_bound = sqrt((df * sample_std^2) / chi2_upper);

% Display results for confidence interval
fprintf('\n95%% Confidence Interval for the Standard Deviation:\n');
fprintf('Lower Bound: %.2f m/s\n', lower_bound);
fprintf('Upper Bound: %.2f m/s\n', upper_bound);

