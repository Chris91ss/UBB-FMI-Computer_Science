% Part A: Correlation and Regression
% Frequency distributions of X and Y
X_values = [20, 21, 22, 23, 24, 25, 26, 27];
X_freq = [2, 1, 3, 6, 5, 9, 2, 2];

Y_values = [75, 76, 77, 78, 79, 80, 81, 82];
Y_freq = [3, 2, 2, 5, 8, 8, 1, 1];

% Calculate means
mean_X = sum(X_values .* X_freq) / sum(X_freq);
mean_Y = sum(Y_values .* Y_freq) / sum(Y_freq);

% Calculate variances
var_X = sum(((X_values - mean_X).^2) .* X_freq) / sum(X_freq);
var_Y = sum(((Y_values - mean_Y).^2) .* Y_freq) / sum(Y_freq);

% Calculate covariance
cov_XY = sum((X_values - mean_X) .* (Y_values - mean_Y) .* X_freq .* Y_freq') / (sum(X_freq));

% Calculate correlation coefficient
corrcoef_XY = cov_XY / (sqrt(var_X) * sqrt(var_Y));

% Display results for Part A
disp('Part A: Correlation and Regression');
fprintf('Mean of X: %.2f\n', mean_X);
fprintf('Mean of Y: %.2f\n', mean_Y);
fprintf('Variance of X: %.2f\n', var_X);
fprintf('Variance of Y: %.2f\n', var_Y);
fprintf('Covariance of X and Y: %.2f\n', cov_XY);
fprintf('Correlation Coefficient of X and Y: %.2f\n', corrcoef_XY);

% Part B: Confidence Intervals
% Question 1
data = [7, 4, 5, 9, 9, 4, 12, 8, 1, 8, 3, 13, 2, 1, 17, 7, 12, 5, 6, 2, 1, 13, 14, 10, 2, 4, 9, 11, 3, 5, 12, 6, 10, 7];

% a) Known standard deviation (sigma = 5)
alpha = 0.05; % 95% confidence level
sigma = 5; % Known standard deviation
n = length(data);
mean_data = mean(data);
z_value = norminv(1 - alpha / 2);
margin_error = z_value * sigma / sqrt(n);
ci_known_sigma = [mean_data - margin_error, mean_data + margin_error];

% b) Unknown standard deviation
s = std(data);
t_value = tinv(1 - alpha / 2, n - 1);
margin_error_unknown = t_value * s / sqrt(n);
ci_unknown_sigma = [mean_data - margin_error_unknown, mean_data + margin_error_unknown];

% c) Confidence intervals for variance and standard deviation
chi2_lower = chi2inv(alpha / 2, n - 1);
chi2_upper = chi2inv(1 - alpha / 2, n - 1);
ci_variance = [(n - 1) * s^2 / chi2_upper, (n - 1) * s^2 / chi2_lower];
ci_std_dev = sqrt(ci_variance);

% Display results for Part B
disp('Part B: Confidence Intervals');
fprintf('Confidence Interval for Mean (Known Sigma): [%.2f, %.2f]\n', ci_known_sigma);
fprintf('Confidence Interval for Mean (Unknown Sigma): [%.2f, %.2f]\n', ci_unknown_sigma);
fprintf('Confidence Interval for Variance: [%.2f, %.2f]\n', ci_variance);
fprintf('Confidence Interval for Standard Deviation: [%.2f, %.2f]\n', ci_std_dev);
