import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

def lic(vector_field: npt.NDArray, resolution: tuple[int, int]):
    # Generate standard normal noise
    width, height = resolution
    mean = 0.0
    std_dev = 1.0
    gaussian_noise = np.random.normal(mean, std_dev, size=(height, width))
    normalized_noise = (gaussian_noise - gaussian_noise.min()) / (gaussian_noise.max() - gaussian_noise.min())

    #

if __name__ == '__main__':
    res = (32, 32)  # width, height

    # Generate mock vector field
    vtr_f = np.zeros(shape=res, dtype=tuple)
    for y in range(res[1]):
        for x in range(res[0]):
            vtr_f[y][x] = (x, y)

    lic(vector_field=vtr_f, resolution=res)
