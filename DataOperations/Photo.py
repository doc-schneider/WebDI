from PIL import Image
from PIL.ExifTags import TAGS
# import pyheif
# import imageio
from pathlib import Path

from DataOperations.Files import get_files_info


# TODO: iPhone HEVC, MOV, ..
allow_formats = [".HEIC", ".JPG"]

class PhotoFactory:

    @staticmethod
    def table_from_folder(
            path_photo,
            album_name,
            chapters=None,
            pretable=None
    ):
        files_info = get_files_info(
            path_photo[0],
            [],
            allow_formats,
            [pretable.name],
        )

        # Create table from admissible columns

        # Get creation time form meta data (exif)
        for i in range(files_info.shape[0]):
            pass


        i = 0
        # Read HEIC file
        # image = imageio.v3.imread(Path(files_info.loc[i, "PATH"], "IMG_8570 (2).heic"))
        # Save the image in a different format (e.g., JPEG)
        # imageio.imwrite("example_converted.jpg", image)
        # Convert HEIC to a PIL Image
        # image = Image.frombytes(
        #     heif_file.mode,
        #     heif_file.size,
        #     heif_file.data,
        #     "raw",
        #     heif_file.mode,
        #     heif_file.stride,
        # )
        #
        # # Save the image in a different format (e.g., JPEG)
        # image.save("example_converted.jpg", "JPEG")
        image = Image.open(Path(files_info.loc[i, "PATH"], files_info.loc[i, "FILE_NAME"]))






# def get_photo_taken_date(image_path):
#     # Open an image file
#     with Image.open(image_path) as img:
#         # Get EXIF data
#         exif_data = img._getexif()
#
#         if not exif_data:
#             return None
#
#         # Extract datetime from EXIF data
#         for tag_id in exif_data:
#             # get the tag name
#             tag = TAGS.get(tag_id, tag_id)
#             if tag == 'DateTimeOriginal':
#                 return exif_data[tag_id]
#
#     return None

# Example usage
# image_path = 'path/to/your/photo.jpg'
# timestamp = get_photo_taken_date(image_path)
# if timestamp:
#     print(f"Photo was taken on: {timestamp}")
# else:
#     print("No original date metadata found.")
