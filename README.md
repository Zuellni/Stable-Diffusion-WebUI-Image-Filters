# Image Filters
A simple image postprocessing extension for [stable diffusion webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).
Applies various effects to generated images in pixel space just before they're saved. Works with txt2img, img2img, and in the extras tab.
Pilgram filters courtesy of [akiomik](https://github.com/akiomik/pilgram).

## Notes
If, after updating, certain values are not displaying correctly in the webui, you should remove all lines containing `customscript/image_filters.py` from your `user-config.js` file in the root directory.
You can also edit the maximum values in the same file to your liking.

To move this script up or down in hierarchy you should rename the `stable-diffusion-webui-image-filters` directory in `extensions`. The scripts are loaded in alphabetical order.

For detailed information on how each filter functions I recommend reading the Pillow documentation: [ImageEnhance](https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html), [ImageFilter](https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html), [ImageOps](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html).

## Preview
![preview](https://user-images.githubusercontent.com/123005779/224801664-661471c6-b06d-427d-b4c4-9c12b2b238a8.jpg)

## Comparison
Base | Filtered
---- | --------
![base](https://user-images.githubusercontent.com/123005779/224670233-00e09bbb-b889-4b34-8e94-9e5c16fe7ec6.jpg) | ![filtered](https://user-images.githubusercontent.com/123005779/224571916-4e669118-a78c-4abb-b0a5-b45c2d6927ed.jpg)
