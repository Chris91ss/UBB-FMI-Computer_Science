% Parameters for variance test
sigma_0_squared = 25; % Null hypothesis variance
sample_data = [47, 53, 49, 51, 52, 48, 50, 51, 49, 52]; % Example sample
alpha = 0.05; % Significance level
n = length(sample_data); % Sample size
sample_variance = var(sample_data); % Sample variance

% Test statistic
chi2_stat = (n - 1) * sample_variance / sigma_0_squared;

% Critical values
chi2_critical_lower = chi2inv(alpha / 2, n - 1);
chi2_critical_upper = chi2inv(1 - alpha / 2, n - 1);

% P-value
p_value_variance = 2 * min(chi2cdf(chi2_stat, n - 1), 1 - chi2cdf(chi2_stat, n - 1));

% Display results
disp('Hypothesis Testing for Population Variance');
fprintf('Test Statistic: %.4f\n', chi2_stat);
fprintf('Critical Values: [%.4f, %.4f]\n', chi2_critical_lower, chi2_critical_upper);
fprintf('P-value: %.4f\n', p_value_variance);

