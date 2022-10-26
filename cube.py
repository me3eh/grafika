import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.size'] = 14
plt.rcParams['toolbar'] = 'None'

def midpoints(x):
    sl = ()
    print(x.ndim)
    for i in range(x.ndim):
        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
        # print(x)
        sl += np.index_exp[:]
        # print('plug', sl)
    return x

r, g, b = np.indices((18, 18, 18)) / 18.0
# print('zielen', r)
# print(g)
rc = midpoints(r)
gc = midpoints(g)
bc = midpoints(b)

sphere = rc > -1
print(sphere.shape)
colors = np.zeros(sphere.shape + (3,))
print(colors)
colors[..., 2] = rc
colors[..., 0] = gc
colors[..., 1] = bc

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111, projection='3d')
ax.voxels(r, g, b, sphere,
          facecolors=colors,
          shade=False)
ax.grid(False)
ax.axis('off')

plt.show()
