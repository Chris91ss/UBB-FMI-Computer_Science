% Octave solution for comparing heat loss between steel and glass pipes

% Given data for heat loss
steel_pipes = [4.6, 3.7, 4.2, 1.9, 4.8, 6.1, 4.7, 5.5, 5.4];
glass_pipes = [2.5, 1.3, 2.0, 1.8, 2.7, 3.2, 3.0, 3.5, 3.4];

% Number of samples
n1 = length(steel_pipes);
n2 = length(glass_pipes);

% PART (a): F-Test for Equality of Variances at 5% significance level
% H0: The variances are equal
% H1: The variances are not equal

% Calculate sample variances
var1 = var(steel_pipes, 1);  % Population variance for Steel pipes
var2 = var(glass_pipes, 1);  % Population variance for Glass pipes

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
% H0: The mean heat loss of Steel pipes is less than or equal to Glass pipes
% H1: The mean heat loss of Steel pipes is greater than Glass pipes

% Calculate sample means and standard deviations
mean1 = mean(steel_pipes);
mean2 = mean(glass_pipes);
std1 = std(steel_pipes);
std2 = std(glass_pipes);

% Calculate the t-statistic for a two-sample t-test
sp = sqrt(((n1 - 1) * std1^2 + (n2 - 1) * std2^2) / (n1 + n2 - 2));  % Pooled standard deviation
t_stat = (mean1 - mean2) / (sp * sqrt(1 / n1 + 1 / n2));

% Degrees of freedom for the t-test
df_t = n1 + n2 - 2;

% Critical value for a one-tailed t-test at 5% significance level
t_critical = tinv(1 - alpha, df_t);

% Display results for t-test
fprintf('\nTwo-Sample t-Test for Difference in Means:\n');
fprintf('t-Statistic: %.4f\n', t_stat);
fprintf('Critical Value (t-critical): %.4f\n', t_critical);

if t_stat > t_critical
    fprintf('Result: Reject H0. Steel pipes seem to lose more heat than Glass pipes at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. There is not enough evidence to suggest that Steel pipes lose more heat than Glass pipes at the 5%% significance level.\n');
end

