import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import math
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
    same_loc = (x, y, fx, fy)
    tx, ty = math.inf, math.inf
    
    if vx > 0:
        tx = (1 - fx) / vx  # time it takes from fx to 1
    elif vx < 0:
        tx = -fx / vx
    if vy > 0:
        ty = (1 - fy) / vy
    elif vy < 0:
        ty = -fy / vy

    newx, newy, newfx, newfy= 0,0,0,0

    if math.isinf(tx) and math.isinf(ty):
        return same_loc 
 
    if tx > ty:
        if vy > 0:
            newx = x
            newy = y + 1
            newfy = 0
        else: 
            newx = x
            newy = y - 1
            newfy = 1
        newfx = ty * vx
      
    else:  # tx < ty
        if vx > 0:
            newx = x + 1
            newy = y
            newfx = 0
        else: 
            newx = x - 1
            newy = y
            newfx = 1
        newfy = tx * vy


    # Check bounds
    if newx >= w or newx < 0:
        return same_loc 
    elif newy >= h or newy < 0:
        return same_loc
    else:
        return (newx, newy, newfx, newfy)
    
    






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
            k = l // 2 + 1  # +1 to avoid starting being added twice
            
            while k < l:
                out_img[i][j] += kernal[k] * normalized_noise[y][x]
                prevx = x
                prevy = y
                x, y, fx, fy = _step(vx, vy, x, y, fx, fy, width, height)
                # Line not advancing
                if prevx == x and prevy == y:
                    break
                k += 1

            # Move backward
            x = j
            y = i
            vx, vy = vector_field[y][x]
            fx, fy = 0.5, 0.5  # starts from center of pixel
            k = l // 2

            while k >= 0:
                out_img[i][j] += kernal[k] * normalized_noise[y][x]

                prevx = x
                prevy = y
                x, y, fx, fy = _step(-vx, -vy, x, y, fx, fy, width, height)
                if prevx == x and prevy == y:
                    break
                k -= 1
    out_img /= (l * 1)  # due to box filter
    plt.imshow(out_img, cmap='gray')
    plt.show()

if __name__ == '__main__':
    res = (256, 256)  # height, width

    # Generate mock vector field
    vtr_f = np.zeros(shape=res, dtype=tuple)
    for y in range(res[0]):
        for x in range(res[1]):
            vtr_f[y][x] = (x, y)

    lic(vector_field=vtr_f, resolution=res, length=16)
