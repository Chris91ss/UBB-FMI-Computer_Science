x = linspace(0, 3, 100);

% Functions
y1 = x.^5 / 10;
y2 = x .* sin(x);
y3 = cos(x);

% Plot them on the same set of axes
figure;
plot(x, y1, 'r-', x, y2, 'g--', x, y3, 'b-.');
title('Functions on the same plot');
legend('x^5/10', 'x * sin(x)', 'cos(x)');
grid on;

% Plot them on different pictures in the same window
figure;
subplot(3, 1, 1);
plot(x, y1, 'r-');
title('x^5/10');
grid on;

subplot(3, 1, 2);
plot(x, y2, 'g--');
title('x * sin(x)');
grid on;

subplot(3, 1, 3);
plot(x, y3, 'b-.');
title('cos(x)');
grid on;
