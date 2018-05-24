import pytaf
import numpy as np
a = np.arange(12, dtype=np.float64).reshape((3,4))
b = a * -333
pytaf.clip(a, b, 4)
print(a)
