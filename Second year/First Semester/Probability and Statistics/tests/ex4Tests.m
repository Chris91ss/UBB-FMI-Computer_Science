% Data for two samples
sample1 = [22.4, 21.7, 24.5, 23.4, 21.6];
sample2 = [17.7, 14.8, 19.6, 19.6, 12.1];
alpha = 0.05; % Significance level

% Variances and degrees of freedom
var1 = var(sample1);
var2 = var(sample2);
df1 = length(sample1) - 1;
df2 = length(sample2) - 1;

% Test statistic
f_stat = var1 / var2;

% Critical values
f_critical_lower = finv(alpha / 2, df1, df2);
f_critical_upper = finv(1 - alpha / 2, df1, df2);

% P-value
p_value_f = 2 * min(fcdf(f_stat, df1, df2), 1 - fcdf(f_stat, df1, df2));

% Display results
disp('Hypothesis Testing for Ratio of Variances');
fprintf('Test Statistic: %.4f\n', f_stat);
fprintf('Critical Values: [%.4f, %.4f]\n', f_critical_lower, f_critical_upper);
fprintf('P-value: %.4f\n', p_value_f);

