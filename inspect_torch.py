import traceback
import sys

print('Python executable:', sys.executable)
try:
    import torch
    print('Imported torch:', getattr(torch, '__file__', 'no __file__'), 'version=', getattr(torch, '__version__', 'unknown'))
except Exception as e:
    print('Error importing torch:')
    traceback.print_exc()

try:
    import torchvision
    print('Imported torchvision:', getattr(torchvision, '__file__', 'no __file__'), 'version=', getattr(torchvision, '__version__', 'unknown'))
except Exception as e:
    print('Error importing torchvision:')
    traceback.print_exc()

# Also print site-packages paths
import site
print('Site-packages:', site.getsitepackages() if hasattr(site, 'getsitepackages') else site.getusersitepackages())
