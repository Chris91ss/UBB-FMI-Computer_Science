
bank_employees = [3.1, 2.9, 3.8, 3.3, 2.7, 3.0, 2.8, 2.5, 2.6, 2.0, 3.2, 2.4, 2.3, 3.1, 2.1, 3.4];
other_employees = [6.9, 6.4, 4.7, 4.3, 5.1, 6.3, 5.9, 5.4, 5.3, 5.2, 5.1, 5.9, 5.8, 4.9];

n1 = length(bank_employees);
n2 = length(other_employees);

% sample variances
var1 = var(bank_employees, 1);
var2 = var(other_employees, 1);

% Part a):

F_stat = var1 / var2;

% Degrees of freedom
df1 = n1 - 1;
df2 = n2 - 1;

% Critical values
alpha = 0.05;
F_critical_lower = finv(alpha / 2, df1, df2);
F_critical_upper = finv(1 - alpha / 2, df1, df2);

fprintf(' Part a) F-Test for Equality of Variances:\n');
fprintf('F-Statistic: %.4f\n', F_stat);
fprintf('Lower Critical Value: %.4f\n', F_critical_lower);
fprintf('Upper Critical Value: %.4f\n', F_critical_upper);

if F_stat < F_critical_lower || F_stat > F_critical_upper
    fprintf('Result: The population variances seem to differ at the 5% significance level.\n');
else
    fprintf('Result: There is not enough evidence to suggest that the population variances differ at the 5% significance level.\n');
end


% Part b)

% sample means and standard deviations
mean1 = mean(bank_employees);
mean2 = mean(other_employees);
std1 = std(bank_employees);
std2 = std(other_employees);

% t-statistic for a two-sample t-test
sp = sqrt(((n1 - 1) * std1^2 + (n2 - 1) * std2^2) / (n1 + n2 - 2));
t_stat = (mean1 - mean2) / (sp * sqrt(1 / n1 + 1 / n2));

% Degrees of freedom
df_t = n1 + n2 - 2;

% critical value
t_critical = tinv(1 - alpha, df_t);

fprintf('\n Part b) Two-Sample t-Test for Difference in Means:\n');
fprintf('t-Statistic: %.4f\n', t_stat);
fprintf('Critical Value (t-critical): %.4f\n', t_critical);

if t_stat < t_critical
    fprintf('Result: Other employees seem to dispose more white paper than bank employees at the 5%% significance level.\n');
else
    fprintf('Result: There is not enough evidence to suggest that other employees dispose more white paper than bank employees at the 5%% significance level.\n');
end






