#This code will work if the color of the desired actor in the mask image is RED.
# Why RED?? Because, during creation of the mask image I have set the color of the desired actor RED.
# SO, if you set another color then also it would be possible but at that time in this code you have to change the color info.



import numpy as np
import cv2
import os
import copy

actor_array = ['SM_DenkMitEdelstahlReinigerSpray_18','SM_CalgonitFinishKlarspueler_3','SM_CalgonitFinishVorratspack_12']
actor_array = np.array(actor_array)

lit = 'F:/unreal_cv_documentation/detect_ROI_for_multi_actor/image_test/lit_1.png'
mask_im = 'F:/unreal_cv_documentation/detect_ROI_for_multi_actor/image_test/mask_1.png'


img = cv2.imread(mask_im)
rgb_img = cv2.imread(lit)
test_copy_rgb = copy.copy(rgb_img)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

## Gen lower mask (0-5) and upper mask (175-180) of RED
mask1 = cv2.inRange(img_hsv, (0,50,20), (5,255,255))
mask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))
## Merge the mask and crop the red regions
mask = cv2.bitwise_or(mask1, mask2 )
croped = cv2.bitwise_and(img, img, mask=mask)

roi_list = []

image, contours, hierarchy =  cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for t in range (0,len(actor_array),1):
    if len(contours)>0:
        print('length is: ',len(contours))
        cnt = contours[t]
        x,y,w,h = cv2.boundingRect(cnt)
        roi_rgb_image=cv2.rectangle(rgb_img,(x,y),(x+w,y+h),(0,255,0),1)
        print('info of ',t,' contour ',x,',',y,',',x+w,',',y+h)
        x=x
        y=y
        x_1=x+w
        y_1=y+h
        
        roi_point = [x,y,x_1,y_1]
        roi_list.append(roi_point)
        
black_rgb = cv2.bitwise_and(test_copy_rgb, test_copy_rgb, mask=mask)

# target = test_rgb
roi_black_rgb = copy.copy(black_rgb)
print('roi_list',roi_list)

for i in roi_list:
    x_new = i[0]
    y_new = i[1]
    x_w_new = i[2]
    y_h_new = i[3]
    
    roi_black_rgb = cv2.rectangle(roi_black_rgb,(x_new,y_new),(x_w_new,y_h_new),(0,255,0),1)


# writing roi info from list to a text file

f = open('F:/unreal_cv_documentation/detect_ROI_for_multi_actor/final_image/ROI_test.txt', 'a')
f = open('F:/unreal_cv_documentation/detect_ROI_for_multi_actor/final_image/ROI_test.txt', 'r+')
f.truncate(0)

for i in roi_list:
    ww = str(i)
    ww=ww.replace('[','')
    ww=ww.replace(']','')
    ww=ww.replace(',','')
    f.write(ww)
    f.write("\n")
f.close()


## Display
# cv2.imshow("mask", mask)
# cv2.imshow("croped", croped)
cv2.imshow('roi_rgb_image', roi_rgb_image)
cv2.imshow("black_rgb", black_rgb)
cv2.imshow("roi_black_rgb", roi_black_rgb)

cv2.imwrite('F:/unreal_cv_documentation/detect_ROI_for_multi_actor/final_image/roi_rgb_new.png',roi_rgb_image)
cv2.imwrite('F:/unreal_cv_documentation/detect_ROI_for_multi_actor/final_image/black_rgb_new.png',black_rgb)
cv2.imwrite('F:/unreal_cv_documentation/detect_ROI_for_multi_actor/final_image/roi_black_rgb_new.png',roi_black_rgb)



if cv2.waitKey() == ord('q'): #press q to close the output image window
        cv2.destroyAllWindows()
