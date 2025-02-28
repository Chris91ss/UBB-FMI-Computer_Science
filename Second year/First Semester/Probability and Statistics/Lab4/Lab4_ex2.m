% 2a
function X = bernoulli(p, n)
    % Generate n samples from Bernoulli(p)
    U = rand(1, n); % Uniform(0,1) random numbers
    X = U < p;      % 1 if U < p, else 0
end

% Example: Generate 100 samples with p = 0.5
samples = bernoulli(0.5, 100);
disp(samples);


% 2b
function X = binomial(n, p, trials)
    % Generate 'trials' samples from Binomial(n, p)
    X = zeros(1, trials);
    for i = 1:trials
        X(i) = sum(bernoulli(p, n));
    end
end

% Example: Generate 100 samples with n = 10 and p = 0.5
samples = binomial(10, 0.5, 100);
disp(samples);


% 2c
function X = geometric(p, n)
    % Generate n samples from Geometric(p)
    X = zeros(1, n);
    for i = 1:n
        count = 0;
        while rand() >= p
            count = count + 1;
        end
        X(i) = count;
    end
end

% Example: Generate 100 samples with p = 0.5
samples = geometric(0.5, 100);
disp(samples);


% 2d
function X = pascal(n, p, trials)
    % Generate 'trials' samples from Pascal(n, p)
    X = zeros(1, trials);
    for i = 1:trials
        count = 0;
        successes = 0;
        while successes < n
            if rand() < p
                successes = successes + 1;
            else
                count = count + 1;
            end
        end
        X(i) = count;
    end
end

% Example: Generate 100 samples with n = 5 and p = 0.5
samples = pascal(5, 0.5, 100);
disp(samples);

