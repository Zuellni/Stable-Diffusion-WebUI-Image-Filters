from PIL import ImageEnhance, ImageFilter, ImageOps
from modules import scripts, scripts_postprocessing
import gradio as gr
import pilgram

script_name = "Image Filters"
script_order = 100000
val_min_enh = -10
val_min = 0
val_def = 0
val_step = 1
val_max = 10
val_max_ops = 50

def ui(is_extra):
	args_main = {}
	args = {}

	with gr.Group():
		with gr.Accordion(label = script_name, open = False):
			with gr.Row():
				args_main["enable"] = gr.Checkbox(label = "Enable", value = False)
				reset_button = gr.Button(value = "Reset", variant = "secondary")
			with gr.Row():
				args_main["effects"] = gr.Dropdown(label = "Effects", multiselect = True, choices = [
					"_1977", "brannan", "brooklyn", "clarendon", "earlybird",
					"gingham", "hudson", "inkwell", "kelvin", "lark",
					"lofi", "maven", "mayfair", "moon", "nashville",
					"perpetua", "reyes", "rise", "slumber", "stinson",
					"toaster", "valencia", "walden", "willow", "xpro2",
				])
				args_main["filters"] = gr.Dropdown(label = "Filters", multiselect = True, choices = [
					"blur", "contour", "detail", "edge_enhance", "edge_enhance_more",
					"emboss", "find_edges", "sharpen", "smooth", "smooth_more",
				])
				args_main["operations"] = gr.Dropdown(label = "Operations", multiselect = True, choices = [
					"equalize", "flip", "grayscale", "invert", "mirror",
				])
			with gr.Row():
				args["ops_cutoff_low"] = gr.Slider(label = "Auto Contrast Low", minimum = val_min, step = val_step, maximum = val_max_ops, value = val_def)
				args["ops_cutoff_high"] = gr.Slider(label = "Auto Contrast High", minimum = val_min, step = val_step, maximum = val_max_ops, value = val_def)
				args["filter_box_blur"] = gr.Slider(label = "Box Blur", minimum = val_min, step = val_step, maximum = val_max, value = val_def)
				args["filter_gaussian_blur"] = gr.Slider(label = "Gaussian Blur", minimum = val_min, step = val_step, maximum = val_max, value = val_def)
			with gr.Row():
				args["filter_min"] = gr.Slider(label = "Min Filter", minimum = val_min, step = val_step, maximum = val_max, value = val_def)
				args["filter_median"] = gr.Slider(label = "Median Filter", minimum = val_min, step = val_step, maximum = val_max, value = val_def)
				args["filter_max"] = gr.Slider(label = "Max Filter", minimum = val_min, step = val_step, maximum = val_max, value = val_def)
				args["filter_mode"] = gr.Slider(label = "Mode Filter", minimum = val_min, step = val_step, maximum = val_max, value = val_def)
			with gr.Row():
				args["enhance_brightness"] = gr.Slider(label = "Brightness", minimum = val_min_enh, step = val_step, maximum = val_max, value = val_def)
				args["enhance_color"] = gr.Slider(label = "Color", minimum = val_min_enh, step = val_step, maximum = val_max, value = val_def)
				args["enhance_contrast"] = gr.Slider(label = "Contrast", minimum = val_min_enh, step = val_step, maximum = val_max, value = val_def)
				args["enhance_sharpness"] = gr.Slider(label = "Sharpness", minimum = val_min_enh, step = val_step, maximum = val_max, value = val_def)

	list_main = list(args_main.values())
	list_args = list(args.values())
	reset_button.click(reset, inputs = list_args, outputs = list_args)
	return args_main | args if is_extra else list_main + list_args

def reset(*args):
	return [val_def for arg in args]

def map_filter(value):
	return 1 + 2 * (value - 1)

def map_enhance(value):
	return 0.1 * value + 1

def process(
	pp, enable, effects, filters, operations,
	ops_cutoff_low, ops_cutoff_high, filter_box_blur, filter_gaussian_blur,
	filter_min, filter_median, filter_max, filter_mode,
	enhance_brightness, enhance_color, enhance_contrast, enhance_sharpness,
):
	if not enable:
		return

	for effect in effects:
		pp.image = getattr(pilgram, effect)(pp.image)

	for filter in filters:
		pp.image = pp.image.filter(getattr(ImageFilter, filter.upper()))

	for operation in operations:
		pp.image = getattr(ImageOps, operation)(pp.image)

	if ops_cutoff_low != val_def or ops_cutoff_high != val_def:
		pp.image = ImageOps.autocontrast(pp.image, (ops_cutoff_low, ops_cutoff_high), True)

	if enhance_brightness != val_def: pp.image = ImageEnhance.Brightness(pp.image).enhance(map_enhance(enhance_brightness))
	if enhance_color != val_def: pp.image = ImageEnhance.Color(pp.image).enhance(map_enhance(enhance_color))
	if enhance_contrast != val_def: pp.image = ImageEnhance.Contrast(pp.image).enhance(map_enhance(enhance_contrast))
	if enhance_sharpness != val_def: pp.image = ImageEnhance.Sharpness(pp.image).enhance(map_enhance(enhance_sharpness))

	if filter_box_blur != val_def: pp.image = pp.image.filter(ImageFilter.BoxBlur(map_filter(filter_box_blur)))
	if filter_gaussian_blur != val_def: pp.image = pp.image.filter(ImageFilter.GaussianBlur(map_filter(filter_gaussian_blur)))

	if filter_min != val_def: pp.image = pp.image.filter(ImageFilter.MinFilter(map_filter(filter_min)))
	if filter_max != val_def: pp.image = pp.image.filter(ImageFilter.MaxFilter(map_filter(filter_max)))
	if filter_median != val_def: pp.image = pp.image.filter(ImageFilter.MedianFilter(map_filter(filter_median)))
	if filter_mode != val_def: pp.image = pp.image.filter(ImageFilter.ModeFilter(map_filter(filter_mode)))

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