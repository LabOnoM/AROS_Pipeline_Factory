# MATLAB Language Fundamentals

**Source:** https://www.mathworks.com/help/matlab/language-fundamentals.html  
**Version:** R2026a

> MATLAB is an abbreviation for "matrix laboratory." While other programming languages work with numbers one at a time, MATLAB operates on **whole matrices and arrays** — this is its primary distinguishing characteristic.

---

## 1. Core Philosophy

| Concept | Detail |
|---|---|
| Default data structure | 2-D matrix (even scalars are 1×1 matrices) |
| 1-indexed | Arrays start at index 1, NOT 0 |
| Column-major | Stored column-by-column in memory |
| Semicolons suppress output | `x = 5;` suppresses echo; `x = 5` prints it |
| `%` for comments | `% this is a comment` |

---

## 2. Entering Commands

```matlab
% Arithmetic in the command window (results auto-displayed)
2 + 2          % ans = 4
sqrt(16)       % ans = 4
pi             % 3.1416 (built-in constant)

% Suppress output with semicolon
x = 42;        % assigns x but does not print

% Display explicitly
disp(x)        % prints value without variable name
fprintf('Value: %d\n', x)  % formatted output

% Multi-line statements using ...
result = 1 + 2 + ...
         3 + 4;
```

---

## 3. Matrices and Arrays

### 3.1 Creating Arrays
```matlab
% Row vector
v = [1 2 3 4 5]          % space-separated
v = [1, 2, 3, 4, 5]      % comma-separated (equivalent)

% Column vector
c = [1; 2; 3; 4; 5]      % semicolons create new rows

% Matrix (2x3)
A = [1 2 3; 4 5 6]       % rows separated by semicolons

% Ranges with colon operator
r = 1:5                   % [1 2 3 4 5]
r = 1:2:10                % [1 3 5 7 9] (step of 2)
r = linspace(0, 1, 5)    % [0 0.25 0.5 0.75 1] (5 evenly spaced)

% Special matrices
Z = zeros(3, 4)           % 3x4 matrix of zeros
O = ones(2, 2)            % 2x2 matrix of ones
I = eye(4)                % 4x4 identity matrix
R = rand(3)               % 3x3 random values [0,1]
R = randn(3)              % 3x3 standard-normal random
```

### 3.2 Array Indexing
```matlab
A = [10 20 30; 40 50 60; 70 80 90];

% Single element (row, col) — 1-indexed!
A(2, 3)       % 60

% Entire row or column
A(2, :)       % [40 50 60]  (2nd row, all columns)
A(:, 1)       % [10; 40; 70] (1st column, all rows)

% Submatrix
A(1:2, 2:3)   % [20 30; 50 60]

% Linear indexing (column-major order)
A(5)          % 50 (5th element counting down columns)

% End keyword
A(end, :)     % last row
A(1:end-1, :) % all rows except last

% Logical indexing
A(A > 40)     % returns elements > 40 as column vector

% Assignment via index
A(1,1) = 99;

% Delete rows/columns
A(2,:) = [];  % delete 2nd row
```

### 3.3 Array Operations
```matlab
A = [1 2; 3 4];
B = [5 6; 7 8];

% Element-wise vs. matrix operations
A + B         % element-wise addition
A * B         % matrix multiplication
A .* B        % element-wise multiplication
A ./ B        % element-wise division
A .^ 2        % element-wise squaring
A ^ 2         % matrix power A*A

% Transpose
A'            % conjugate transpose
A.'           % plain transpose (non-conjugate)

% Common array functions
size(A)       % [2, 2] — dimensions
size(A, 1)    % 2 — number of rows
size(A, 2)    % 2 — number of columns
length(A)     % max(size(A))
numel(A)      % total number of elements
ndims(A)      % number of dimensions

% Reshape and manipulation
reshape(A, 1, 4)       % [1 3 2 4] — reshapes column-by-column
A(:)                   % flatten to column vector
repmat(A, 2, 3)        % tile A in a 2x3 grid
cat(1, A, B)           % concatenate vertically (dim 1)
cat(2, A, B)           % concatenate horizontally (dim 2)
[A; B]                 % vertical concatenation shorthand
[A, B]                 % horizontal concatenation shorthand

% Sorting
sort(v)                % sort row vector ascending
sort(A, 1)             % sort each column ascending
sort(A, 2, 'descend')  % sort each row descending
[sorted, idx] = sort(v) % also get sort indices

% Finding
find(v > 3)            % indices where condition is true
find(A == 50)          % linear indices
```

---

## 4. Data Types

| Type | Description | Example |
|---|---|---|
| `double` | Default floating-point (64-bit) | `x = 3.14` |
| `single` | Single-precision float (32-bit) | `single(3.14)` |
| `int8/16/32/64` | Signed integers | `int32(5)` |
| `uint8/16/32/64` | Unsigned integers | `uint8(255)` |
| `logical` | Boolean (true/false) | `true`, `false`, `logical(1)` |
| `char` | Character array (string) | `'hello'` |
| `string` | String scalar/array (modern) | `"hello"` |
| `cell` | Cell array (mixed types) | `{1, 'two', [3 4]}` |
| `struct` | Structure | `s.field = value` |
| `table` | Tabular data | `table(...)` |

### 4.1 Strings
```matlab
% Character arrays (old style)
c = 'hello world';
length(c)           % 11
c(1:5)              % 'hello'

% String scalars (modern, preferred)
s = "hello world";
strlength(s)        % 11
s + " more"         % "hello world more" (concatenation)

% Useful string functions
upper("hello")            % "HELLO"
lower("HELLO")            % "hello"
strtrim("  hi  ")         % "hi"
strsplit("a,b,c", ",")    % ["a" "b" "c"]
strjoin(["a","b"], "-")   % "a-b"
contains("hello", "ell")  % true
strfind("hello", "l")     % [3 4]
strrep("hello", "l", "L") % "heLLo"
sprintf("Value: %.2f", pi)% "Value: 3.14"
num2str(3.14)             % '3.14' (char)
str2num('42')             % 42 (double)
str2double("3.14")        % 3.14 (double, safer)
```

### 4.2 Cell Arrays
```matlab
C = {1, 'hello', [1 2 3], true};

% Access with {} for content, () for sub-cell
C{2}          % 'hello' (content)
C(2)          % {'hello'} (1x1 cell)

% Iterate a cell array
for i = 1:numel(C)
    disp(C{i})
end

% Common cell functions
iscell(C)         % true
cellfun(@length, C)  % apply function to each element
cell2mat(C)          % convert (only if all numeric, same size)
```

### 4.3 Structures
```matlab
% Create struct
s.name = 'Alice';
s.age = 30;
s.scores = [95 87 92];

% Struct functions
fieldnames(s)       % {'name'; 'age'; 'scores'}
isfield(s, 'age')   % true
rmfield(s, 'age')   % remove a field
s = struct('x', 1, 'y', 2)  % constructor syntax

% Struct arrays
patients(1).name = 'Bob';
patients(2).name = 'Carol';
[patients.name]     % all names concatenated
{patients.name}     % as cell array
```

### 4.4 Tables
```matlab
% Create table
Name = ["Alice"; "Bob"; "Carol"];
Age = [30; 25; 35];
Score = [95; 87; 92];
T = table(Name, Age, Score);

% Access
T.Age               % Age column as array
T{1, :}             % 1st row as array
T(T.Age > 27, :)    % filter rows

% Table operations
T.NewCol = T.Score * 1.1;  % add column
sortrows(T, 'Age')          % sort by Age
T(2, :) = [];               % delete row
summary(T)                  % descriptive stats
writetable(T, 'out.csv')    % write to CSV
T2 = readtable('data.csv')  % read from CSV
```

---

## 5. Operators and Elementary Operations

### 5.1 Arithmetic
```matlab
+  -  *  /   % standard
^            % power
.*  ./  .^   % element-wise variants for arrays
\            % left division: A\b solves A*x = b
./           % right element-wise division
```

### 5.2 Relational (return logical arrays)
```matlab
==  ~=  <  <=  >  >=
```

### 5.3 Logical
```matlab
&&   % short-circuit AND (scalar)
||   % short-circuit OR (scalar)
&    % element-wise AND (arrays)
|    % element-wise OR (arrays)
~    % NOT
xor(a, b)
```

### 5.4 Special Characters
```matlab
:    % colon — range, slice, linearize
.    % field access in structs; element-wise prefix
...  % line continuation
%    % comment
;    % row separator in arrays; suppress output
,    % element separator; output multiple values
()   % function call / indexing
{}   % cell array indexing
[]   % array construction; ignore outputs with [~,x]
@    % function handle
```

---

## 6. Loops and Conditional Statements

### 6.1 if / elseif / else
```matlab
x = 10;
if x > 0
    disp('positive')
elseif x < 0
    disp('negative')
else
    disp('zero')
end
```

### 6.2 for loop
```matlab
% Over a numeric range
for i = 1:5
    fprintf('%d\n', i);
end

% Over a row vector
for val = [10 20 30]
    disp(val)
end

% Over columns of a matrix
A = [1 2 3; 4 5 6];
for col = A       % iterates over column vectors
    disp(col)
end
```

### 6.3 while loop
```matlab
n = 1;
while n < 10
    n = n * 2;
end
```

### 6.4 switch / case
```matlab
day = 'Mon';
switch day
    case 'Mon'
        disp('Monday')
    case {'Sat', 'Sun'}
        disp('Weekend')
    otherwise
        disp('Weekday')
end
```

### 6.5 break / continue / return
```matlab
for i = 1:10
    if i == 5, break; end      % exit loop
    if mod(i,2)==0, continue; end  % skip iteration
    disp(i)
end
```

### 6.6 The Tilde `~` — Ignoring Outputs
```matlab
% ~ ignores specific output arguments
[~, idx] = sort(v);          % ignore sorted values, keep indices
[~, ~, v] = find(A);         % ignore row/col indices, keep values

% ~ in function signatures
function result = myFun(~, b)  % ignore first argument
    result = b * 2;
end
```

---

## 7. Vectorization (Performance Best Practice)

Avoid explicit loops when possible — use vectorized operations.

```matlab
% Slow: loop
result = zeros(1, 1000);
for i = 1:1000
    result(i) = i^2;
end

% Fast: vectorized
i = 1:1000;
result = i.^2;

% Apply function element-wise: arrayfun
result = arrayfun(@(x) x^2 + log(x), 1:100);

% Logical masking instead of if-loop
v = -5:5;
v(v < 0) = 0;    % clamp negatives to zero
```
