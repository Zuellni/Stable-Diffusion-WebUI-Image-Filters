from PIL import ImageEnhance, ImageFilter, ImageOps
from modules import scripts, scripts_postprocessing
import gradio as gr
import pilgram

script_name = "Image Filters"

def ui(is_extra):
	args = {}

	with gr.Group():
		with gr.Accordion(label = script_name, open = is_extra):
			with gr.Row():
				args["enable"] = gr.Checkbox(label = "Enable", value = False)
			with gr.Row():
				args["pillow_filter"] = gr.Dropdown(label = "Pillow Filter", multiselect = True, choices = [
					"blur", "contour", "detail", "edge_enhance", "edge_enhance_more",
					"emboss", "find_edges", "sharpen", "smooth", "smooth_more",
				])
			with gr.Row():
				args["pilgram_filter"] = gr.Dropdown(label = "Pilgram Filter", multiselect = True, choices = [
					"_1977", "brannan", "brooklyn", "clarendon", "earlybird",
					"gingham", "hudson", "inkwell", "kelvin", "lark",
					"lofi", "maven", "mayfair", "moon", "nashville", "perpetua",
					"reyes", "rise", "slumber", "stinson", "toaster",
					"valencia", "walden", "willow", "xpro2",
				])
			with gr.Row():
				args["ops_cutoff_low"] = gr.Slider(label = "Contrast Low", minimum = 0, step = 1, maximum = 50, value = 0)
				args["ops_cutoff_high"] = gr.Slider(label = "Contrast High", minimum = 0, step = 1, maximum = 50, value = 0)
				args["filter_box_blur"] = gr.Slider(label = "Box Blur", minimum = -1, step = 2, maximum = 99, value = -1)
				args["filter_gaussian_blur"] = gr.Slider(label = "Gaussian Blur", minimum = -1, step = 2, maximum = 99, value = -1)
			with gr.Row():
				args["filter_min"] = gr.Slider(label = "Min Filter", minimum = -1, step = 2, maximum = 99, value = -1)
				args["filter_median"] = gr.Slider(label = "Median Filter", minimum = -1, step = 2, maximum = 99, value = -1)
				args["filter_max"] = gr.Slider(label = "Max Filter", minimum = -1, step = 2, maximum = 99, value = -1)
				args["filter_mode"] = gr.Slider(label = "Mode Filter", minimum = -1, step = 2, maximum = 99, value = -1)
			with gr.Row():
				args["enhance_brightness"] = gr.Slider(label = "Brightness", minimum = 0, step = 0.1, maximum = 10, value = 1)
				args["enhance_color"] = gr.Slider(label = "Color", minimum = 0, step = 0.1, maximum = 10, value = 1)
				args["enhance_contrast"] = gr.Slider(label = "Contrast", minimum = 0, step = 0.1, maximum = 10, value = 1)
				args["enhance_sharpness"] = gr.Slider(label = "Sharpness", minimum = 0, step = 0.1, maximum = 10, value = 1)

	return args if is_extra else list(args.values())

def process(
	pp, enable, pillow_filter, pilgram_filter,
	ops_cutoff_low, ops_cutoff_high,
	filter_box_blur, filter_gaussian_blur,
	filter_min, filter_median, filter_max, filter_mode,
	enhance_brightness, enhance_color, enhance_contrast, enhance_sharpness,
):
	if not enable:
		return

	if ops_cutoff_low > 0 or ops_cutoff_high > 0:
		pp.image = ImageOps.autocontrast(pp.image, (ops_cutoff_low, ops_cutoff_high), True)

	if filter_box_blur > 0: pp.image = pp.image.filter(ImageFilter.BoxBlur(filter_box_blur))
	if filter_gaussian_blur > 0: pp.image = pp.image.filter(ImageFilter.GaussianBlur(filter_gaussian_blur))

	if filter_min > 0: pp.image = pp.image.filter(ImageFilter.MinFilter(filter_min))
	if filter_max > 0: pp.image = pp.image.filter(ImageFilter.MaxFilter(filter_max))
	if filter_median > 0: pp.image = pp.image.filter(ImageFilter.MedianFilter(filter_median))
	if filter_mode > 0: pp.image = pp.image.filter(ImageFilter.ModeFilter(filter_mode))

	if enhance_brightness != 1: pp.image = ImageEnhance.Brightness(pp.image).enhance(enhance_brightness)
	if enhance_color != 1: pp.image = ImageEnhance.Color(pp.image).enhance(enhance_color)
	if enhance_contrast != 1: pp.image = ImageEnhance.Contrast(pp.image).enhance(enhance_contrast)
	if enhance_sharpness != 1: pp.image = ImageEnhance.Sharpness(pp.image).enhance(enhance_sharpness)

	for filter in pillow_filter:
		pp.image = pp.image.filter(getattr(ImageFilter, filter.upper()))

	for filter in pilgram_filter:
		pp.image = getattr(pilgram, filter)(pp.image)

class Script(scripts.Script):
	def title(self):
		return script_name

	def show(self, is_img2img):
		return scripts.AlwaysVisible

	def ui(self, is_img2img):
		return ui(False)

	def postprocess_image(self, p, pp, *args):
		return process(pp, *args)

class ScriptPostprocessing(scripts_postprocessing.ScriptPostprocessing):
	name = script_name
	order = 0

	def ui(self):
		return ui(True)

	def process(self, pp, **args):
		return process(pp, **args)
