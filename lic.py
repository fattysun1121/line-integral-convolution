import numpy as np
import matplotlib.pyplot as plt

# generate noise
height, width = 512, 512

mean = 0.0      
std_dev = 1.0

noise = np.random.normal(loc=mean, scale=std_dev, size=(height, width))
normalized_noise = (noise - noise.min()) / (noise.max() - noise.min())

# Display the noise as an image for verification
# plt.imshow(normalized_noise, cmap='gray')
# plt.title("Gaussian Noise")
# plt.colorbar()
# plt.show()
# line integral convolution
# feature: 
# windowing normalization -- stop loop when magnitude of vector is too small