# MATLAB Mathematics

**Source:** https://www.mathworks.com/help/matlab/mathematics.html  
**Version:** R2026a

> Math functions use processor-optimized libraries for fast vector and matrix calculations.

---

## 1. Elementary Math

```matlab
% Trigonometry (angles in RADIANS by default)
sin(pi/2)            % 1
cos(0)               % 1
tan(pi/4)            % 1
asin(1)              % pi/2
atan2(y, x)          % four-quadrant arc tangent

% Degrees variants
sind(90), cosd(0)    % use degrees directly

% Exponentials and logarithms
exp(1)               % e = 2.7183
log(exp(1))          % 1 (natural log)
log2(8)              % 3
log10(1000)          % 3
sqrt(16)             % 4
nthroot(27, 3)       % 3 (real cube root)
abs(-5)              % 5

% Rounding
floor(2.9)           % 2
ceil(2.1)            % 3
round(2.5)           % 3
fix(2.9)             % 2 (truncate toward zero)
mod(7, 3)            % 1 (modulo — preserves sign of divisor)
rem(7, 3)            % 1 (remainder — preserves sign of dividend)

% Complex numbers
z = 3 + 4i;
real(z)              % 3
imag(z)              % 4
abs(z)               % 5 (magnitude)
angle(z)             % atan2(4,3)
conj(z)              % 3 - 4i

% Discrete math
factorial(5)         % 120
nchoosek(10, 3)      % 120 (combinations)
primes(20)           % [2 3 5 7 11 13 17 19]
isprime(17)          % true
gcd(12, 8)           % 4
lcm(4, 6)            % 12
```

---

## 2. Linear Algebra

```matlab
A = [4 7; 2 6];
b = [1; 2];

% Solve linear system A*x = b
x = A \ b            % backslash operator (preferred)
x = inv(A) * b       % via inverse (less numerically stable)

% Matrix properties
det(A)               % determinant
rank(A)              % rank
trace(A)             % sum of diagonal (trace)
norm(A)              % 2-norm (largest singular value)
norm(A, 'fro')       % Frobenius norm
cond(A)              % condition number
inv(A)               % inverse
pinv(A)              % Moore-Penrose pseudoinverse

% Eigenvalues and eigenvectors
[V, D] = eig(A)      % V: eigenvectors (columns), D: diagonal eigenvalues
e = eig(A)           % just eigenvalues as vector

% Singular Value Decomposition (SVD)
[U, S, V] = svd(A)   % A = U*S*V'
svd(A)               % just singular values

% Matrix decompositions
[L, U, P] = lu(A)    % LU decomposition: P*A = L*U
[Q, R] = qr(A)       % QR decomposition
R = chol(A)          % Cholesky (A must be positive definite)

% Special operations
diag(A)              % extract diagonal as vector
diag([1 2 3])        % create diagonal matrix
triu(A)              % upper triangular part
tril(A)              % lower triangular part
kron(A, B)           % Kronecker tensor product

% Cross and dot products
dot(u, v)            % dot product
cross(u, v)          % cross product (3D vectors)
```

---

## 3. Statistics and Descriptive Functions

```matlab
x = [4 2 7 1 9 3 5];

mean(x)              % 4.4286
median(x)            % 4
std(x)               % standard deviation
var(x)               % variance
min(x)               % 1
max(x)               % 9
[mn, idx] = min(x)   % also get index
range(x)             % max - min
sum(x)               % 31
cumsum(x)            % cumulative sum
prod(x)              % product
cumprod(x)           % cumulative product

% For matrices (operates along dimension)
mean(A, 1)           % mean of each column (default)
mean(A, 2)           % mean of each row
sum(A, 'all')        % sum of all elements (R2018b+)

% Percentiles and quantiles
prctile(x, 25)       % 25th percentile
quantile(x, 0.5)     % 50th percentile (median)

% Correlation and covariance
corrcoef(x, y)       % correlation matrix
cov(x, y)            % covariance matrix
```

---

## 4. Random Number Generation

```matlab
% Set seed for reproducibility
rng(42)              % seed with integer
rng('default')       % reset to default

% Uniform distributions
rand(3)              % 3x3 uniform [0,1]
rand(1, 5)           % 1x5 uniform [0,1]
randi(10, 3, 4)      % 3x4 integers in [1,10]
randi([5, 15], 2)    % 2x2 integers in [5,15]

% Normal distribution
randn(3)             % 3x3 standard normal N(0,1)
mu + sigma * randn(n, 1)  % N(mu, sigma^2)

% Other distributions (Statistics Toolbox)
randperm(n)          % random permutation of 1:n
shuffle(v)           % random shuffle alternative: v(randperm(end))
```

---

## 5. Interpolation

```matlab
% 1D interpolation
x = [0 1 2 3 4];
y = [0 1 4 9 16];
xi = 0:0.1:4;
yi = interp1(x, y, xi);           % linear (default)
yi = interp1(x, y, xi, 'cubic'); % cubic
yi = interp1(x, y, xi, 'spline'); % spline (smooth)
yi = interp1(x, y, xi, 'pchip');  % shape-preserving

% 2D interpolation
[X, Y] = meshgrid(1:4, 1:4);
Z = X.^2 + Y.^2;
[Xq, Yq] = meshgrid(1:0.5:4, 1:0.5:4);
Zq = interp2(X, Y, Z, Xq, Yq);
Zq = interp2(X, Y, Z, Xq, Yq, 'cubic');

% Scattered data interpolation
F = scatteredInterpolant(x, y, z);
zq = F(xq, yq);
```

---

## 6. Optimization

```matlab
% Minimize scalar function (fminbnd — bounded 1D)
f = @(x) x.^2 - 4*x + 4;
[xmin, fval] = fminbnd(f, 0, 5);   % minimize on [0,5]

% Minimize multi-variable function (fminsearch — Nelder-Mead)
g = @(x) (x(1)-2).^2 + (x(2)-3).^2;
x0 = [0, 0];
[xopt, fval] = fminsearch(g, x0);

% Linear least squares
x = A \ b;                         % min ||Ax - b||^2

% Non-negative least squares
x = lsqnonneg(A, b);

% Find roots of function
r = fzero(@(x) x^3 - x - 1, 1.0); % root near x=1
```

---

## 7. Numerical Integration and Differential Equations

### 7.1 Numerical Integration
```matlab
% Quadrature (numerical integration)
f = @(x) sin(x) ./ x;
q = integral(f, 0.001, pi)          % ∫f dx from 0.001 to pi
q = integral2(f2d, 0, 1, 0, 1)     % double integral
q = integral3(f3d, 0,1, 0,1, 0,1)  % triple integral

% Trapezoidal rule (for discrete data)
trapz(x, y)                         % integrate y w.r.t. x
```

### 7.2 Ordinary Differential Equations (ODEs)
```matlab
% dy/dt = f(t,y)
f = @(t, y) -2 * y;          % exponential decay

tspan = [0, 5];
y0 = 1;                       % initial condition

% Solvers (choose based on stiffness)
[t, y] = ode45(f, tspan, y0);   % Runge-Kutta 4/5, general purpose
[t, y] = ode23(f, tspan, y0);   % lower order, faster for loose tolerances
[t, y] = ode15s(f, tspan, y0);  % stiff problems
[t, y] = ode23s(f, tspan, y0);  % stiff, low order

% Specify output times
tspan = 0:0.1:5;
[t, y] = ode45(f, tspan, y0);

% Options
opts = odeset('RelTol', 1e-8, 'AbsTol', 1e-10);
[t, y] = ode45(f, tspan, y0, opts);

% System of ODEs (y is a vector)
% Lorenz system example:
lorentz = @(t, y) [10*(y(2)-y(1));
                   y(1)*(28-y(3))-y(2);
                   y(1)*y(2)-(8/3)*y(3)];
[t, Y] = ode45(lorentz, [0 50], [1; 1; 1]);
```

---

## 8. Fourier Analysis and Filtering

```matlab
% Fast Fourier Transform
N = 1024;
t = (0:N-1) / Fs;        % time vector (Fs = sample rate)
signal = sin(2*pi*50*t) + 0.5*sin(2*pi*120*t);  % 50Hz + 120Hz

Y = fft(signal);          % complex FFT
P = abs(Y/N);             % single-sided amplitude
f = Fs * (0:N/2) / N;    % frequency axis

% Inverse FFT
x_restored = ifft(Y);

% 2D FFT (images, spatial data)
F = fft2(img);
F_shifted = fftshift(F);  % center DC component

% Convolution
output = conv(signal, kernel);       % 1D convolution
output = conv2(img, kernel, 'same'); % 2D, same size output

% Digital filtering
b = [1 -1];              % FIR highpass coefficients
y = filter(b, 1, x);    % apply FIR filter
```

---

## 9. Sparse Matrices

```matlab
% Create sparse matrix
S = sparse(rows, cols, vals, m, n)  % from triplet format
S = speye(n)                         % sparse identity
full(S)                              % convert to full matrix

% Sparse linear solvers
x = S \ b          % automatically uses sparse algorithms
```
