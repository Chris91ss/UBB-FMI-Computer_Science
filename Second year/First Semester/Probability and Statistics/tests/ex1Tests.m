% Load the statistics package
pkg load statistics

% Parameters for population mean test
mu_0 = 50; % Null hypothesis mean
sample_data = [47, 53, 49, 51, 52, 48, 50, 51, 49, 52]; % Example sample
alpha = 0.05; % Significance level
n = length(sample_data); % Sample size
sample_mean = mean(sample_data); % Sample mean
sample_std = std(sample_data); % Sample standard deviation

% Test statistic
t_stat = (sample_mean - mu_0) / (sample_std / sqrt(n));

% Critical values for left, right, and two-tailed tests
t_critical_left = tinv(alpha, n - 1);
t_critical_right = tinv(1 - alpha, n - 1);
t_critical_two = tinv(1 - alpha / 2, n - 1);

% P-values
p_value_left = tcdf(t_stat, n - 1);
p_value_right = 1 - tcdf(t_stat, n - 1);
p_value_two = 2 * min(p_value_left, p_value_right);

% Display results
disp('Hypothesis Testing for Population Mean');
fprintf('Test Statistic: %.4f\n', t_stat);
fprintf('Left-tailed Test: Critical Value = %.4f, P-value = %.4f\n', t_critical_left, p_value_left);
fprintf('Right-tailed Test: Critical Value = %.4f, P-value = %.4f\n', t_critical_right, p_value_right);
fprintf('Two-tailed Test: Critical Values = ±%.4f, P-value = %.4f\n', t_critical_two, p_value_two);

