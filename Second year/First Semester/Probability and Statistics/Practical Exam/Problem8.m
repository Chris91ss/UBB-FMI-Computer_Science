% Octave solution for comparing weights from two suppliers

% Given data for weights from two suppliers
supplier_A = [1021, 980, 1017, 988, 1005, 998, 1014, 985, 995, 1004, 1030, 1015, 995, 1023];
supplier_B = [1070, 970, 993, 1013, 1006, 1002, 1014, 997, 1002, 1010, 975];

% Number of samples
n1 = length(supplier_A);
n2 = length(supplier_B);

% PART (a): F-Test for Equality of Variances at 5% significance level
% H0: The variances are equal
% H1: The variances are not equal

% Calculate sample variances
var1 = var(supplier_A, 1);  % Population variance for Supplier A
var2 = var(supplier_B, 1);  % Population variance for Supplier B

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
% H0: The mean weight of Supplier A is less than or equal to Supplier B
% H1: The mean weight of Supplier A is greater than Supplier B

% Calculate sample means and standard deviations
mean1 = mean(supplier_A);
mean2 = mean(supplier_B);
std1 = std(supplier_A);
std2 = std(supplier_B);

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
    fprintf('Result: Reject H0. Supplier A seems to be more reliable at the 5%% significance level.\n');
else
    fprintf('Result: Fail to reject H0. There is not enough evidence to suggest that Supplier A is more reliable at the 5%% significance level.\n');
end

