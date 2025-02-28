pkg load statistics
% Octave solution for comparing assembling times between two methods (updated)

% Given data for assembling times
standard_times = [46, 37, 39, 48, 47, 44, 35, 31, 44, 37];
new_times = [35, 33, 31, 35, 34, 30, 27, 32, 31, 31];

% Number of samples
n1 = length(standard_times);
n2 = length(new_times);

% PART (a): F-Test for Equality of Variances at 5% significance level
% H0: The variances are equal
% H1: The variances are not equal

% Calculate sample variances
var1 = var(standard_times, 1);  % Population variance for standard method
var2 = var(new_times, 1);  % Population variance for new method

% Calculate the F-statistic
F_stat = var1 / var2;

% Degrees of freedom
df1 = n1 - 1;
df2 = n2 - 1;

% Critical values for a two-tailed F-test at 5% significance level
alpha = 0.05;
F_critical_lower = finv(alpha / 2, df1, df2);
F_critical_upper = finv(1 - alpha / 2, df1, df2);

% Display results for F-test
fprintf('F-Test for Equality of Variances:\n');
fprintf('F-Statistic: %.4f\n', F_stat);
fprintf('Lower Critical Value: %.4f\n', F_critical_lower);
fprintf('Upper Critical Value: %.4f\n', F_critical_upper);

if F_stat < F_critical_lower || F_stat > F_critical_upper
    fprintf('Result: Reject H0. The population variances seem to differ at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. There is not enough evidence to suggest that the population variances differ at the 5%% significance level.\n');
end

% PART (b): Two-Sample t-Test for Difference in Means at 5% significance level
% H0: The new method is not more efficient (mean_new >= mean_standard)
% H1: The new method is more efficient (mean_new < mean_standard)

% Calculate sample means and standard deviations
mean1 = mean(standard_times);
mean2 = mean(new_times);
std1 = std(standard_times);
std2 = std(new_times);

% Calculate the t-statistic for a two-sample t-test
sp = sqrt(((n1 - 1) * std1^2 + (n2 - 1) * std2^2) / (n1 + n2 - 2));  % Pooled standard deviation
t_stat = (mean2 - mean1) / (sp * sqrt(1 / n1 + 1 / n2));

% Degrees of freedom for the t-test
df_t = n1 + n2 - 2;

% Critical value for a one-tailed t-test at 5% significance level
t_critical = tinv(alpha, df_t);

% Display results for t-test
fprintf('\nTwo-Sample t-Test for Difference in Means:\n');
fprintf('t-Statistic: %.4f\n', t_stat);
fprintf('Critical Value (t-critical): %.4f\n', t_critical);

if t_stat < t_critical
    fprintf('Result: Reject H0. The new method seems to be more efficient at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. There is not enough evidence to suggest that the new method is more efficient at the 5%% significance level.\n');
end

