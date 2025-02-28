% Load the necessary package
pkg load statistics

% Question 2: Premium and Regular Gas Mileage
premium = [22.4, 21.7, 24.5, 23.4, 21.6, 23.3, 22.4, 21.6, 24.8, 20.0];
regular = [17.7, 14.8, 19.6, 19.6, 12.1, 14.8, 15.4, 12.6, 14.0, 12.2];

% Confidence level (1 - alpha)
alpha = 0.05; % 95% confidence level

% a) Equal variances (sigma1 = sigma2)
mean_diff = mean(premium) - mean(regular);
pooled_std = sqrt(((var(premium) * (length(premium) - 1)) + (var(regular) * (length(regular) - 1))) / ...
                 (length(premium) + length(regular) - 2));
se_diff = pooled_std * sqrt(1 / length(premium) + 1 / length(regular));
t_value = tinv(1 - alpha / 2, length(premium) + length(regular) - 2); % Calculate t-value for pooled variances
margin_error_equal = t_value * se_diff;
ci_equal_var = [mean_diff - margin_error_equal, mean_diff + margin_error_equal];

% b) Unequal variances (Welch's t-test)
se_diff_unequal = sqrt(var(premium) / length(premium) + var(regular) / length(regular));
df = (var(premium) / length(premium) + var(regular) / length(regular))^2 / ...
    ((var(premium)^2 / ((length(premium) - 1) * length(premium)^2)) + ...
    (var(regular)^2 / ((length(regular) - 1) * length(regular)^2)));
t_value_unequal = tinv(1 - alpha / 2, df); % Calculate t-value for Welch's test
margin_error_unequal = t_value_unequal * se_diff_unequal;
ci_unequal_var = [mean_diff - margin_error_unequal, mean_diff + margin_error_unequal];

% c) Confidence interval for ratio of variances
s1_squared = var(premium); % Variance of premium
s2_squared = var(regular); % Variance of regular

df1 = length(premium) - 1; % Degrees of freedom for premium
df2 = length(regular) - 1; % Degrees of freedom for regular

f_lower = finv(alpha / 2, df1, df2); % Lower critical value of F-distribution
f_upper = finv(1 - alpha / 2, df1, df2); % Upper critical value of F-distribution

ci_var_ratio = [s1_squared / s2_squared / f_upper, s1_squared / s2_squared * f_lower];

% Display results
disp('Part B: Confidence Intervals for Gas Mileage');
fprintf('Confidence Interval for Difference (Equal Variances): [%.2f, %.2f]\n', ci_equal_var);
fprintf('Confidence Interval for Difference (Unequal Variances): [%.2f, %.2f]\n', ci_unequal_var);
fprintf('Confidence Interval for Variance Ratio: [%.2f, %.2f]\n', ci_var_ratio);

