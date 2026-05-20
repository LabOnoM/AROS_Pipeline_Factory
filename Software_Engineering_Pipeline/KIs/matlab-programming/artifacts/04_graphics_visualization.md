# MATLAB Graphics and Visualization

**Source:** https://www.mathworks.com/help/matlab/graphics.html  
**Version:** R2026a

> Graphics functions include 2-D and 3-D plotting to visualize data and communicate results. Customize plots either interactively or programmatically.

---

## 1. Basic 2-D Plotting

```matlab
x = linspace(0, 2*pi, 100);
y = sin(x);

% Basic line plot
figure;                   % open new figure window
plot(x, y)                % simple line plot

% Styling
plot(x, y, 'r--o')        % red dashed line with circle markers
                           % 'b' blue, 'g' green, 'k' black, 'm' magenta
                           % '-' solid, '--' dashed, ':' dotted, '-.' dash-dot
                           % 'o' circle, '*' star, 's' square, '^' triangle, '.' point

% Multiple lines in one call
plot(x, sin(x), 'b-', x, cos(x), 'r--');

% Hold on: add to existing plot without replacing
hold on
plot(x, tan(x), 'g:')
hold off

% Labels and title
xlabel('x (radians)')
ylabel('Amplitude')
title('Sine and Cosine')
legend('sin(x)', 'cos(x)')

% Grid and limits
grid on
xlim([0, 2*pi])
ylim([-1.5, 1.5])
```

---

## 2. Plot Types

### 2.1 Common 2-D Plots
```matlab
% Scatter plot
scatter(x, y)
scatter(x, y, sz, c)         % size and color arrays

% Bar chart
bar(categories, values)
bar(values, 'FaceColor', 'blue')
barh(values)                  % horizontal bars

% Histogram
histogram(data)               % auto-binning
histogram(data, 20)           % 20 bins
histogram(data, 'BinEdges', 0:10:100)

% Pie chart
pie(values, {'Label1', 'Label2', 'Label3'})

% Error bars
errorbar(x, y, err)           % symmetric error bars
errorbar(x, y, lower, upper)  % asymmetric

% Area plot
area(x, y)

% Step plot
stairs(x, y)

% Stem plot
stem(x, y)

% Semilog plots
semilogy(x, y)    % log y-axis
semilogx(x, y)   % log x-axis
loglog(x, y)     % both log
```

### 2.2 3-D Plots
```matlab
% 3D line plot
plot3(x, y, z)

% Surface plot (requires meshgrid)
[X, Y] = meshgrid(-2:0.1:2, -2:0.1:2);
Z = X .* exp(-X.^2 - Y.^2);

surf(X, Y, Z)             % 3D surface
surfc(X, Y, Z)            % surface + contour projection
mesh(X, Y, Z)             % wireframe surface
meshc(X, Y, Z)            % wireframe + contour

% Contour plots
contour(X, Y, Z)          % 2D contour lines
contour(X, Y, Z, 20)      % 20 contour levels
contourf(X, Y, Z)         % filled contours
contour3(X, Y, Z)         % 3D contour lines

% Color control
colormap(jet)             % set colormap (jet, hot, cool, gray, viridis...)
colorbar                  % show color scale

% 3D rotation and view
view(45, 30)              % azimuth=45, elevation=30 degrees
view(3)                   % default 3D view
view(2)                   % top-down (2D equivalent)
```

### 2.3 Image Display
```matlab
img = imread('photo.tif');

% Display image
imshow(img)                % auto-scale, best for images
imagesc(data)              % scale to use full colormap
image(data)                % no scaling

% Display with axes
imagesc(xvec, yvec, data);  % specify axis coordinates
colorbar
axis equal                   % equal aspect ratio
axis tight                   % tight axis limits

% Multiple images
subplot(1, 2, 1), imshow(img1), title('Before')
subplot(1, 2, 2), imshow(img2), title('After')

% Overlay: display image then add plot on top
imshow(img); hold on;
plot(cx, cy, 'r+', 'MarkerSize', 10);
hold off;
```

---

## 3. Subplots and Multiple Figures

```matlab
% Create a grid of subplots
figure('Position', [100, 100, 1200, 800]);  % [left, bottom, width, height]
subplot(2, 3, 1)    % 2 rows, 3 cols, plot 1
plot(x, y1)
title('Plot 1')

subplot(2, 3, 2)
plot(x, y2)
title('Plot 2')

subplot(2, 3, [3 6])   % span positions 3 and 6 (tall right)
surf(X, Y, Z)

% tiledlayout (modern, R2019b+)
figure;
t = tiledlayout(2, 2, 'TileSpacing', 'compact', 'Padding', 'compact');
nexttile; plot(x, sin(x));
nexttile; plot(x, cos(x));
nexttile([1 2]); surf(X, Y, Z);  % span 2 tiles
title(t, 'My Figure')
xlabel(t, 'Shared X Label')
```

---

## 4. Labels, Styling, and Annotations

```matlab
% Text properties using name-value pairs
title('My Title', 'FontSize', 16, 'FontWeight', 'bold')
xlabel('Time (s)', 'FontSize', 12)
ylabel('Amplitude', 'FontSize', 12)

% Text annotations
text(2, 0.5, 'Label here', 'FontSize', 10, 'Color', 'red')
annotation('arrow', [0.3 0.5], [0.5 0.7])  % figure-relative coords

% Axis properties
ax = gca;                          % get current axes
ax.FontSize = 12;
ax.XTick = 0:pi/2:2*pi;
ax.XTickLabel = {'0', '\pi/2', '\pi', '3\pi/2', '2\pi'};  % LaTeX in labels
ax.Box = 'on';
ax.LineWidth = 1.5;

% Legend customization
lg = legend('Signal 1', 'Signal 2');
lg.Location = 'northeast';
lg.FontSize = 11;

% Color control
set(gca, 'Color', [0.95 0.95 0.95])  % gray background
```

---

## 5. Saving and Exporting Figures

```matlab
% Save as various formats
saveas(gcf, 'plot.png')             % PNG (use for raster)
saveas(gcf, 'plot.pdf')             % PDF (vector)
saveas(gcf, 'plot.svg')             % SVG (vector)
saveas(gcf, 'plot.fig')             % MATLAB figure (editable)

% High-quality export with print
print(gcf, 'plot', '-dpng', '-r300')     % 300 DPI PNG
print(gcf, 'plot', '-dpdf')              % PDF
print(gcf, 'plot', '-dsvg')             % SVG

% exportgraphics (R2020a+, most reliable)
exportgraphics(gcf, 'plot.png', 'Resolution', 300)
exportgraphics(gcf, 'plot.pdf', 'ContentType', 'vector')
exportgraphics(gcf, 'plot.tif', 'Resolution', 600)
```

---

## 6. Graphics Objects and Handles

Every graphical element is an object with properties.

```matlab
% Get and modify line properties
h = plot(x, y);
h.Color = [0.2 0.6 0.9];    % RGB color
h.LineWidth = 2;
h.MarkerSize = 8;

% Get axes handle
ax = gca;                    % current axes
fig = gcf;                   % current figure

% Set figure size programmatically
fig = figure;
fig.Position = [100 100 800 600];  % [x y width height]

% Surface properties
s = surf(X, Y, Z);
s.EdgeColor = 'none';        % remove mesh edges
s.FaceAlpha = 0.8;           % transparency (0=transparent, 1=opaque)

% Axis handle for loop
figs = findall(0, 'Type', 'figure');  % find all figure windows
close all;                             % close all figures
clf;                                   % clear current figure
cla;                                   % clear current axes
```

---

## 7. Animation

```matlab
% Simple animation loop
figure;
h = plot(NaN, NaN);
xlim([0 2*pi]); ylim([-1.1 1.1]); grid on;

for t = linspace(0, 2*pi, 100)
    h.XData = 0:0.01:t;
    h.YData = sin(0:0.01:t);
    drawnow;
    pause(0.02);
end

% Save as GIF
filename = 'animation.gif';
for k = 1:50
    % ...update plot...
    frame = getframe(gcf);
    img = frame2im(frame);
    [imind, cm] = rgb2ind(img, 256);
    if k == 1
        imwrite(imind, cm, filename, 'gif', 'Loopcount', inf, 'DelayTime', 0.05);
    else
        imwrite(imind, cm, filename, 'gif', 'WriteMode', 'append', 'DelayTime', 0.05);
    end
end
```
