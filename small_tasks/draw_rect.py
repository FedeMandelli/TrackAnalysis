# imports
import cv2
import os

# settings
color = (255, 255, 255)
width = 10

# load image
path = r"C:\Users\Federico\Desktop\exp 1\large(2) vs small"

for img in os.listdir(path):
    if img.endswith('jpg'):
        # load image
        cv2image = cv2.imread(os.path.join(path, img))
        
        # draw rectangles
        # small sx
        rect_xy_sx = cv2.rectangle(cv2image, (1305, 1950), (1590, 1630), color, width)
        rect_yz_sx = cv2.rectangle(rect_xy_sx, (5465, 3920), (5690, 3880), color, width)
        rect_xz_sx = cv2.rectangle(rect_yz_sx, (7415, 3855), (7785, 3780), color, width)
        
        # large dx
        rect_xy = cv2.rectangle(rect_xz_sx, (1995, 2235), (2435, 1630), color, width)
        rect_yz = cv2.rectangle(rect_xy, (5265, 3920), (5690, 3880), color, width)
        rect_xz = cv2.rectangle(rect_yz, (8300, 3855), (8870, 3780), color, width)
        
        # export image
        new_img = os.path.join(path, f'rect_{img}')
        cv2.imwrite(new_img, rect_xz_sx)

"""
exp 1
    # small sx
    - X(0.04,0.22)
    - Y(1.13,1.35)
    - Z(-0.02,0.02)
    rect_xy_sx = cv2.rectangle(cv2image, (1305, 1950), (1590, 1630), color, width)
    rect_yz_sx = cv2.rectangle(rect_xy_sx, (5465, 3920), (5690, 3880), color, width)
    rect_xz_sx = cv2.rectangle(rect_yz_sx, (7415, 3855), (7785, 3780), color, width)
    
    # small dx
    - X(0.62,0.80)
    - Y(1.13,1.35)
    - Z(-0.02,0.02)
    rect_xy = cv2.rectangle(rect_xz_sx, (2135, 1950), (2395, 1630), color, width)
    rect_yz = cv2.rectangle(rect_xy, (5465, 3920), (5690, 3880), color, width)
    rect_xz = cv2.rectangle(rect_yz, (8485, 3855), (8815, 3780), color, width)
    
    # large sx
    - X(0.04,0.35)
    - Y(0.93,1.35)
    - Z(-0.02,0.02)
    rect_xy_sx = cv2.rectangle(cv2image, (1305, 2235), (1750, 1630), color, width)
    rect_yz_sx = cv2.rectangle(rect_xy_sx, (5265, 3920), (5690, 3880), color, width)
    rect_xz_sx = cv2.rectangle(rect_yz_sx, (7415, 3855), (7990, 3780), color, width)
    
    # large dx
    - X(0.53,0.83)
    - Y(0.93,1.35)
    - Z(-0.02,0.02)
    rect_xy = cv2.rectangle(rect_xz_sx, (1995, 2235), (2435, 1630), color, width)
    rect_yz = cv2.rectangle(rect_xy, (5265, 3920), (5690, 3880), color, width)
    rect_xz = cv2.rectangle(rect_yz, (8300, 3855), (8870, 3780), color, width)
"""

"""
exp 2
    # vert sx
    - X(0.04,0.35)
    - Y(1.25,1.29)
    - Z(-0.02,0.41)
    rect_xy_sx = cv2.rectangle(cv2image, (1305, 1775), (1750, 1715), color, width)
    rect_yz_sx = cv2.rectangle(rect_xy_sx, (5590, 3920), (5630, 3485), color, width)
    rect_xz_sx = cv2.rectangle(rect_yz_sx, (7415, 3855), (7990, 3065), color, width)

    # vert dx
    - X(0.52,0.83)
    - Y(1.25,1.29)
    - Z(-0.02,0.41)
    rect_xy = cv2.rectangle(rect_xz_sx, (1995, 1775), (2440, 1715), color, width)
    rect_yz = cv2.rectangle(rect_xy, (5590, 3920), (5630, 3485), color, width)
    rect_xz = cv2.rectangle(rect_yz, (8340, 3855), (8870, 3065), color, width)
    
    # hor sx
    - X(0.04,0.35)
    - Y(0.93,1.35)
    - Z(-0.02,0.02)
    rect_xy_sx = cv2.rectangle(cv2image, (1305, 2235), (1750, 1630), color, width)
    rect_yz_sx = cv2.rectangle(rect_xy_sx, (5265, 3920), (5690, 3880), color, width)
    rect_xz_sx = cv2.rectangle(rect_yz_sx, (7415, 3855), (7990, 3780), color, width)
    
    # hor dx
    - X(0.52,0.83)
    - Y(0.93,1.35)
    - Z(-0.02,0.2)
    rect_xy = cv2.rectangle(rect_xz_sx, (1995, 2235), (2440, 1630), color, width)
    rect_yz = cv2.rectangle(rect_xy, (5265, 3920), (5690, 3880), color, width)
    rect_xz = cv2.rectangle(rect_yz, (8340, 3855), (8870, 3780), color, width)
"""

"""
exp 3
    - X(0.24,0.64)
    - Y(1.04,1.34)
    - Z(-0.02,0.02)
    rect_xy = cv2.rectangle(cv2image, (1590, 2075), (2165, 1645), color, width)
    rect_yz = cv2.rectangle(rect_xy, (5375, 3920), (5680, 3880), color, width)
    rect_xz = cv2.rectangle(rect_yz, (7785, 3855), (8520, 3780), color, width)
"""
