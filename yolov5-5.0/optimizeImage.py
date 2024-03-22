from PIL import Image
from PIL import ImageEnhance
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['FangSong'] # 设置字体以便正确显示汉字
plt.rcParams['axes.unicode_minus'] = False # 正确显示连字符

# 原图
image = Image.open('./runs/detect/exp36/plates/0_346_1.jpg')
# 亮度增强
enh_bri = ImageEnhance.Brightness(image)
brightness = 2
image_brightened = enh_bri.enhance(brightness)
# 色度增强(饱和度↑)
enh_col = ImageEnhance.Color(image)
color = 2
image_colored = enh_col.enhance(color)
# 对比度增强
enh_con = ImageEnhance.Contrast(image)
contrast = 2
image_contrasted = enh_con.enhance(contrast)
# 锐度增强
enh_sha = ImageEnhance.Sharpness(image)
sharpness = 4.0
image_sharped = enh_sha.enhance(sharpness)

fig,axes=plt.subplots(nrows=2,ncols=3,figsize=(10,8),dpi=100)
axes[0,0].imshow(np.array(image, dtype=np.uint8)[:,:,::-1])
axes[0,0].set_title("原图")
axes[0,1].imshow(np.array(image_brightened, dtype=np.uint8)[:,:,::-1])
axes[0,1].set_title("亮度增强")
axes[0,2].imshow(np.array(image_colored, dtype=np.uint8)[:,:,::-1])
axes[0,2].set_title("饱和度增强")
axes[1,0].imshow(np.array(image_contrasted, dtype=np.uint8)[:,:,::-1])
axes[1,0].set_title("对比度增强")
axes[1,1].imshow(np.array(image_sharped, dtype=np.uint8)[:,:,::-1])
axes[1,1].set_title("锐度增强")
axes[1,2].imshow(np.array(image_sharped, dtype=np.uint8)[:,:,::-1])
axes[1,2].set_title("锐度增强")
plt.show()
