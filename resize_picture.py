import os
from PIL import Image


def resize_image(image_path, output_path, resize_ratio):
    """
    Resize an image by a given ratio.

    :param image_path: Path to the input image.
    :param output_path: Path to save the resized image.
    :param resize_ratio: Ratio to resize the image.
    """
    with Image.open(image_path) as image:
        # Calculate new size
        new_width = int(image.width * resize_ratio)
        new_height = int(image.height * resize_ratio)
        new_size = (new_width, new_height)

        # Resize the image
        resized_image = image.resize(new_size)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the resized image
        resized_image.save(output_path)


def resize_images_in_folder(input_path, output_path, resize_ratio):
    """
    Resize all images in a folder and its subfolders.

    :param input_path: Path to the input folder.
    :param output_path: Path to the output folder.
    :param resize_ratio: Ratio to resize the images.
    """
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                input_image_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_path)
                output_image_path = os.path.join(output_path, relative_path, file)

                print(f"Resizing {input_image_path} to {output_image_path}")
                resize_image(input_image_path, output_image_path, resize_ratio)


# Example usage
input_path = 'D:/movie/image'
output_path = 'D:/movie/pic'
resize_ratio = 0.9  # Resize to 50% of the original size

resize_images_in_folder(input_path, output_path, resize_ratio)