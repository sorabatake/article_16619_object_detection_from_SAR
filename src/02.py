import os, requests, subprocess
import cv2
import copy as cp
import numpy as np
import random

# vs target
def rectvsrect(_x1, _y1, _w1, _h1, _x2, _y2, _w2, _h2):
    if _x1 < _x2 and _y1 < _y2 and _w1 > _w2 and _h1 > _h2:
      return True
    return False

# Entry point    
def main():
    # fileds
    src_name = "./data/ALOS2237752900-181018/IMG-HH-ALOS2237752900-181018-UBSR2.1GUD.tif"
    file_name = src_name + "_cropped.png" # previous processing
    output_dir = "./data/datasets/"
    src_bbox = np.load("./data/ALOS2237752900-181018/bbox.npy") # bbox
    src_img = cv2.imread(file_name)
    dataset_num = 1100
    max_size = 416
    count = 0
    object_ratio = 1.0
    file_list = []
    
    # make dir
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)
    
    # start processing
    print("generating datasets...")
    for i in range(99999):
      offset_x = random.randint(0, (src_img.shape[1] - max_size))
      offset_y = random.randint(0, (src_img.shape[0] - max_size))
      limit_x = offset_x + max_size
      limit_y = offset_y + max_size
      train_x = cp.deepcopy(src_img[offset_y:limit_y, offset_x:limit_x])
      # train_x = cv2.equalizeHist(train_x[:,:,0])
      view_x = cp.deepcopy(src_img[offset_y:limit_y, offset_x:limit_x])
      # calculate bbox
      label_str = ""
      included_flag = False
      for _box in src_bbox:
        collision = rectvsrect(offset_x, offset_y, limit_x, limit_y, _box[0], _box[1], _box[2], _box[3])
        if collision:
          _box_offset_x = int(_box[0]) - offset_x
          _box_offset_y = int(_box[1]) - offset_y
          _box_limit_x = int(_box[2]) - offset_x
          _box_limit_y = int(_box[3]) - offset_y
          _box_center_w = (_box_limit_x - _box_offset_x) # box full-length in x
          _box_center_h = (_box_limit_y - _box_offset_y) # box full-length in y
          _box_center_x = _box_offset_x + (_box_center_w * 0.5) # box center in x
          _box_center_y = _box_offset_y + (_box_center_h * 0.5) # box center in y
          _box_center_w_norm = _box_center_w / max_size
          _box_center_h_norm = _box_center_h / max_size
          _box_center_x_norm = _box_center_x / max_size
          _box_center_y_norm = _box_center_y / max_size
          label_str += "0 " + str(_box_center_x_norm) + " " + str(_box_center_y_norm) + " " + str(_box_center_w_norm) + " " + str(_box_center_h_norm) + "\n"
          # test view
          view_x = cv2.rectangle(view_x, (_box_offset_x, _box_offset_y), (_box_limit_x, _box_limit_y), (0, 255, 255))
          included_flag = True 

      # bridge included ?
      if not included_flag and random.random() < object_ratio:
        continue
        
      # write image
      output_name = output_dir + str(count)
      cv2.imwrite(output_name +".png", train_x)
      cv2.imwrite(output_name +"_view.jpg", view_x)
      # write label
      file = open(output_name + ".txt", 'w')
      file.write(label_str)
      file.close()
      # progress
      count += 1
      print("Generated:", count, "/", dataset_num)
      if count == dataset_num:
        break
        
if __name__=="__main__":
       main()
