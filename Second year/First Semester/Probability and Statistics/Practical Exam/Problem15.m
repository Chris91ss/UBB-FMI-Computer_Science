% Octave solution for comparing white paper disposal between bank employees and other employees

% Given data for white paper disposal (in kilograms per year)
bank_employees = [6.1, 5.9, 6.4, 6.7, 6.3, 6.4, 6.5, 6.1, 6.2, 6.0, 6.2];
other_employees = [6.5, 6.4, 6.9, 7.1, 7.3, 6.8, 7.0, 7.2, 7.1, 6.9, 7.4];

% Number of samples
n1 = length(bank_employees);
n2 = length(other_employees);

% PART (a): F-Test for Equality of Variances at 5% significance level
% H0: The variances are equal
% H1: The variances are not equal

% Calculate sample variances
var1 = var(bank_employees, 1);  % Population variance for bank employees
var2 = var(other_employees, 1);  % Population variance for other employees

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
% H0: The mean disposal of bank employees is greater than or equal to other employees
% H1: The mean disposal of bank employees is less than other employees (other employees dispose more paper)

% Calculate sample means and standard deviations
mean1 = mean(bank_employees);
mean2 = mean(other_employees);
std1 = std(bank_employees);
std2 = std(other_employees);

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

if t_stat < t_critical
    fprintf('Result: Reject H0. Other employees seem to dispose more white paper than bank employees at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. There is not enough evidence to suggest that other employees dispose more white paper than bank employees at the 5%% significance level.\n');
end

