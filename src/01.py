import os, requests, subprocess
import cv2

# Entry point
def main():
    # fileds
    file_name = "./data/ALOS2237752900-181018/IMG-HH-ALOS2237752900-181018-UBSR2.1GUD.tif"
    output_name = file_name + ".png"
    cnv_cmd = "gdal_translate -of PNG " + file_name + " " + output_name

    # convert tif -> png
    process = (subprocess.Popen(cnv_cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
    # read, crop and write
    tmp = cv2.imread(output_name)
    cropping = tmp[8800:16000, 17500:21920]
    cv2.imwrite(file_name + "_cropped.png", cropping)
        
if __name__=="__main__":
       main()
