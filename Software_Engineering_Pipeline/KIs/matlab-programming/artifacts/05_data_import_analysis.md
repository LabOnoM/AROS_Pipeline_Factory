# MATLAB Data Import and Analysis

**Source:** https://www.mathworks.com/help/matlab/data-import-and-analysis.html  
**Version:** R2026a

> Access data from text files, spreadsheets, hardware, other software, or the web. Explore data to identify trends, test hypotheses, and estimate uncertainty.

---

## 1. Data Import

### 1.1 Spreadsheets and Text
```matlab
% Excel files
T = readtable('data.xlsx');                    % read entire sheet
T = readtable('data.xlsx', 'Sheet', 'Sheet2'); % specific sheet
T = readtable('data.xlsx', 'Range', 'B2:D10'); % specific range

M = readmatrix('data.xlsx');   % just numeric data
A = readvars('data.xlsx');     % return separate variables

% CSV / delimited text
T = readtable('data.csv');
T = readtable('data.tsv', 'Delimiter', '\t');
T = readtable('data.txt', 'Delimiter', ' ', 'HeaderLines', 3);

% Raw numeric import
M = load('data.txt');          % whitespace-delimited matrix
M = dlmread('data.csv', ',');  % (legacy, prefer readmatrix)
M = csvread('data.csv');       % (legacy)

% textscan for complex formats
fid = fopen('data.txt', 'r');
C = textscan(fid, '%s %f %f %f', 'Delimiter', ',', 'HeaderLines', 1);
fclose(fid);
```

### 1.2 MATLAB Binary Files
```matlab
% Save
x = 1:100;
results = struct('x', x, 'y', x.^2);
save('results.mat', 'x', 'results')          % specific vars
save('workspace.mat')                         % everything
save('large.mat', 'bigArray', '-v7.3')       % HDF5 format for >2GB

% Load
data = load('results.mat');    % struct with all saved vars
load('results.mat', 'x')      % load 'x' directly into workspace
whos('-file', 'results.mat')  % peek at file contents without loading
```

### 1.3 Images
```matlab
% Read images
img = imread('photo.tif');           % returns uint8 or uint16 array
info = imfinfo('photo.tif');         % metadata: width, height, bit depth...

% Multi-frame TIF (z-stacks, time series)
info = imfinfo('stack.tif');
n_frames = length(info);
stack = zeros(info(1).Height, info(1).Width, n_frames, 'uint16');
for k = 1:n_frames
    stack(:, :, k) = imread('stack.tif', k);
end

% Write images
imwrite(img, 'output.png')
imwrite(img_uint16, 'output.tif')
imwrite(img, 'output.tif', 'Compression', 'none')        % uncompressed
imwrite(img, 'out.tif', 'Compression', 'lzw')            % LZW compressed

% Write multi-frame TIF
imwrite(stack(:,:,1), 'output.tif');
for k = 2:n_frames
    imwrite(stack(:,:,k), 'output.tif', 'WriteMode', 'append');
end
```

### 1.4 Big Data and Large Files
```matlab
% datastore — lazy loading for large collections
ds = datastore('*.csv');                          % CSV collection
ds = datastore('images/*.tif', 'Type', 'image'); % image collection
ds = datastore('data/*.mat', 'Type', 'mat');      % MAT files

% Read data in chunks
while hasdata(ds)
    chunk = read(ds);   % reads one chunk at a time
    % process chunk...
end

% ImageDatastore for images
imds = imageDatastore('images/', 'FileExtensions', '.tif', ...
                      'LabelSource', 'foldernames');
img = read(imds);            % reads next image
reset(imds);                 % restart

% Tall arrays for datasets larger than RAM
tt = tall(T);               % create tall table
m = mean(tt.ValueColumn);   % deferred computation
m_actual = gather(m);       % triggers actual computation
```

---

## 2. Data Preprocessing

### 2.1 Missing Data
```matlab
% NaN represents missing numeric data
x = [1 NaN 3 4 NaN 6];
isnan(x)                    % [0 1 0 0 1 0]
sum(isnan(x))               % count missing
x(isnan(x)) = 0;            % replace with 0
x = x(~isnan(x));           % remove missing

% For tables
T = rmmissing(T)            % remove rows with any NaN
T = fillmissing(T, 'linear') % interpolate missing values
T = fillmissing(T, 'constant', 0)  % fill with constant
```

### 2.2 Normalization and Scaling
```matlab
% Min-max normalization [0,1]
x_norm = (x - min(x)) / (max(x) - min(x));

% Z-score normalization
x_z = (x - mean(x)) / std(x);

% Clip/clamp values
x_clipped = min(max(x, low), high);

% Remove outliers
x_clean = rmoutliers(x);                          % remove statistical outliers
x_clean = rmoutliers(x, 'percentiles', [5 95]);  % remove outside 5th-95th
```

### 2.3 Filtering and Smoothing
```matlab
% Moving average
y = movmean(x, 5)                 % 5-point moving average
y = movmedian(x, 5)               % 5-point moving median
y = smoothdata(x, 'gaussian', 10) % Gaussian kernel smoothing
y = smoothdata(x, 'loess')        % LOESS smoothing

% Digital filtering (Signal Processing Toolbox)
% Low-pass Butterworth filter
[b, a] = butter(4, Wn);          % 4th order, Wn = normalized cutoff
y_filt = filtfilt(b, a, x);      % zero-phase filtering (no lag)
y_filt = filter(b, a, x);        % causal filtering (has phase lag)
```

### 2.4 Reshaping and Restructuring
```matlab
% Stack/unstack
A_flat = A(:);                    % flatten to column vector  
A_reshaped = reshape(A, m, n);   % reshape (column-major)

% Squeeze: remove singleton dimensions
B = squeeze(A);                   % e.g., 1×3×4 → 3×4

% Permute dimensions
B = permute(A, [2 1 3]);          % swap dims 1 and 2 (like transpose for 3D)

% For tables
T_long = stack(T, {'Var1','Var2','Var3'}, 'NewDataVariableName', 'Value')
T_wide = unstack(T_long, 'Value', 'Condition')
```

---

## 3. Descriptive Statistics

```matlab
% Summary statistics
mean(x)         % arithmetic mean
median(x)       % median
mode(x)         % most frequent value
std(x)          % standard deviation (N-1 denominator)
std(x, 1)       % std with N denominator
var(x)          % variance
iqr(x)          % interquartile range
mad(x)          % mean absolute deviation
skewness(x)     % skewness
kurtosis(x)     % kurtosis

% Grouped operations (splitapply)
groups = [1 1 2 2 1 2];
group_means = splitapply(@mean, x, groups);

% Table operations
grpstats(T, 'GroupVar', {@mean, @std})  % grouped stats
varfun(@mean, T, 'GroupingVariables', 'Category')

% Correlation
R = corrcoef(X)    % correlation matrix (returns with p-values too)
[R, P] = corrcoef(X)  % R: correlations, P: p-values
```

---

## 4. Data Exploration

### 4.1 Interactive Apps (no code needed)
- **Import Tool**: `uiimport` — GUI to import varied file types
- **Variable Editor**: double-click variable in Workspace
- **Data Browser**: explore datasets in app
- **Statistics and Machine Learning Toolbox**: `classificationLearner`, `regressionLearner`

### 4.2 Programmatic Exploration
```matlab
% Quick inspection
head(T)                % first 8 rows of table
tail(T)                % last 8 rows
summary(T)             % variable-by-variable stats
T.Properties           % metadata about table

% Profile: which parts take longest
profile on
myFunction();
profile viewer         % interactive graphical view
profile off
```

---

## 5. Image-Specific Analysis (Image Processing Toolbox)

```matlab
% Conversion
img_gray  = rgb2gray(img_rgb);      % RGB → grayscale
img_double = im2double(img_uint8);  % uint8 → double [0,1]
img_uint8  = im2uint8(img_double);  % double → uint8
img_uint16 = im2uint16(img_double); % double → uint16

% Basic measurements
mean2(img)              % mean of all pixels
std2(img)               % std of all pixels

% Thresholding
thresh = graythresh(img);           % Otsu's method
bw = imbinarize(img, thresh);       % apply threshold
bw = imbinarize(img, 'adaptive');   % adaptive local threshold

% Region properties
cc = bwconncomp(bw);                % connected component labeling
stats = regionprops(cc, 'Area', 'Centroid', 'BoundingBox', 'Eccentricity');
areas = [stats.Area];
centroids = vertcat(stats.Centroid);

% Background subtraction / flat-field correction
background = imgaussfilt(img, 50);  % large sigma = background estimate
corrected = double(img) ./ double(background);

% Morphological operations
se = strel('disk', 5);            % structuring element
img_eroded = imerode(bw, se);
img_dilated = imdilate(bw, se);
img_opened = imopen(bw, se);      % erosion then dilation
img_closed = imclose(bw, se);     % dilation then erosion
```
