import numpy as np
a = np.array(range(1,11))
print(a)
for i in range(len(a)):
    a[i] *= a[i]*10    
print(a)