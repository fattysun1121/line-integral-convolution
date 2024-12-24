import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

'''
@Source 
    https://github.com/alexus37/licplot/blob/master/licplot/lic_internal.pyx

@Parameters
    vx: vector x component
    vy: vector y component
    x: v pixel location on x-axis
    y: v pixel location on y-axis
    fx: position along x in pixel unit square
    fy: position along y in pixel unit square
    w: width
    h: height

@Returns
    tuple [x, y, fx, fy]
'''
def _step(vx: float, vy: float, x: int, y: int, fx: float, fy: float, w:int, h:int) -> tuple[int, int, float, float]:
    pass

def lic(vector_field: npt.NDArray, resolution: tuple[int, int], length: int):
    # Generate standard normal noise
    height, width = resolution
    mean = 0.0
    std_dev = 1.0
    gaussian_noise = np.random.normal(mean, std_dev, size=resolution)
    normalized_noise = (gaussian_noise - gaussian_noise.min()) / (gaussian_noise.max() - gaussian_noise.min())
    out_img = np.zeros(shape=resolution, dtype=float)
    l = length
    kernal = np.ones(l)  # box filter
    for i in range(height):
        for j in range(width):
            # Move forward
            x = j
            y = i
            vx, vy = vector_field[y][x]
            fx, fy = 0.5, 0.5  # starts from center of pixel
            k = l // 2

            while k < l:
                out_img[i][j] += normalized_noise[y][x] * kernal[k]
                x, y, fx, fy = _step(vx, vy, x, y, fx, fy)
                k += 1

            # Move backward
            x = j
            y = i
            vx, vy = vector_field[y][x]
            fx, fy = 0.5, 0.5  # starts from center of pixel
            k = l // 2

            while k >= 0:
                out_img[i][j] += normalized_noise[y][x] * kernal[k]
                x, y, fx, fy = _step(-vx, -vy, x, y, fx, fy)
                k -= 1
    out_img /= (l * 1)


    plt.imshow(out_img, cmap='gray')
    plt.show()

if __name__ == '__main__':
    res = (16, 16)  # height, width

    # Generate mock vector field
    vtr_f = np.zeros(shape=res, dtype=tuple)
    for y in range(res[0]):
        for x in range(res[1]):
            vtr_f[y][x] = (x, y)

    lic(vector_field=vtr_f, resolution=res, length=4)
