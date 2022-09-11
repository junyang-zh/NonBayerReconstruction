import cv2
import os
import sys
import tqdm

def gen_sample(video_path, target_path, frameFrequency):
    cap = cv2.VideoCapture(video_path)
    frames_num = int(cap.get(7))
    frame_index = 0
    for frame_index in tqdm.tqdm(range(frames_num)):
        res, image = cap.read()
        if not res:
            print('Unexpected image got, exited')
            break
        if frame_index % frameFrequency == 0:
            image_name = "{}_{}.png".format(os.path.basename(video_path), frame_index)
            cv2.imwrite(os.path.join(target_path, image_name), image)
    cap.release()

def main():
    if (len(sys.argv) != 3):
        print("Usage: {} input_path output_path".format(sys.argv[0]))
        return
    #需要处理的视频路径; linux和windows下面注意路径的读取方式有所不同
    src_path = sys.argv[1]
    #目标文件夹路径
    target_path = sys.argv[2]
    #设置间隔帧数
    frameFrequency = 10
    # 获取文件路径
    filelist = os.listdir(src_path)
    video_num = len(filelist)
    print("视频个数为：%d" % video_num)
    for item in filelist:
        #设置视频的索引个数
        video_index = 0
        if item.endswith(('.h264','.mp4','.mkv','avi')):
            video_path = os.path.join(src_path,item)
            #截取图片
            gen_sample(video_path, target_path,frameFrequency)
            video_index += 1

if __name__ == '__main__':
    main()