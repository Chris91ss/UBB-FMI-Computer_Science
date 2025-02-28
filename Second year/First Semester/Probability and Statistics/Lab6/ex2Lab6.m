% Load necessary package
pkg load statistics

% Data
premium = [22.4, 21.7, 24.5, 23.4, 21.6, 23.3, 22.4, 21.6, 24.8, 20.0];
regular = [17.7, 14.8, 19.6, 19.6, 12.1, 14.8, 15.4, 12.6, 14.0, 12.2];

% Parameters
alpha = 0.05; % Significance level

% a) Test H0: variances are equal
var_premium = var(premium);
var_regular = var(regular);
f_stat = var_premium / var_regular; % Test statistic
df1 = length(premium) - 1;
df2 = length(regular) - 1;
f_critical_lower = finv(alpha / 2, df1, df2); % Lower critical value
f_critical_upper = finv(1 - alpha / 2, df1, df2); % Upper critical value

fprintf('Exercise 2a - Variances Test\n');
if f_stat < f_critical_lower || f_stat > f_critical_upper
    disp('Reject H0: Variances are not equal.');
else
    disp('Fail to reject H0: Variances are equal.');
end
fprintf('F-statistic: %.4f, Critical Values: [%.4f, %.4f]\n', f_stat, f_critical_lower, f_critical_upper);

% b) Test H0: premium mean <= regular mean
mean_diff = mean(premium) - mean(regular);
pooled_std = sqrt(((var_premium * (length(premium) - 1)) + (var_regular * (length(regular) - 1))) / ...
                  (length(premium) + length(regular) - 2));
se_diff = pooled_std * sqrt(1 / length(premium) + 1 / length(regular));
t_stat_b = mean_diff / se_diff; % Test statistic
t_critical_b = tinv(1 - alpha, length(premium) + length(regular) - 2);

fprintf('Exercise 2b - Means Test\n');
if t_stat_b > t_critical_b
    disp('Reject H0: Premium gas mileage is higher on average.');
else
    disp('Fail to reject H0: Premium gas mileage is not higher on average.');
end
fprintf('T-statistic: %.4f, Critical Value: %.4f\n', t_stat_b, t_critical_b);

