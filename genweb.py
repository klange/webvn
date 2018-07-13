#!/usr/bin/env python
"""
Generate HTML from a subset of rpy
"""
import fileinput
import sys


quick_help_text = """
This is a 'kinetic visual novel'. To advance in the<br>
story, just click the screen. There are no decisions<br>
to make, items to collect, or minigames to play.
"""

container_text = """
<!doctype html>
<html>
	<head>
		<title>{title}</title>
		<link rel="stylesheet" href="fullscreen.css">
		<meta name="viewport" content="width=device-width, user-scalable=no">
	</head>
	<body>
		<div class="viewport-container">
			<iframe src="{filename}#frame_0" seamless="true"></iframe>
		</div>
	</body>
</html>
"""

header = """
<!doctype html>
<html>
	<head>
		<link rel="stylesheet" href="vn.css">
		<link rel="stylesheet" href="scenes.css">
		<meta name="viewport" content="width=device-width, user-scalable=no">
	</head>
	<body>
		<div class="viewport">
"""

images_used = [
# TODO put your assets here
# TODO(klange): Maybe this should be automatically generated from the script?
]
next_classes = None
scene = "black"
frame_count = 0
characters = {}
expressions = []
last_content = ""
last_scene = ""
last_expression = ""
audio_background = None

output_buffer = ''
current_file_num = 0

def format_filename(file_num):
	t = fileinput.filename().replace('.webvn','')
	if file_num != -1:
		t += '_' + str(file_num)
	t += '.htm'
	return t

def output_append(string):
	global output_buffer
	output_buffer += string

def output_buffer_write(name):
	global output_buffer
	output_buffer = output_buffer.replace('_XXX_','')
	with open(name, 'w') as out:
		out.write(output_buffer)
	output_buffer = ''

def output_replace_last_link(new_target):
	global output_buffer
	parts = output_buffer.split('_XXX_')
	x = parts[:-1]
	output_buffer = "_XXX_".join(x) + new_target + parts[-1]

def next_file():
	global current_file_num
	print_preload()
	print_footer()
	output_buffer_write(format_filename(current_file_num))
	current_file_num += 1
	output_append(header)

def wordbox(text):
	return """
<div class="wordbox">
	<div class="wordbox-content">
		{0}
	</div>
</div>
""".format(text)

def wordbubble(text):
	return """
<div class="wordbubble">
	<div class="wordbubble-content">
		{0}
	</div>
</div>
""".format(text)

def whitetext(text):
	global scene
	if scene != "black": return wordbox(text)
	line_map = { 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five' }
	line_count = len(text.splitlines())
	return """
<div class="centered-white-text vertical-{0}-line">
	{1}
</div>
""".format(line_map[line_count] if line_count in line_map else "one", text)

def switch_mouth(character, newmouth):
	if '_m1' in characters[character]['pose']:
		characters[character]['pose'] = characters[character]['pose'].replace('_m1','_'+newmouth)
	elif '_m0' in characters[character]['pose']:
		characters[character]['pose'] = characters[character]['pose'].replace('_m0','_'+newmouth)

def switch_pose(character, newpose):
	if '_m1' in characters[character]['pose']:
		characters[character]['pose'] = newpose + '_m1'
	elif '_m0' in characters[character]['pose']:
		characters[character]['pose'] = newpose + '_m0'

def characterbubble(character, text):
	if text.startswith('"'): text = "m0 " + text
	mouth, _, text = text.partition(" ")
	if not (mouth == 'm1' or mouth == 'm0'):
		switch_pose(character, mouth)
		mouth, _, text = text.partition(" ")
	text = eval(text)
	switch_mouth(character, mouth)
	return """
<div class="wordbubble-character">
	<div class="wordbubble-content">
		{0}
	</div>
</div>
""".format(text)

def character(name, extra=None):
	attributes = characters[name]
	return """
<div class="{2}-character">
	<img class="{0}" src="assets/character/{0}/{0}_{1}.png">
</div>
""".format(name, attributes['pose'], attributes['position'])

def make_expression(expression):
	return """<div class="overlay {0}"></div>""".format(expression)

def stage(contents):
	global scene, next_classes, characters, expressions, last_content, last_scene, last_expression
	chars = ""
	for k,v in characters.iteritems():
		chars += character(k)
	extra_classes = "scene-{0}".format(scene if scene else "black")
	my_expressions = "\n".join([make_expression(x) for x in expressions])
	out = """
<div class="stage {3}">
	{4}
	{7}
</div>
<div class="stage {0} {5}">
	{1}
	{6}
	{2}
</div>
""".format(extra_classes, chars, "\n".join(contents), last_scene, last_content, next_classes if next_classes else "fade-in", my_expressions, last_expression)
	last_content = chars + "\n".join(contents)
	last_scene = extra_classes
	last_expression = my_expressions
	return out

def print_frame(content):
	global frame_count
	frame_count += 1
	output_append("""
<div class="frame" id="frame_{1}">
	{0}
	<a target="_self" class="framelink" href="_XXX_#frame_{2}"></a>
</div>
""".format(content.strip(), frame_count - 1, frame_count))

def process(line):
	global scene, next_classes, characters, expressions, audio_background
	c, _, rest = line.strip().partition(" ")
	if c == "#WEB:":
		c, _, rest = rest.strip().partition(" ")
	if line.strip().startswith('"'):
		print_frame(stage([whitetext(eval(line.strip()))]))
	elif c == "class":
		next_classes = rest
	elif c == "expression":
		expressions = rest.split(" ")

	# TODO: These character lines need to be adjusted
	# TODO(klange): This should probably be part of a config.
	elif c == "wordbubble":
		print_frame(stage([wordbubble(eval(rest))]))
	elif c == "characterbubble":
		character, _, rest = rest.partition(" ")
		print_frame(stage([characterbubble(character, rest)]))
	elif c == "scene":
		scene = rest.split()[-1]
		characters.clear()
		del expressions[:]
	elif c == "pause":
		# Can't pause, can insert an interstitial
		print_frame(stage(["<!-- blank interstitial -->"]))
	elif c == "show":
		character = rest.split()[0].replace(":","")
		if character not in characters:
			characters[character] = {'pose': None, 'position': 'center'}

		attributes = rest.split()[1:]
		if len(attributes) == 1 and attributes[0] == 'm1':
			switch_mouth(character, 'm1')
			return
		if len(attributes) == 1 and attributes[0] == 'm0':
			switch_mouth(character, 'm0')
			return
		if len(attributes) == 1 and not (attributes[0].endswith('_m1') or attributes[0].endswith('_m0')):
			switch_pose(character, attributes[0])
			return
		if len(attributes) > 0:
			characters[character]['pose'] = attributes[0]
		if len(attributes) > 1:
			characters[character]['position'] = attributes[1]
	elif c == "hide":
		character = rest.split()[0]
		if character in characters:
			del charactersc[character]
	elif c == "music":
		output_replace_last_link(format_filename(current_file_num + 1))
		next_file()
		if rest.split()[0] == 'stop':
			audio_background = None
		else:
			audio_background = eval(rest)


def print_footer():
	output_append("\n			</div>\n")
	if audio_background:
		output_append("""
			<audio autoplay="autoplay" loop="loop" src="{audio}" />
		""".format(audio=audio_background))
	output_append("""
		</body>
	</html>
	""")

def print_preload():
	output_append("""
</div>
<div id="preload">
{0}
""".format("\n".join(['<img src="{0}" width="1" height="1">'.format(x) for x in images_used])))

if __name__ == "__main__":

	output_append(header)

	scene = 'black'
	text = whitetext(quick_help_text)
	scene = 'splash'
	expressions = ['screen-color-80']
	print_frame(stage([text]))

	for line in fileinput.input():
		process(line)

	next_file()

	with open(format_filename(-1), 'w') as f:
		# TODO(klange): Why is this hard-coded...
		f.write(container_text.format(title="Your Title Here", filename=format_filename(0)))

