# MATLAB External Interfaces: Python, C/C++, Java and More

**Sources:**  
- https://www.mathworks.com/help/matlab/external-language-interfaces.html  
- https://www.mathworks.com/products/matlab/getting-started/using-matlab-python.html

---

## 1. MATLAB ↔ Python Integration

MATLAB provides **built-in, bidirectional** support for Python without any third-party tools.

### 1.1 Prerequisites
```matlab
% Check Python configuration
pyenv                          % shows Python version, executable, status
pyenv('Version', '3.10')      % select specific Python version (before first use)
pyenv('ExecutionMode', 'OutOfProcess')  % run Python in separate process (safer)
```

**Supported Python versions:** Check [installation guide](https://www.mathworks.com/help/matlab/matlab_external/install-supported-python-implementation.html) for the version matrix per MATLAB release.

---

### 1.2 Calling Python from MATLAB

The `py.` prefix provides direct access to any Python module.

```matlab
% Call built-in Python functions
x = py.math.sqrt(42)
y = py.len([1, 2, 3])
s = py.str.upper("hello")

% Import and use a module
np = py.importlib.import_module('numpy');
arr = np.array([1.0, 2.0, 3.0]);

% Call user-defined Python function
% Given: my_module.py in Python path with function process(data)
result = py.my_module.process(data);

% Reload Python module after editing
clear classes
py.importlib.reload(py.my_module);

% Run a Python script or expression with pyrun
pyrun("import numpy as np; result = np.sqrt(16)")
pyrun("x = [1, 2, 3]")
x_matlab = pyrun("x = [1, 2, 3]", "x");  % capture output

% Run Python file
pyrunfile("my_script.py")
pyrunfile("my_script.py", "output_var")
```

### 1.3 Data Type Mapping: MATLAB → Python

| MATLAB Type | Python Type | Notes |
|---|---|---|
| `double scalar` | `float` | Auto-converted |
| `double array` | `numpy.ndarray` | Via `py.numpy.array()` |
| `char / string` | `str` | Auto-converted |
| `logical` | `bool` | Auto-converted |
| `int32` | `int` | Auto-converted |
| `cell array` | `list` | `py.list({1,'a',true})` |
| `struct` | `dict` | `py.dict(pyargs('a',1,'b',2))` |
| `table` | `pandas.DataFrame` | Requires explicit conversion |

```matlab
% Passing MATLAB arrays to Python (numpy)
M = [1 2 3; 4 5 6];
py_array = py.numpy.array(M);    % convert to numpy array

% Convert Python numpy array back to MATLAB
M_back = double(py_array);

% Passing a MATLAB table to Python as pandas DataFrame (manual)
% Step 1: convert to numeric matrix
M = table2array(T(:, varclasses == "double"));
py_df = py.pandas.DataFrame(py.numpy.array(M));
```

### 1.4 Calling MATLAB from Python

**Install the engine:**
```bash
# From MATLAB's Engine API directory
cd "C:\Program Files\MATLAB\R2026a\extern\engines\python"
python setup.py install
```

```python
# Python side
import matlab.engine

eng = matlab.engine.start_matlab()           # start MATLAB
eng = matlab.engine.connect_matlab()         # connect to existing session

# Call MATLAB function
result = eng.sqrt(4.0)                       # 2.0
arr = eng.zeros(3, 3)                        # 3x3 zeros matrix

# Pass data
import matlab
x = matlab.double([1.0, 2.0, 3.0])          # MATLAB double array
result = eng.sum(x)                          # 6.0

# Call user function (my_func.m must be on MATLAB path)
out = eng.my_func(arg1, arg2, nargout=2)    # 2 outputs

# Run MATLAB scripts
eng.run('my_script.m', nargout=0)

# Async background call
future = eng.my_slow_func(x, background=True)
result = future.result()                     # blocks until done

eng.quit()
```

### 1.5 Deep Learning Model Exchange
```matlab
% Import pretrained models
net = importONNXNetwork('model.onnx');             % ONNX
net = importTensorFlowNetwork('tf_model_dir');     % TensorFlow SavedModel
net = importPyTorchNetwork('model.pt', InputSize=[28 28 1]);  % PyTorch

% Export MATLAB network to other formats
exportONNXNetwork(net, 'exported.onnx');
exportTensorFlowNetwork(net, 'output_dir');
```

### 1.6 Using MATLAB from Jupyter / VS Code
- **Jupyter**: Install `jupyter-matlab-proxy` package; access MATLAB from Jupyter notebooks
- **VS Code**: Install MATLAB extension from MathWorks; supports syntax highlighting, IntelliSense, and running code

---

## 2. C/C++ with MATLAB

### 2.1 Calling C Libraries from MATLAB (`loadlibrary`)
```matlab
% Load a shared library (.dll on Windows, .so on Linux)
loadlibrary('mylib', 'mylib.h')

% Call a function
result = calllib('mylib', 'my_function', arg1, arg2)

% Unload
unloadlibrary('mylib')

% List available functions
libfunctions('mylib')
libfunctions('mylib', '-full')   % with signatures
```

### 2.2 MEX Files (C/C++ code callable from MATLAB)
MEX files compile C/C++ code into `.mex*` binary format, running at native speed.

```c
// File: my_mex.c
#include "mex.h"

void mexFunction(int nlhs, mxArray *plhs[],
                 int nrhs, const mxArray *prhs[])
{
    // Read input
    double *inData = mxGetDoubles(prhs[0]);
    mwSize n = mxGetNumberOfElements(prhs[0]);
    
    // Create output
    plhs[0] = mxCreateDoubleMatrix(1, n, mxREAL);
    double *outData = mxGetDoubles(plhs[0]);
    
    // Process
    for (mwSize i = 0; i < n; i++) {
        outData[i] = inData[i] * 2.0;
    }
}
```

```matlab
% Compile the MEX file
mex my_mex.c

% Call it like any MATLAB function
result = my_mex([1 2 3 4 5]);  % [2 4 6 8 10]
```

---

## 3. Java with MATLAB

MATLAB includes a built-in JVM, so Java classes are directly accessible.

```matlab
% Create Java objects
sb = java.lang.StringBuilder('hello');
sb.append(' world');
str = char(sb.toString())        % 'hello world'

% Use Java data structures
list = java.util.ArrayList();
list.add(1); list.add(2); list.add(3);
list.size()                      % 3

% File I/O via Java
file = java.io.File('data.txt');
file.exists()

% Custom Java class (add JAR to classpath first)
javaaddpath('mylib.jar')
obj = com.example.MyClass(arg1);
obj.myMethod();
```

---

## 4. .NET with MATLAB (Windows only)

```matlab
% Load a .NET assembly
NET.addAssembly('C:\path\to\myLib.dll');

% Create .NET object
obj = MyNamespace.MyClass(arg1);
result = obj.MyMethod(input);

% Use .NET types
arr = NET.createArray('System.Int32', 5);
```

---

## 5. Web Services / REST APIs

```matlab
% HTTP GET request
response = webread('https://api.example.com/data');
% response is automatically parsed (JSON → struct, XML → struct)

% With options
options = weboptions('Timeout', 10, 'ContentType', 'json');
options.HeaderFields = {'Authorization', 'Bearer mytoken'};
data = webread(url, 'param1', val1, 'param2', val2, options);

% HTTP POST request
response = webwrite(url, data_struct, options);

% Download a file
websave('local_file.csv', 'https://example.com/data.csv');

% RESTful APIs with full control
import matlab.net.*
import matlab.net.http.*
request = RequestMessage('GET');
[response, ~, history] = request.send(URI('https://api.example.com'));
```

---

## 6. Summary: MATLAB External Language Interfaces

| Language | Direction | Key Functions | Notes |
|---|---|---|---|
| Python | MATLAB→Python | `py.*`, `pyrun`, `pyrunfile` | Built-in, no toolbox needed |
| Python | Python→MATLAB | `matlab.engine` | Install Engine API |
| C/C++ | MATLAB→C | `loadlibrary`, `calllib` | Dynamic shared libraries |
| C/C++ | C→MATLAB | MEX files (`mex`) | Native-speed custom functions |
| Java | MATLAB→Java | Direct `java.*` syntax | JVM always available |
| .NET | MATLAB→.NET | `NET.addAssembly` | Windows only |
| Web/REST | MATLAB→HTTP | `webread`, `webwrite` | JSON/XML auto-parsed |
| Fortran | Fortran→MATLAB | MEX files | Legacy support |
