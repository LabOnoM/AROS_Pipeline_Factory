# MATLAB Quick Reference Cheatsheet

**For rapid lookup — covers the most-used patterns from all topic areas.**  
**Source:** https://www.mathworks.com/help/matlab/  

---

## Syntax Essentials

```matlab
%  → comment
;  → suppress output / row separator in arrays
:  → range (1:10), slice (A(2,:)), linearize (A(:))
... → line continuation
~  → ignore output: [~, idx] = sort(v)
@  → function handle: f = @(x) x.^2
.* → element-wise multiply (vs * for matrix multiply)
\  → solve A*x=b via A\b (preferred over inv(A)*b)
'  → transpose (conjugate) or character delimiter
"  → string scalar delimiter
```

---

## Most-Used Functions By Category

### Arrays
| Function | Description |
|---|---|
| `zeros(m,n)` | m×n zeros matrix |
| `ones(m,n)` | m×n ones matrix |
| `eye(n)` | n×n identity |
| `linspace(a,b,n)` | n evenly spaced from a to b |
| `a:step:b` | range with explicit step |
| `size(A)` | dimensions [rows, cols] |
| `numel(A)` | total elements |
| `length(A)` | max(size(A)) |
| `reshape(A,m,n)` | reshape (column-major) |
| `A(:)` | flatten to column vector |
| `A'` | transpose |
| `[A;B]` | vertical concatenation |
| `[A,B]` | horizontal concatenation |
| `sort(v)` | sort ascending |
| `find(v>0)` | indices where condition is true |
| `unique(v)` | unique values |

### Math
| Function | Description |
|---|---|
| `sum(A)` | column sums (or `sum(A,'all')`) |
| `cumsum(v)` | cumulative sum |
| `prod(A)` | product |
| `mean(A)` | mean (per column by default) |
| `std(A)` | std deviation |
| `min/max(A)` | min or max |
| `abs(x)` | absolute value |
| `sqrt(x)` | square root |
| `exp(x)` | e^x |
| `log(x)` | natural log |
| `mod(a,b)` | modulo a/b |
| `round/floor/ceil(x)` | rounding |
| `A\b` | solve linear system Ax=b |
| `eig(A)` | eigenvalues |
| `svd(A)` | singular value decomposition |
| `fft(x)` | fast Fourier transform |
| `conv(u,v)` | convolution |

### Strings
| Function | Description |
|---|---|
| `sprintf(fmt,...)` | format string |
| `num2str(x)` | number to string |
| `str2double(s)` | string to double |
| `strsplit(s,delim)` | split string |
| `strjoin(C,delim)` | join cell of strings |
| `contains(s,pat)` | check substring |
| `strrep(s,old,new)` | replace substring |
| `upper/lower(s)` | change case |
| `strtrim(s)` | remove whitespace |
| `fprintf(fmt,...)` | print to command window |

### Control Flow
```matlab
if cond; ...; elseif cond2; ...; else; ...; end
for i = 1:n; ...; end
while cond; ...; end
switch x; case val; ...; otherwise; ...; end
break    % exit loop
continue % next iteration
return   % exit function early
```

### File I/O
| Function | Description |
|---|---|
| `load('file.mat')` | load MATLAB binary |
| `save('file.mat','v1','v2')` | save variables |
| `readtable('f.csv')` | read table from CSV/Excel |
| `writetable(T,'f.csv')` | write table |
| `readmatrix('f.csv')` | read numeric matrix |
| `writematrix(M,'f.csv')` | write numeric matrix |
| `imread('img.tif')` | read image |
| `imwrite(img,'out.tif')` | write image |
| `dir('*.csv')` | list files |
| `fullfile(folder,name)` | safe path join |

### Plotting
| Function | Description |
|---|---|
| `figure` | new figure window |
| `plot(x,y)` | 2D line plot |
| `scatter(x,y)` | scatter plot |
| `bar(x,y)` | bar chart |
| `histogram(data)` | histogram |
| `imagesc(M)` | display matrix as image |
| `imshow(img)` | display image |
| `surf(X,Y,Z)` | 3D surface |
| `contourf(X,Y,Z)` | filled contours |
| `subplot(r,c,i)` | subplot grid |
| `title/xlabel/ylabel(s)` | labels |
| `legend(...)` | legend |
| `grid on/off` | grid lines |
| `xlim/ylim([a b])` | axis limits |
| `hold on/off` | overlay plots |
| `colorbar` | color scale |
| `colormap(name)` | set colormap |
| `saveas(gcf,'f.png')` | save figure |
| `exportgraphics(gcf,'f.pdf')` | high-quality export |

---

## Common Patterns for Scientific Computing

### Loading and Processing a Stack of TIF Images
```matlab
files = dir(fullfile('data', '*.tif'));
stack = [];
for k = 1:numel(files)
    img = imread(fullfile(files(k).folder, files(k).name));
    stack = cat(3, stack, img);  % append along 3rd dim
end
% stack is now H×W×N
```

### Processing Multiple CSVs and Aggregating
```matlab
files = dir('results_*.csv');
all_data = table();
for k = 1:numel(files)
    T = readtable(fullfile(files(k).folder, files(k).name));
    T.Source = repmat({files(k).name}, height(T), 1);
    all_data = [all_data; T];
end
```

### Fitting Data and Plotting with Confidence Intervals
```matlab
x = (0:10)';
y = 2*x + 1 + randn(11,1)*0.5;

% Linear regression
p = polyfit(x, y, 1);         % coefficients [slope, intercept]
y_fit = polyval(p, x);

figure; hold on;
scatter(x, y, 'k', 'DisplayName', 'Data')
plot(x, y_fit, 'r-', 'LineWidth', 2, 'DisplayName', 'Fit')
legend; grid on;
xlabel('x'); ylabel('y');
title(sprintf('y = %.2fx + %.2f', p(1), p(2)));
```

### Parallel Image Processing
```matlab
files = dir('images/*.tif');
results = zeros(numel(files), 1);

parfor k = 1:numel(files)
    img = imread(fullfile(files(k).folder, files(k).name));
    img_d = im2double(img);
    results(k) = mean(img_d(:));   % compute mean intensity
end
```

### Calling Python from MATLAB
```matlab
% Simple call
x = py.math.sqrt(42);

% Use numpy
np = py.importlib.import_module('numpy');
arr = np.array([1.0, 2.0, 3.0]);
result = double(np.sum(arr));   % convert back

% Run arbitrary Python code
pyrun("import numpy as np; y = np.log(x)", "y")
```

### Calling MATLAB from Python
```python
import matlab.engine
eng = matlab.engine.start_matlab()

# Call MATLAB function
result = eng.sqrt(float(16))   # 4.0

# Pass numpy array
import matlab, numpy as np
x = matlab.double(np.arange(10).tolist())
result = eng.sum(x)            # 45.0

eng.quit()
```

---

## MATLAB vs Python: Key Differences

| Concept | MATLAB | Python/NumPy |
|---|---|---|
| Indexing | 1-based | 0-based |
| Semicolons | suppress output | statement separator |
| Array multiply | `.*` element-wise, `*` matrix | `*` element-wise, `@` matrix |
| String delimiters | `'single'` (char) or `"double"` (string) | `'` or `"` both string |
| Comment | `%` | `#` |
| Logical NOT | `~` | `not`, `~` (NumPy) |
| End keyword | needed (`end`) | indentation |
| Default array | column-major (Fortran) | row-major (C) |
| NaN/Inf | `NaN`, `Inf` | `np.nan`, `np.inf` |
| Boolean | `true`/`false` | `True`/`False` |

---

## Useful Diagnostic Commands

```matlab
whos              % list workspace variables with sizes and types
class(x)          % 'double', 'char', 'uint8', etc.
size(x)           % dimensions
isnan(x)          % check for NaN
isinf(x)          % check for Inf
isa(x, 'double')  % type check
exist('var','var')% check if variable exists in workspace
which myFunc      % find which .m file is being called
type myFunc       % display source code of myFunc
edit myFunc       % open myFunc.m in editor
doc function      % open documentation for function
help function     % quick help in command window
lookfor keyword   % search help text for keyword
profile on        % start profiler
profile viewer    % view profiling results
tic; ...; toc     % measure elapsed time
```
