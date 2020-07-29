from PIL import Image
import os

def main():
    """
    loop through images, resize and split into tiles
    """
    pwd = os.getcwd()
    print(pwd)
    # resize images
    # im = f'{pwd}/data/waldo/book1_s1.jpg'
    # out = resize_img(im)
    # out.save(f'{pwd}/data/waldo_resized/book1_s1.jpg')
    
    for book in range(5):
        for scene in range(13):
            try:
                im = f'{pwd}/data/waldo/book{book}_s{scene}.jpg'
                out = resize_img(im)
                out.save(f'{pwd}/data/waldo_resized/book{book}_s{scene}.jpg')
            except (NameError, FileNotFoundError):
                pass

    # split images into tiles
    for book in range(5):
        for scene in range(13):
            try:
                im_path = f'{pwd}/data/waldo_resized/book{book}_s{scene}.jpg'
                crop_img(pwd, im_path, f'{pwd}/data/waldo_tiles', book, scene)
            except (NameError, FileNotFoundError):
                pass  

# def create_dir():
    

# resize images to 1536*1024
def resize_img(f):
    im = Image.open(f)
    out = im.resize((1536, 1024))
    return out


# split images to 256x256
def crop_img(pwd, img_path, save_path, test=False, book=None, scene=None):
    im = Image.open(img_path)
    imgwidth, imgheight = im.size
    
    y1 = 0
    height = 256
    width = 256
    i = 0
    
    for y in range(0, imgheight, height):
        for x in range(0, imgwidth, width):
            y1 = y + height
            x1 = x + width
            box = (x, y, x1, y1)
            area = im.crop(box)
            if test == False:
                area.save(f'{save_path}/book{book}_s{scene}_{x}_{y}.jpg')
            else:
                area.save(f'{save_path}/{i}.jpg')
                i = i + 1
            create_label_files(pwd, book, scene, x, y)

def create_label_files(pwd, book, scene, x, y):
    with open(f'{pwd}/data/waldo_tiles/book{book}_s{scene}_{x}_{y}.txt', 'w') as f:
        # do nothing as we want the files empty as default
        pass


if __name__ == "__main__":
    main()