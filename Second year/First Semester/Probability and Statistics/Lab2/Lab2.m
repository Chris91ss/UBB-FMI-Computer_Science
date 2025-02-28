n = input("Give no. of trials n = ");  % n - natural number
p = input("Give prob. of success p = ");  % p is from [0, 1]

% Discrete values for the number of successes
x = 0:n;

% Binomial Probability Mass Function (PDF)
px = binopdf(x, n, p);

% Clear previous figure
clf;

% Plot PDF
plot(x, px, 'r*', 'MarkerSize', 8);  % Red stars for PDF

hold on;

% Simulate continuity for CDF
xx = 0:0.001:n;

% Binomial Cumulative Distribution Function (CDF)
cx = binocdf(xx, n, p);

% Plot CDF
plot(xx, cx, 'b-', 'LineWidth', 2);  % Blue line for CDF

% Add legend to indicate PDF and CDF
legend('PDF', 'CDF');

% Add labels and title for clarity
xlabel('Number of successes');
ylabel('Probability');
title('Binomial PDF and CDF');
grid on;

