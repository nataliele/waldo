from PIL import Image
import numpy as np
import os
import argparse
import subprocess
from data import preprocess_img


def get_path():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Path of test image')
    
    # Add the arguments
    my_parser.add_argument('Path',
                           metavar='path',
                           type=str,
                           help='the path to test image')
    
    # Execute the parse_args() method
    args = my_parser.parse_args()
    return args.Path

def main():
    """
    loop through images, resize and split into tiles
    """
    pwd = os.getcwd()
    print(pwd)
    
    input_path = os.path.join(pwd, get_path())
    
    tmp_dir = f'{pwd}/data/tmp'
    pred_dir = os.path.join(tmp_dir, 'pred')
    tmp_im_path = os.path.join(tmp_dir, 'tmp.jpg')
    
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    if not os.path.isdir(pred_dir):
        os.mkdir(pred_dir)
    # print(tmp_dir)
    # print(tmp_im_path)
    # print(input_path)
    
    # resize images
    try:
        out = preprocess_img.resize_img(input_path)
        out.save(tmp_im_path)
    except (NameError, FileNotFoundError):
        print('File not found')
    
    # split images into tiles
    try:
        preprocess_img.crop_img(pwd, tmp_im_path, tmp_dir, test=True)
    except (NameError, FileNotFoundError):
        print('File not found')

    # predict tiles
    for tile in os.listdir(tmp_dir):
        if (tile != 'tmp.jpg') and (tile != 'pred'):
            tile_input = os.path.join(tmp_dir, tile)
            # print(tile_input)
            subprocess.run(f"./darknet detector test cfg/obj_waldo_yolo2.data cfg/yolov2-waldo.cfg backup_waldo_yolo2/yolov2-waldo_3000.weights '{tile_input}'", shell=True, check=True)
            subprocess.run(f"mv '{pwd}/predictions.jpg' '{pred_dir}/pred_{tile}'", shell=True, check=True)
    
    # stitch the prediction tiles back
    img_lst = []
    n = len(os.listdir(pred_dir))
    for i in range(n):
        tile_input = os.path.join(pred_dir, f'pred_{i}.jpg')        #to keep order of tiles
        img_lst.append(Image.open(tile_input))
    img_grid = pil_grid(img_lst, max_horiz=6)
    img_grid.save(f'{pwd}/predictions.jpg')
    
    


def pil_grid(images, max_horiz=np.iinfo(int).max):
    n_images = len(images)
    n_horiz = min(n_images, max_horiz)
    h_sizes, v_sizes = [0] * n_horiz, [0] * (n_images // n_horiz)
    for i, im in enumerate(images):
        h, v = i % n_horiz, i // n_horiz
        h_sizes[h] = max(h_sizes[h], im.size[0])
        v_sizes[v] = max(v_sizes[v], im.size[1])
    h_sizes, v_sizes = np.cumsum([0] + h_sizes), np.cumsum([0] + v_sizes)
    im_grid = Image.new('RGB', (h_sizes[-1], v_sizes[-1]), color='white')
    for i, im in enumerate(images):
        im_grid.paste(im, (h_sizes[i % n_horiz], v_sizes[i // n_horiz]))
    return im_grid


if __name__ == "__main__":
    main()