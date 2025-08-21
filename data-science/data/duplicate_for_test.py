import shutil
import os

# Path to the original image (update this if your image is named differently)
original_image = os.path.join('..', '..', 'frontend', 'src', 'assets', 'handwriting_sample.png')  # Change this to your actual image path

targets = [
    os.path.join('A', 'img1.png'),
    os.path.join('A', 'img2.png'),
    os.path.join('B', 'img3.png'),
    os.path.join('B', 'img4.png'),
]

for target in targets:
    folder = os.path.dirname(target)
    if not os.path.exists(folder):
        os.makedirs(folder)
    shutil.copyfile(original_image, target)

print('Images duplicated for quick test.')
