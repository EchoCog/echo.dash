"""
Mock numpy implementation for testing when numpy is not available
Provides minimal interface needed for echo9ml tests
"""

class ndarray:
    """Mock numpy ndarray"""
    def __init__(self, data=None, shape=None, dtype=None):
        if data is not None:
            if isinstance(data, (list, tuple)):
                self._data = list(data)
                if shape is not None:
                    self.shape = shape
                else:
                    self.shape = self._compute_shape(data)
            else:
                self._data = [data]
                self.shape = shape if shape is not None else (1,)
        elif shape is not None:
            self.shape = shape
            self._data = [0.0] * self._compute_size(shape)
        else:
            self._data = []
            self.shape = (0,)
        self.dtype = dtype or float
    
    def _compute_shape(self, data):
        if isinstance(data, (list, tuple)) and len(data) > 0:
            if isinstance(data[0], (list, tuple)):
                return (len(data),) + self._compute_shape(data[0])
            else:
                return (len(data),)
        return (0,)
    
    def _compute_size(self, shape):
        size = 1
        for dim in shape:
            size *= dim
        return size
    
    def copy(self):
        new_array = ndarray()
        new_array._data = self._data.copy()
        new_array.shape = self.shape
        new_array.dtype = self.dtype
        return new_array
    
    def __getitem__(self, key):
        # Simplified indexing for multi-dimensional arrays
        if isinstance(key, int):
            if len(self.shape) == 1:
                return self._data[key]
            else:
                # Return a sub-array for multi-dimensional access
                new_shape = self.shape[1:]
                new_size = self._compute_size(new_shape)
                start_idx = key * new_size
                end_idx = start_idx + new_size
                sub_data = self._data[start_idx:end_idx]
                sub_array = ndarray()
                sub_array._data = sub_data
                sub_array.shape = new_shape
                sub_array.dtype = self.dtype
                return sub_array
        elif isinstance(key, tuple):
            # Handle multi-dimensional indexing
            if any(k is None for k in key):
                # Handle None (newaxis) - just return self for simplicity
                return self
            return self._get_multi_index(key)
        elif isinstance(key, slice) and key == slice(None):
            # Handle [:] - return full array
            return self
        return self
    
    def _get_multi_index(self, indices):
        """Handle multi-dimensional indexing with slices"""
        # Handle slices - for now, return a simple sub-array
        if any(isinstance(idx, slice) for idx in indices):
            # Simplified slice handling - return self for slices
            return self
        
        flat_index = 0
        multiplier = 1
        for i in reversed(range(len(indices))):
            if i < len(self.shape):
                flat_index += indices[i] * multiplier
                multiplier *= self.shape[i]
        
        if flat_index < len(self._data):
            return self._data[flat_index]
        return 0.0
    
    def __setitem__(self, key, value):
        if isinstance(key, int):
            if len(self.shape) == 1 and key < len(self._data):
                self._data[key] = value
            else:
                # Handle multi-dimensional assignment arr[0] = new_array
                if hasattr(value, '_data'):
                    # Calculate the size of one "slice" 
                    sub_size = self._compute_size(self.shape[1:])
                    start_idx = key * sub_size
                    end_idx = start_idx + min(sub_size, len(value._data))
                    # Update the data
                    for i in range(min(sub_size, len(value._data))):
                        if start_idx + i < len(self._data):
                            self._data[start_idx + i] = value._data[i]
                else:
                    # Setting a scalar value
                    sub_size = self._compute_size(self.shape[1:])
                    start_idx = key * sub_size
                    for i in range(sub_size):
                        if start_idx + i < len(self._data):
                            self._data[start_idx + i] = value
        elif isinstance(key, tuple):
            # Handle multi-dimensional indexing for setting
            flat_index = 0
            multiplier = 1
            for i in reversed(range(len(key))):
                if i < len(self.shape):
                    flat_index += key[i] * multiplier
                    multiplier *= self.shape[i]
            
            if flat_index < len(self._data):
                self._data[flat_index] = value
    
    def __bool__(self):
        return len(self._data) > 0
    
    def __add__(self, other):
        """Addition operation"""
        result = self.copy()
        if hasattr(other, '_data'):
            for i in range(min(len(result._data), len(other._data))):
                result._data[i] += other._data[i]
        else:
            result._data = [x + other for x in result._data]
        return result
    
    def __mul__(self, other):
        """Multiplication operation"""
        result = self.copy()
        if hasattr(other, '_data'):
            for i in range(min(len(result._data), len(other._data))):
                result._data[i] *= other._data[i]
        else:
            result._data = [x * other for x in result._data]
        return result
    
    def __rmul__(self, other):
        """Right multiplication operation (scalar * array)"""
        return self.__mul__(other)
    
    def __sub__(self, other):
        """Subtraction operation"""
        result = self.copy()
        if hasattr(other, '_data'):
            for i in range(min(len(result._data), len(other._data))):
                result._data[i] -= other._data[i]
        else:
            result._data = [x - other for x in result._data]
        return result
    
    def __ge__(self, other):
        """Greater than or equal operation"""
        result = self.copy()
        if hasattr(other, '_data'):
            result._data = [x >= y for x, y in zip(result._data, other._data)]
        else:
            result._data = [x >= other for x in result._data]
        return result
    
    def __le__(self, other):
        """Less than or equal operation"""  
        result = self.copy()
        if hasattr(other, '_data'):
            result._data = [x <= y for x, y in zip(result._data, other._data)]
        else:
            result._data = [x <= other for x in result._data]
        return result
    
    def __gt__(self, other):
        """Greater than operation"""
        result = self.copy()
        if hasattr(other, '_data'):
            result._data = [x > y for x, y in zip(result._data, other._data)]
        else:
            result._data = [x > other for x in result._data]
        return result

def zeros(shape, dtype=None):
    """Mock numpy.zeros"""
    return ndarray(shape=shape, dtype=dtype)

def array(data, dtype=None):
    """Mock numpy.array"""
    return ndarray(data=data, dtype=dtype)

def mean(arr, axis=None):
    """Mock numpy.mean with axis support"""
    if isinstance(arr, list) and len(arr) > 0 and hasattr(arr[0], '_data'):
        # Handle list of ndarrays (like history tensors)
        if axis == 0:
            # Average across the first dimension (list of arrays)
            if not arr:
                return ndarray([])
            # Create average by element-wise mean
            result_data = []
            min_len = min(len(a._data) for a in arr)
            for i in range(min_len):
                avg_val = sum(a._data[i] for a in arr) / len(arr)
                result_data.append(avg_val)
            result = ndarray(data=result_data, shape=arr[0].shape)
            return result
        else:
            # Fall back to simple mean
            all_data = []
            for a in arr:
                if hasattr(a, '_data'):
                    all_data.extend(a._data)
            return sum(all_data) / len(all_data) if all_data else 0.0
    elif hasattr(arr, '_data'):
        if axis is None:
            return sum(arr._data) / len(arr._data) if arr._data else 0.0
        elif isinstance(axis, tuple) and arr.shape and len(arr.shape) > 1:
            # For multi-dimensional axis like (1, 2, 3) on shape (7, 13, 5, 2)
            # We want to average over the specified axes, keeping the others
            if axis == (1, 2, 3) and len(arr.shape) == 4:
                # Average over dimensions 1, 2, 3, keeping dimension 0 (7 traits)
                trait_means = []
                dim0_size = arr.shape[0]  # Number of traits (7)
                elements_per_trait = 1
                for i in range(1, len(arr.shape)):
                    elements_per_trait *= arr.shape[i]
                
                for trait_idx in range(dim0_size):
                    start_idx = trait_idx * elements_per_trait
                    end_idx = start_idx + elements_per_trait
                    trait_data = arr._data[start_idx:end_idx]
                    trait_mean = sum(trait_data) / len(trait_data) if trait_data else 0.0
                    trait_means.append(trait_mean)
                
                return ndarray(data=trait_means, shape=(dim0_size,))
            else:
                # For other multi-dimensional cases, just return simple mean
                return sum(arr._data) / len(arr._data) if arr._data else 0.0
        elif isinstance(axis, int):
            # For single axis, just return simple mean for now  
            return sum(arr._data) / len(arr._data) if arr._data else 0.0
    elif isinstance(arr, (list, tuple)):
        return sum(arr) / len(arr) if arr else 0.0
    else:
        return arr

def std(arr):
    """Mock numpy.std (standard deviation)"""
    if hasattr(arr, '_data'):
        data = arr._data
    else:
        data = arr if isinstance(arr, (list, tuple)) else [arr]
    
    if len(data) <= 1:
        return 0.0
    
    mean_val = sum(data) / len(data)
    variance = sum((x - mean_val) ** 2 for x in data) / len(data)
    return variance ** 0.5

def all(arr):
    """Mock numpy.all"""
    if hasattr(arr, '_data'):
        return all(bool(x) for x in arr._data)
    elif isinstance(arr, (list, tuple)):
        return all(bool(x) for x in arr)
    else:
        return bool(arr)

def array_equal(a1, a2):
    """Mock numpy.array_equal"""
    if hasattr(a1, '_data') and hasattr(a2, '_data'):
        return a1._data == a2._data
    return a1 == a2

def clip(arr, min_val, max_val):
    """Mock numpy.clip"""
    if hasattr(arr, '_data'):
        clipped_data = [max(min_val, min(max_val, x)) for x in arr._data]
        result = ndarray()
        result._data = clipped_data
        result.shape = arr.shape
        result.dtype = arr.dtype
        return result
    return max(min_val, min(max_val, arr))

def where(condition, x, y):
    """Mock numpy.where"""
    if hasattr(condition, '_data'):
        result_data = []
        for i, c in enumerate(condition._data):
            if c:
                result_data.append(x._data[i] if hasattr(x, '_data') else x)
            else:
                result_data.append(y._data[i] if hasattr(y, '_data') else y)
        result = ndarray()
        result._data = result_data
        result.shape = condition.shape
        return result
    return x if condition else y

def random_normal(size=None):
    """Mock numpy random normal distribution"""
    import random
    if size is None:
        return random.gauss(0, 1)
    if isinstance(size, int):
        return [random.gauss(0, 1) for _ in range(size)]
    # For tuple sizes, create nested structure
    result = []
    total_size = 1
    for dim in size:
        total_size *= dim
    data = [random.gauss(0, 1) for _ in range(total_size)]
    return ndarray(data=data, shape=size)

# Random module mock
class random:
    @staticmethod
    def normal(loc=0, scale=1, size=None):
        import random as pyrand
        if size is None:
            return pyrand.gauss(loc, scale)
        if isinstance(size, int):
            data = [pyrand.gauss(loc, scale) for _ in range(size)]
            return ndarray(data=data, shape=(size,))
        elif isinstance(size, tuple):
            # For tuple sizes - calculate total size correctly
            total_size = 1
            for dim in size:
                total_size *= dim
            data = [pyrand.gauss(loc, scale) for _ in range(total_size)]
            return ndarray(data=data, shape=size)
        else:
            # Assume it's an ndarray shape
            if hasattr(size, 'shape'):
                total_size = 1
                for dim in size.shape:
                    total_size *= dim
                data = [pyrand.gauss(loc, scale) for _ in range(total_size)]
                return ndarray(data=data, shape=size.shape)
            return pyrand.gauss(loc, scale)

def save(filename, arr):
    """Mock numpy.save"""
    import json
    if hasattr(arr, '_data'):
        data = {
            'data': arr._data,
            'shape': arr.shape,
            'dtype': str(arr.dtype)
        }
    else:
        data = {'data': [arr], 'shape': (1,), 'dtype': str(type(arr))}
    
    with open(filename, 'w') as f:
        json.dump(data, f)

def load(filename):
    """Mock numpy.load"""
    import json
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return ndarray(data=data['data'], shape=tuple(data['shape']))
    except:
        return ndarray([])

# Float types
float32 = float
float64 = float