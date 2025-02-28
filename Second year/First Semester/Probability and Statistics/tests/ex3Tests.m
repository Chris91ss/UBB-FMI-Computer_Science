% Data for two samples
sample1 = [22.4, 21.7, 24.5, 23.4, 21.6];
sample2 = [17.7, 14.8, 19.6, 19.6, 12.1];
alpha = 0.05; % Significance level

% Known variances (example values)
sigma1_squared = 4; % Variance of sample1
sigma2_squared = 3; % Variance of sample2
n1 = length(sample1);
n2 = length(sample2);

% Test statistic for known variances
mean_diff = mean(sample1) - mean(sample2);
se_known = sqrt(sigma1_squared / n1 + sigma2_squared / n2);
z_stat = mean_diff / se_known;

% P-value for known variances
p_value_known = 2 * (1 - normcdf(abs(z_stat)));

% Display results
disp('Hypothesis Testing for Two Population Means (Known Variances)');
fprintf('Test Statistic: %.4f\n', z_stat);
fprintf('P-value: %.4f\n', p_value_known);

% Unknown variances (equal and unequal variances)
var1 = var(sample1);
var2 = var(sample2);

% Pooled variance for equal variances
sp_squared = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2);
se_equal = sqrt(sp_squared * (1 / n1 + 1 / n2));
t_stat_equal = mean_diff / se_equal;
p_value_equal = 2 * (1 - tcdf(abs(t_stat_equal), n1 + n2 - 2));

% Unequal variances
se_unequal = sqrt(var1 / n1 + var2 / n2);
df_unequal = (var1 / n1 + var2 / n2)^2 / ...
    ((var1^2 / (n1^2 * (n1 - 1))) + (var2^2 / (n2^2 * (n2 - 1))));
t_stat_unequal = mean_diff / se_unequal;
p_value_unequal = 2 * (1 - tcdf(abs(t_stat_unequal), df_unequal));

% Display results for unknown variances
disp('Hypothesis Testing for Two Population Means (Unknown Variances)');
fprintf('Equal Variances: Test Statistic = %.4f, P-value = %.4f\n', t_stat_equal, p_value_equal);
fprintf('Unequal Variances: Test Statistic = %.4f, P-value = %.4f\n', t_stat_unequal, p_value_unequal);

