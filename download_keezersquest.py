import json		# parsing json data
import requests	# downloadnig files
import os		# for mkdir

url = "https://keezersquest.nl/"

folder = "keezersquest.nl"

try:
	os.mkdir(folder)
except:
	print ()

print ("downloading index.html")
r = requests.get(url)
with open(folder + "/index.html",'wb') as output_file:
	output_file.write(r.content)

# makes the folders where the files are stored
def make_folders(file):
	i = 0
	end = 0
	while end != -1:
		start = file.find("/", i)
		end = file.find("/", start + 1)
		if (start < i or end == -1):
			return
		i = end
		try:
			os.mkdir(folder + file[0:end])
		except:
			continue

# downloads one file
def get_file(file):
	if (file.find("www") != -1):
		return
	make_folders(file)
	url_file = url + file
	r = requests.get(url_file)
	with open(folder + file,'wb') as output_file:
		output_file.write(r.content)

# lists all files reverenced in index.html
def src_href_files_names(str):
	file = list()
	i = 0
	index = 0
	while i != -1:
		index = i
		i = str.find("src", i)
		if (i < index):
			break
		start = str.find('"', i) + 1
		end = str.find('"', start)
		i += 3
		file.append(str[start:end])
	i = 0
	index = 0
	while i != -1:
		index = i
		i = str.find("href", i)
		if (i < index):
			break
		start = str.find('"', i) + 1
		end = str.find('"', start)
		i += 3
		file.append(str[start:end])
	return (file)

# downloads all files reverenced in index.html
def get_all_src_href_files():
	index = open(folder + "/" + "index.html", 'r')
	index_html = index.read()
	files_to_download = src_href_files_names(index_html)
	for file in files_to_download:
		get_file(file)

def download_logo_images(images):
	images_list = images[1:-1].split("\",\"")
	for image in images_list:
		get_file("/logo/" + image + ".png")

# downloads all images reverenced in static/js/main*.js jason section
# and some witch arent
def get_images():
	images_start = main_js_content.find("JSON.parse('[{\"name\"") + 12
	images_end = main_js_content.find("]", images_start) + 1
	images_json = main_js_content[images_start:images_end]
	images_parsed_json = json.loads(images_json)
	for image in images_parsed_json:
		get_file(image['path'])
	images_parsed_json = json.loads("[{\"name\":\"crtoverlay\",\"path\":\"/crtoverlay.png\"},{\"name\":\"draainujescherm\",\"path\":\"/objects/draainujescherm.png\"},{\"name\":\"progressbar\",\"path\":\"/progressbar.png\"},{\"name\":\"progressbar-fill\",\"path\":\"/progressbar-fill.png\"},{\"name\":\"logo-zml\",\"path\":\"/logo-zml.png\"},{\"name\":\"logo-vpro\",\"path\":\"/logo-vpro.png\"},{\"name\":\"logo-npo3\",\"path\":\"/logo-npo3.png\"}]")
	for image in images_parsed_json:
		get_file(image['path'])
	images_start = main_js_content.find("var n=[\"")
	images_start = main_js_content.find("[", images_start) + 1
	images_end = main_js_content.find("]", images_start)
	images_logo = main_js_content[images_start:images_end]
	download_logo_images(images_logo)

# downloads all audio files reverenced in static/js/main*.js
def get_audio_file():
	audio_index =  main_js_content.find("a.tracks={")
	audio_end = main_js_content.find("}", audio_index)
	audio_end = main_js_content.find("}", audio_end + 1)
	str = main_js_content[audio_index:audio_end]
	i = 0
	while i != -1:
		index = i
		i = str.find(":\"/audio/", i)
		if (i < index or i == -1):
			break
		start = str.find("\"", i) + 1
		end = str.find("\"", start)
		i += 9
		get_file(str[start:end])

print ("downloading all files reverenced in index.html")
get_all_src_href_files()

static_js = os.listdir("./" + folder + "/static/js/")
main_js = 0
for js in static_js:
	if js.find("main") == -1:
		continue
	main_js = open("./" + folder + "/static/js/" + js)
main_js_content = main_js.read()

print ("downloading images")
get_images()
print ("downloading audio")
get_audio_file()
