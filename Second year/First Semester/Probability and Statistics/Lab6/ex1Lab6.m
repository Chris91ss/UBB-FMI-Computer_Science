% Load necessary package
pkg load statistics

% Data
data = [7, 4, 5, 9, 9, 4, 12, 8, 1, 8, 3, 13, 2, 1, 17, 7, 12, 5, 6, 2, 1, 13, 14, 10, 2, 4, 9, 11, 3, 5, 12, 6, 10, 7];

% Parameters
alpha_1 = 0.05; % Significance level 5%
alpha_2 = 0.01; % Significance level 1%
sigma = 5; % Given standard deviation
mu_0 = 8.5; % Null hypothesis mean

% a) Test H0: mu >= 8.5 at 5% and 1% significance level
n = length(data);
sample_mean = mean(data);
z_5 = (sample_mean - mu_0) / (sigma / sqrt(n)); % Test statistic
z_critical_5 = norminv(alpha_1); % Critical value for 5%
z_critical_1 = norminv(alpha_2); % Critical value for 1%

% P-value for 5%
p_value_5 = normcdf(z_5);

% Rejection Region
fprintf('Exercise 1a - 5%% Significance Level\n');
if z_5 < z_critical_5
    disp('Reject H0: The efficiency standard is not met at 5%.');
else
    disp('Fail to reject H0: The efficiency standard is met at 5%.');
end

fprintf('P-value: %.4f\n', p_value_5);

fprintf('Exercise 1a - 1%% Significance Level\n');
if z_5 < z_critical_1
    disp('Reject H0: The efficiency standard is not met at 1%.');
else
    disp('Fail to reject H0: The efficiency standard is met at 1%.');
end

% b) Test H0: mu <= 5.5 with unknown sigma
mu_b = 5.5; % Null hypothesis mean
sample_std = std(data);
t_stat = (sample_mean - mu_b) / (sample_std / sqrt(n)); % Test statistic
t_critical = tinv(1 - alpha_1, n - 1); % Critical value for 5%

% P-value for b
p_value_b = 1 - tcdf(t_stat, n - 1);

fprintf('Exercise 1b - 5%% Significance Level\n');
if t_stat > t_critical
    disp('Reject H0: The number of files stored exceeds 5.5.');
else
    disp('Fail to reject H0: The number of files stored does not exceed 5.5.');
end

fprintf('P-value: %.4f\n', p_value_b);

