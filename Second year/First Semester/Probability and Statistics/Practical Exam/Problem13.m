pkg load statistics

% Octave solution for comparing printing times between two brands of printers

% Given data for printing times
brand_A = [29.8, 30.6, 29.0, 27.7, 29.9, 29.6, 30.5, 31.1, 30.2, 28.1, 29.4, 28.5];
brand_B = [31.5, 30.2, 31.2, 29.0, 31.4, 31.1, 32.5, 33.0, 31.3, 30.7, 30.7, 29.9];

% Number of samples
n1 = length(brand_A);
n2 = length(brand_B);

% PART (a): F-Test for Equality of Variances at 5% significance level
% H0: The variances are equal
% H1: The variances are not equal

% Calculate sample variances
var1 = var(brand_A, 1);  % Population variance for Brand A
var2 = var(brand_B, 1);  % Population variance for Brand B

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
% H0: The mean printing time of Brand A is greater than or equal to Brand B
% H1: The mean printing time of Brand A is less than Brand B (Brand A is faster)

% Calculate sample means and standard deviations
mean1 = mean(brand_A);
mean2 = mean(brand_B);
std1 = std(brand_A);
std2 = std(brand_B);

% Calculate the t-statistic for a two-sample t-test
sp = sqrt(((n1 - 1) * std1^2 + (n2 - 1) * std2^2) / (n1 + n2 - 2));  % Pooled standard deviation
t_stat = (mean1 - mean2) / (sp * sqrt(1 / n1 + 1 / n2));

% Degrees of freedom for the t-test
df_t = n1 + n2 - 2;

% Critical value for a one-tailed t-test at 5% significance level
t_critical = tinv(alpha, df_t);

% Display results for t-test
fprintf('\nTwo-Sample t-Test for Difference in Means:\n');
fprintf('t-Statistic: %.4f\n', t_stat);
fprintf('Critical Value (t-critical): %.4f\n', t_critical);

if t_stat < t_critical
    fprintf('Result: Reject H0. Brand A printer seems to be faster at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. There is not enough evidence to suggest that Brand A printer is faster at the 5%% significance level.\n');
end

