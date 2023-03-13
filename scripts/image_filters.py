from PIL import ImageEnhance, ImageFilter, ImageOps
from modules import scripts, scripts_postprocessing
import gradio as gr
import pilgram

script_name = "Image Filters"
script_order = 100000

def ui(is_extra):
	args_main = {}
	args = {}

	with gr.Group():
		with gr.Accordion(label = script_name, open = False):
			with gr.Row(equal_height = True):
				args_main["enable"] = gr.Checkbox(label = "Enable", value = False)
				gr.Column(scale = 4)
				reset_button = gr.Button(value = "Reset", variant = "secondary")
			with gr.Row(equal_height = True):
				args_main["pillow_filters"] = gr.Dropdown(label = "Pillow Filters", multiselect = True, choices = [
					"blur", "contour", "detail", "edge_enhance", "edge_enhance_more",
					"emboss", "find_edges", "sharpen", "smooth", "smooth_more",
				])
				args_main["pilgram_filters"] = gr.Dropdown(label = "Pilgram Filters", multiselect = True, choices = [
					"_1977", "brannan", "brooklyn", "clarendon", "earlybird",
					"gingham", "hudson", "inkwell", "kelvin", "lark",
					"lofi", "maven", "mayfair", "moon", "nashville",
					"perpetua", "reyes", "rise", "slumber", "stinson",
					"toaster", "valencia", "walden", "willow", "xpro2",
				])
			with gr.Row(equal_height = True):
				args["ops_cutoff_low"] = gr.Slider(label = "Auto Contrast Low", minimum = 0, step = 1, maximum = 50, value = 0)
				args["ops_cutoff_high"] = gr.Slider(label = "Auto Contrast High", minimum = 0, step = 1, maximum = 50, value = 0)
				args["filter_box_blur"] = gr.Slider(label = "Box Blur", minimum = 0, step = 1, maximum = 10, value = 0)
				args["filter_gaussian_blur"] = gr.Slider(label = "Gaussian Blur", minimum = 0, step = 1, maximum = 10, value = 0)
			with gr.Row(equal_height = True):
				args["filter_min"] = gr.Slider(label = "Min Filter", minimum = 0, step = 1, maximum = 10, value = 0)
				args["filter_median"] = gr.Slider(label = "Median Filter", minimum = 0, step = 1, maximum = 10, value = 0)
				args["filter_max"] = gr.Slider(label = "Max Filter", minimum = 0, step = 1, maximum = 10, value = 0)
				args["filter_mode"] = gr.Slider(label = "Mode Filter", minimum = 0, step = 1, maximum = 10, value = 0)
			with gr.Row(equal_height = True):
				args["enhance_brightness"] = gr.Slider(label = "Brightness", minimum = -10, step = 1, maximum = 10, value = 0)
				args["enhance_color"] = gr.Slider(label = "Color", minimum = -10, step = 1, maximum = 10, value = 0)
				args["enhance_contrast"] = gr.Slider(label = "Contrast", minimum = -10, step = 1, maximum = 10, value = 0)
				args["enhance_sharpness"] = gr.Slider(label = "Sharpness", minimum = -10, step = 1, maximum = 10, value = 0)

	list_main = list(args_main.values())
	list_args = list(args.values())
	reset_button.click(reset, inputs = list_args, outputs = list_args)
	return args_main | args if is_extra else list_main + list_args

def reset(*args):
	return [0 for arg in args]

def map_filter(value):
	return 1 + 2 * (value - 1)

def map_enhance(value):
	return 0.1 * value + 1

def process(
	pp, enable, pillow_filters, pilgram_filters,
	ops_cutoff_low, ops_cutoff_high,
	filter_box_blur, filter_gaussian_blur,
	filter_min, filter_median, filter_max, filter_mode,
	enhance_brightness, enhance_color, enhance_contrast, enhance_sharpness,
):
	if not enable:
		return

	if ops_cutoff_low != 0 or ops_cutoff_high != 0:
		pp.image = ImageOps.autocontrast(pp.image, (ops_cutoff_low, ops_cutoff_high), True)

	if filter_box_blur != 0: pp.image = pp.image.filter(ImageFilter.BoxBlur(map_filter(filter_box_blur)))
	if filter_gaussian_blur != 0: pp.image = pp.image.filter(ImageFilter.GaussianBlur(map_filter(filter_gaussian_blur)))

	if filter_min != 0: pp.image = pp.image.filter(ImageFilter.MinFilter(map_filter(filter_min)))
	if filter_max != 0: pp.image = pp.image.filter(ImageFilter.MaxFilter(map_filter(filter_max)))
	if filter_median != 0: pp.image = pp.image.filter(ImageFilter.MedianFilter(map_filter(filter_median)))
	if filter_mode != 0: pp.image = pp.image.filter(ImageFilter.ModeFilter(map_filter(filter_mode)))

	if enhance_brightness != 0: pp.image = ImageEnhance.Brightness(pp.image).enhance(map_enhance(enhance_brightness))
	if enhance_color != 0: pp.image = ImageEnhance.Color(pp.image).enhance(map_enhance(enhance_color))
	if enhance_contrast != 0: pp.image = ImageEnhance.Contrast(pp.image).enhance(map_enhance(enhance_contrast))
	if enhance_sharpness != 0: pp.image = ImageEnhance.Sharpness(pp.image).enhance(map_enhance(enhance_sharpness))

	for filter in pillow_filters:
		pp.image = pp.image.filter(getattr(ImageFilter, filter.upper()))

	for filter in pilgram_filters:
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
	order = script_order

	def ui(self):
		return ui(True)

	def process(self, pp, **args):
		return process(pp, **args)