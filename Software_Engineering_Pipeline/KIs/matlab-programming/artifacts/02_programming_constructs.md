# MATLAB Programming Constructs

**Source:** https://www.mathworks.com/help/matlab/programming-and-data-types.html  
**Version:** R2026a

> When you have a sequence of commands to perform repeatedly or that you want to save for future reference, store them in a **program file**. The simplest type is a **script**; for flexibility create **functions**; for specialized data structures use **classes**.

---

## 1. Scripts

A script is a plain `.m` file containing MATLAB commands, executed sequentially. Scripts share the workspace with the caller.

```matlab
% File: my_analysis.m
clear; clc;       % clean workspace and command window
data = load('measurements.mat');
x = data.x;
y = x .^ 2 + 3 * x;
plot(x, y);
title('My Analysis');
```

Run from command window: `my_analysis` or `run('my_analysis.m')`

**Best practice:** Always start scripts with `clear; clc;` for reproducibility.

---

## 2. Functions

Functions are `.m` files that accept inputs and return outputs. They have their **own workspace**.

### 2.1 Basic Function Structure
```matlab
% File: quadratic.m  (filename MUST match function name)
function [root1, root2] = quadratic(a, b, c)
%QUADRATIC  Solve quadratic equation a*x^2 + b*x + c = 0
%   [r1, r2] = QUADRATIC(a, b, c)
%
%   Uses the quadratic formula.

    discriminant = b^2 - 4*a*c;
    root1 = (-b + sqrt(discriminant)) / (2*a);
    root2 = (-b - sqrt(discriminant)) / (2*a);
end
```

### 2.2 Calling Functions
```matlab
[r1, r2] = quadratic(1, -3, 2);  % r1=2, r2=1
r1 = quadratic(1, -3, 2);        % only capture first output
[~, r2] = quadratic(1, -3, 2);   % ignore first output
```

### 2.3 nargin / nargout — Variable Arguments
```matlab
function result = myFunc(x, scale)
    if nargin < 2
        scale = 1.0;   % default value
    end
    result = x * scale;
end

function [out1, out2] = flexOut(x)
    out1 = x^2;
    if nargout > 1      % only compute if caller requests it
        out2 = x^3;
    end
end
```

### 2.4 varargin / varargout
```matlab
function result = sumAll(varargin)
    result = 0;
    for i = 1:length(varargin)
        result = result + varargin{i};
    end
end

% Call: sumAll(1, 2, 3, 4)  → 10
```

### 2.5 Anonymous Functions (Function Handles)
```matlab
f = @(x) x.^2 + 3*x;      % anonymous function
f(5)                         % 40

g = @(x, y) sqrt(x.^2 + y.^2);  % multiple inputs
g(3, 4)                           % 5

% Capturing variables (closure)
a = 10;
h = @(x) a * x;    % 'a' is captured at creation time
h(5)               % 50
```

### 2.6 Nested Functions
```matlab
function y = outer(x)
    a = 10;
    y = inner(x);   % can call inner

    function z = inner(w)
        z = w + a;  % can access outer's 'a'
    end
end
```

### 2.7 Local Functions (subfunctions)
```matlab
% File: main_analysis.m
function result = main_analysis(data)
    cleaned = cleanData(data);     % calls local function
    result = processData(cleaned);
end

function out = cleanData(in)
    out = in(~isnan(in));    % only visible within this file
end

function out = processData(in)
    out = mean(in);
end
```

---

## 3. Live Scripts and Functions (.mlx)

Live Scripts combine code, output, and formatted text in one document (similar to Jupyter notebooks). Created in MATLAB's Live Editor.

- Run sections independently with `Ctrl+Enter`
- Include formatted text (LaTeX math, images, hyperlinks)
- Export to PDF, HTML, or Word

---

## 4. Classes and Object-Oriented Programming

### 4.1 Value Classes (handle-free)
```matlab
% File: Rectangle.m
classdef Rectangle
    properties
        Width  = 1;
        Height = 1;
    end
    
    methods
        function obj = Rectangle(w, h)
            obj.Width = w;
            obj.Height = h;
        end
        
        function A = area(obj)
            A = obj.Width * obj.Height;
        end
        
        function P = perimeter(obj)
            P = 2 * (obj.Width + obj.Height);
        end
    end
end

% Usage:
r = Rectangle(3, 4);
r.area()           % 12
r.perimeter()      % 14
```

### 4.2 Handle Classes (reference semantics)
```matlab
classdef Counter < handle
    properties
        Count = 0;
    end
    methods
        function increment(obj)
            obj.Count = obj.Count + 1;  % modifies in-place
        end
    end
end

c = Counter();
c.increment();
c.Count   % 1
```

### 4.3 Inheritance
```matlab
classdef ColorRectangle < Rectangle
    properties
        Color = 'blue';
    end
    methods
        function obj = ColorRectangle(w, h, color)
            obj = obj@Rectangle(w, h);  % call superclass constructor
            obj.Color = color;
        end
    end
end
```

---

## 5. Error Handling (try/catch)

```matlab
try
    result = risky_operation(x);
catch ME
    fprintf('Error: %s\n', ME.message);
    fprintf('ID:    %s\n', ME.identifier);
    % ME.stack — call stack info
    result = NaN;  % fallback
end

% Throwing errors
if x < 0
    error('mypackage:badInput', 'x must be non-negative, got %g', x);
end

% Warnings (non-fatal)
warning('mypackage:slowPath', 'Using slow fallback');
```

---

## 6. File I/O

### 6.1 MATLAB Data Files (.mat)
```matlab
% Save variables to .mat file
x = 1:10;
y = x.^2;
save('results.mat', 'x', 'y')         % save specific vars
save('all.mat')                         % save entire workspace

% Load
data = load('results.mat')             % struct with fields x, y
load('results.mat', 'x')              % load only x into workspace
```

### 6.2 Text / CSV
```matlab
% Read CSV (modern)
T = readtable('data.csv');
T = readtable('data.csv', 'Delimiter', '\t');  % TSV

% Write CSV
writetable(T, 'output.csv');

% Read raw numeric data
M = readmatrix('numbers.csv');
writematrix(M, 'output.csv');

% Low-level text I/O
fid = fopen('log.txt', 'w');
fprintf(fid, 'Value: %g\n', 3.14);
fclose(fid);

fid = fopen('log.txt', 'r');
line = fgetl(fid);       % read one line
data = textscan(fid, '%s %f', 'Delimiter', ',');
fclose(fid);
```

### 6.3 Images
```matlab
img = imread('photo.tif');       % read image (uint8 or uint16 array)
info = imfinfo('photo.tif');     % metadata without loading
imwrite(img, 'output.png');      % write image
imwrite(img, 'out.tif', 'Compression', 'none');  % uncompressed TIFF
```

### 6.4 Directory and File Operations
```matlab
% Navigation
pwd                              % current directory
cd('C:\Data')                    % change directory
ls, dir                          % list directory
files = dir('*.tif')             % list matching files

% Loop over files
files = dir('data/*.csv');
for k = 1:numel(files)
    fname = fullfile(files(k).folder, files(k).name);
    T = readtable(fname);
    % process T...
end

% File utilities
fullfile('C:\Data', 'file.mat')  % platform-safe path joining
fileparts('C:\Data\file.mat')    % returns [folder, name, ext]
exist('myfile.mat', 'file')      % check existence
copyfile('src.mat', 'dst.mat')
movefile('old.mat', 'new.mat')
delete('temp.mat')
mkdir('new_folder')
```

---

## 7. Background and Parallel Processing

```matlab
% parfeval — run function in background (non-blocking)
f = parfeval(@myFunction, 1, inputArg);  % 1 output
result = fetchOutputs(f);                 % wait and collect

% parfor — parallel for loop (requires Parallel Computing Toolbox)
parfor i = 1:100
    results(i) = expensiveCalc(i);
end

% Batch job
job = batch(@myScript);   % run in a separate MATLAB session
wait(job);
```

---

## 8. The MATLAB Search Path

```matlab
addpath('C:\MyFunctions')          % add to path (this session)
addpath(genpath('C:\MyLib'))       % add recursively
savepath                            % persist changes
which('myFunc')                     % find which file is called
rmpath('C:\OldFunctions')          % remove from path
```

---

## 9. Useful Debugging and Introspection

```matlab
whos                   % list all workspace variables with sizes/types
class(x)               % 'double', 'char', etc.
isa(x, 'double')       % true/false type check
isnumeric(x)           % true for numeric types
ischar(x)              % true for char arrays
islogical(x)           % true for logical arrays
isempty(x)             % true if size has a zero dimension
isstruct(x)            % true for structs
iscell(x)              % true for cell arrays

% Debugging commands (in Editor)
% Set breakpoints with dbstop
dbstop in myFunc at 10          % break at line 10
dbstop in myFunc if x < 0       % conditional breakpoint
dbcont                          % continue execution
dbstep                          % step one line
dbquit                          % exit debug mode
```
