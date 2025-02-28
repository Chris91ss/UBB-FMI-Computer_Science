% Parameters for the binomial distribution
n = input('Enter the number of trials (n): ');
p = input('Enter the probability of success (p, 0 < p < 1): ');

% Normal approximation parameters
mu = n * p;
sigma = sqrt(n * p * (1 - p));

% Define x values
x = 1:3:n;

% Binomial PDF
binomial_pdf = binopdf(x, n, p);

% Normal approximation PDF
normal_pdf = normpdf(x, mu, sigma);

% Poisson approximation PDF (if p is small and n is large)
lambda = n * p;
poisson_pdf = poisspdf(x, lambda);

% Plotting
figure;
plot(x, binomial_pdf, 'b*');
hold on;
plot(x, normal_pdf, 'g--');
plot(x, poisson_pdf, 'm:');
hold off;

legend('Binomial PDF', 'Normal Approximation', 'Poisson Approximation');
title('Comparison of Binomial, Normal, and Poisson Approximations');
xlabel('x');
ylabel('Probability Density');
grid on;

