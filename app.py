from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import random
import time
import numpy
import os
import cv2 as cv
from decord import VideoReader, cpu
import edge_tts
import asyncio
from moviepy import VideoFileClip, vfx, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import moviepy
import re
import threading
import fpstimer
from srt_equalizer import srt_equalizer
import json

"""
To do: 
- Some links make it so bot does not read whole thread. (done)
- Get out of opencv hell as it is slow as shit. (Done but need to test on a server)
- Fix frame timings for bad apple (good enough)
- Add subtitiles (It does exist)
- Add multiple voice support
- Add channel bot features which only work in #stunts-sanctuary (added welcome message)
- Upload slop videos via hack club cdn? (to solve timeout issue with large file uploads) (cant find one)
- more cat photos (done)
- fix channel id's not being read (done)
"""

########################################################################################################################
# Slack utils stuff
########################################################################################################################

ASCII_COLOURMAP = numpy.frombuffer(" @%#*+=-:."[::-1].encode(), dtype=numpy.uint8)

# Env shit
load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

slopify_slack_block = [{
			"type": "rich_text",
			"elements": [
				{
					"type": "rich_text_section",
					"elements": [
						{
							"type": "text",
							"text": "Enter the parameters here!"
						}
					]
				}
			]
		},
		{
			"type": "input",
			"block_id": "thread_link",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Thread Link",
				"emoji": False
			},
			"optional": False
		},
		{
			"type": "input",
			"block_id": "lang_iso_code",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Language (ISO Language Code)\t",
				"emoji": False
			},
			"optional": True
		},
		{
			"type": "input",
			"block_id": "gender",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": False
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Man",
							"emoji": False
						},
						"value": "Male"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Woman",
							"emoji": False
						},
						"value": "Female"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "I don't care",
							"emoji": False
						},
						"value": "Both"
					}
				],
				"action_id": "static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Voice Gender",
				"emoji": False
			},
			"optional": True
		}]
########################################################################################################################
# Channel Stuff
########################################################################################################################
def get_valid_channel_ids(filepath):
	with open(filepath, "r") as f:
		lst = f.readlines()
		for i in range(0, len(lst)):
			lst[i] = lst[i].replace("\n", "")
		return lst

@app.event("member_joined_channel")
def handle_member_joined(event, client, logger):
	user_id = event.get("user")
	channel_id = event.get("channel")

	try:
		user_info = client.users_info(user=user_id)
		display_name = user_info["user"]["profile"]["display_name"]

		channel_info = client.conversations_info(channel=channel_id)
		joined_channel_id = channel_info["channel"]["id"]
		valid_channel_ids = get_valid_channel_ids("channel_welcome_ids.txt")
		if joined_channel_id in valid_channel_ids:
			client.chat_postMessage(
				channel=channel_id,
				text=f"Haiii :haii: Welcome <@{user_id}> to my silly channel! Hope you have an amazing stay! :yay: <@U0A7QFF7X17> GET OVER HERE!"
			)

	except Exception as e:
		logger.error(f"Error handling member_joined_channel: {e}")

########################################################################################################################
# Slop generator
########################################################################################################################
def handle_mention(event, client, say):
	print("Recieved: " + event["text"])
	channel_id = event.get("channel")
	thread_ts = event.get("thread_ts")
	user_id = event.get("user")

	# Some mentions don't include slopify so shouldn't trigger anything.
	if "slopify" in event["text"].split() and thread_ts:
		# Getting all thread contents
		result = client.conversations_replies(channel=channel_id, ts=thread_ts)
		messages = result.get("messages", [])
		return messages, thread_ts, user_id
	# If pinged to slopify outside of a thread.
	elif "slopify" in event["text"].split() and not thread_ts:
		client.chat_postEphemeral(
			channel=channel_id,
			user=user_id,
			thread_ts=thread_ts,
			text="Mention me inside of the thread you want to slopify"
		)
		return None
	# Add other mention features here as necessary.

	return None

# REMINDER TO SELF: async lets other functions run whilst this is happening
# So whilst file is being saved other actions can happen with await
async def speak(text, lang = "en-GB", gender = "", name="output"):
	voices = await edge_tts.VoicesManager.create()
	print(gender)
	if gender not in ("Male", "Female"):
		gender = random.choice(["Male", "Female"])
	voice_bank = voices.find(Gender=gender, Locale=lang)
	print(voice_bank)
	if voice_bank == []:
		voice_bank = voices.find(Locale="en-GB")
	model = random.choice(voice_bank)["Name"]
	print(model)
	communicate = edge_tts.Communicate(text, voice = model, boundary="SentenceBoundary")

	submaker = edge_tts.SubMaker()
	with open(f"{name}.mp3", "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "SentenceBoundary":
				submaker.feed(chunk)

	with open(f"{name}_long.srt", "w", encoding="utf-8") as file:
		file.write(submaker.get_srt())

	srt_equalizer.equalize_srt_file(f"{name}_long.srt", f"{name}.srt", 30)
	os.remove(f"{name}_long.srt")

def upload_video(client, user_id, file_path, thread_ts):
	dm = client.conversations_open(users=user_id)
	try:
		dm_channel_id = dm["channel"]["id"]
		client.files_upload_v2(
			channel=dm_channel_id,  # DMs to the user directly
			file=file_path,
			title=f"Slopified video {thread_ts}"
		)
	except Exception as e:
		if e == "<urlopen error The write operation timed out>":
			client.chat_postMessage(channel=user_id,
									text=f"So the thread you wanted to slopify was too large to send over slack.\n"
										 f"So ummm... have fun?")
		else:
			client.chat_postMessage(channel=user_id,
								text=f"I'm to lazy to create actual error messages so here is what slack said went wrong.\n"
									 f"{e}")
		return
	os.remove(file_path)

def filter_script(client, messages):
	text = ""
	channel_cache = {}

	for message in messages:
		p = r'https?://\S+|www\.\S+'
		n_url = str(re.sub(p, "", message["text"]))
		parts = re.split(r"<@(U[A-Z0-9]+)(?:\|[^>]+)?>|<#(C[A-Z0-9]+)?>",n_url)
		# 3 groups per match: [text, user_id, chan_id]
		rebuilt = []
		for i in range(0, len(parts), 3):
			text_chunk = parts[i]
			if i + 1 < len(parts) :
				user_id = parts[i + 1]
			else:
				user_id = None
			if i + 2 < len(parts):
				chan_id = parts[i + 2]
			else:
				chan_id = None

			if text_chunk:
				rebuilt.append(text_chunk)

			if user_id:
				try:
					user_info = client.users_info(user=user_id)
					rebuilt.append(f"@{user_info["user"]["profile"]["display_name"]}")
				except Exception:
					rebuilt.append(f"@{user_id}")

			if chan_id:
				if chan_id not in channel_cache:
					try:
						channel_info = client.conversations_info(channel=chan_id)
						channel_cache[chan_id] = channel_info["channel"]["name"]
					except Exception:
						channel_cache[chan_id] = f"[Channel {chan_id}]"
				rebuilt.append(f"#{channel_cache[chan_id]}")

		msg = "".join(rebuilt)
		text += msg + ". "
	return text

def process_script(text, thread_ts, lang, gender):
	print("turning to audio")
	name = f"{thread_ts}{random.randint(1000, 9999)}"
	asyncio.run(speak(text=text, lang=lang, gender=gender, name=name))

	print("turing to video")
	audio_clip = AudioFileClip(f"{name}.mp3")

	mypath = "slop_videos"
	onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	file_i = random.randint(0, len(onlyfiles) - 1)

	video_clip = (
		VideoFileClip(f"{mypath}/{onlyfiles[file_i]}")
		.with_volume_scaled(0)
	).with_effects([vfx.Loop(duration=audio_clip.duration)])

	video_clip.audio = audio_clip.subclipped(0, video_clip.duration)

	generator = lambda txt: TextClip(text = txt, font="arial.ttf", font_size=24, color="white", method='caption', size=(video_clip.w, int(video_clip.h/5)))
	subtitles = SubtitlesClip(f'{name}.srt', make_textclip=generator)


	video_clip = CompositeVideoClip((video_clip, subtitles))
	video_clip.write_videofile(f"{name}.mp4")
	os.remove(f"{name}.mp3")
	os.remove(f"{name}.srt")
	return name

@app.event("app_mention")
def handle_slop_mention(event, client, say):
	messages, thread_ts, user_id = handle_mention(event, client, say)
	client.chat_postMessage(channel=user_id,
							text="generating your video be patient as it can take a while")
	text = filter_script(client, messages)
	name = process_script(text, thread_ts, lang="en-GB", gender="")
	threading.Thread(target=upload_video, args=(client, user_id, f"{name}.mp4", thread_ts)).start()

def determine_state(link_text):
	return link_text.split("?")

@app.command("/slopify")
def open_slopify_menu(ack, body, command, client):
	ack()
	user_id = command["user_id"]
	client.views_open(
		trigger_id=body["trigger_id"],
		view={
			"type": "modal",
			"callback_id": "slopify_request",
			"title": {"type": "plain_text", "text": "Enter Details"},
			"submit": {"type": "plain_text", "text": "Submit"},
			"blocks": slopify_slack_block,
			"private_metadata": f"{user_id}"
		}
	)

@app.view("slopify_request")
def handle_slopify_response(ack, view):
	ack()
	thread_link = view["state"]["values"]["thread_link"]["plain_text_input-action"]["value"]
	lang_iso_code = view["state"]["values"]["lang_iso_code"]["plain_text_input-action"]["value"]
	gender = view["state"]["values"]["gender"]["static_select-action"]["selected_option"]["value"]
	user_id = view['private_metadata']
	create_slop(thread_link, lang_iso_code, gender, user_id)


def create_slop(url, lang_iso_code, gender, user_id):
	print("Triggered")
	client = app.client
	try:
		msg_info = determine_state(url)
		if len(msg_info) == 2:
			info_str = msg_info[1].split("&")
			channel_id = info_str[1][4:]
			thread_ts = info_str[0][10:]

		elif len(msg_info) == 1:
			info_str = msg_info[0].split("/")
			channel_id = info_str[-2]
			unfiltered_thread_ts = info_str[-1][1:]
			thread_ts = f"{unfiltered_thread_ts[:-6]}.{unfiltered_thread_ts[-6:]}"

		else:
			channel_id = None
			thread_ts = None
	except Exception as e:
		client.chat_postMessage(channel=user_id,
								text=f"Error occured trying to process the request. Most likely invalid URL.")
		return
	try:
		result = client.conversations_replies(channel=channel_id, ts=thread_ts)
		messages = result.get("messages", [])
	except Exception as e:
		client.chat_postMessage(channel=user_id,
								text=f"I'm to lazy to create actual error messages so here is what slack said went wrong.\n"
									 f"{e}")
		return

	# Messages found so sending confirmation
	client.chat_postMessage(channel=user_id,
							text="generating your video be patient as it can take a while")

	text = filter_script(client, messages)
	name = process_script(text, thread_ts, lang_iso_code, gender)
	threading.Thread(target=upload_video, args=(client, user_id, f"{name}.mp4", thread_ts)).start()

########################################################################################################################
# Bad Apple generator
########################################################################################################################

def frame_to_gs(frame):
	"""
	Greyscales a single frame and returns the frame
	:param frame: singlular RGB numpy frame
	:return: singuar Greyscaled numoy frame
	"""
	# Vector Calc to convert whole frame in 1 go. Storing frame as unsigned 16 bit int
	return ((frame[:, :, 0] * 0.299) + (frame[:, :, 1] * 0.587) + (frame[:, :, 2] * 0.114)).astype(numpy.uint16)


def frame_to_ascii(frame, colourmap):
	"""
	Converts a greyscaled numoy frame into an ASCII frame
	"""
	# Formula for calcing ascii value stolen from stackoverflow
	# colourmap length subtracted from 1 due to potential index errors.
	# Once frame is converted the colourmap is applied to whole frame
	frame = colourmap[((frame[:] * (len(colourmap) - 1)) // 255).astype(numpy.uint8)]
	# Maps entire row to corresponding ascii character and adds that row to the string as 1 long string.
	# frame is still in raw bytes so we need to decode it
	return frame.tobytes().decode()


def create_video_obj(video_file: str, width, height):
	vr = VideoReader(video_file, cpu(), width = width, height = height)
	return vr

@app.command("/badapple")
def handle_badapple_command(ack, say, command):
	ack()
	print("Acknowledged")
	client = app.client

	# Get height and width
	nums = command.get("text", "")

	try:
		width, height = nums.split()
		width = int(width)
		height = int(height)
	except Exception:
		width = 80
		height = 24

	print_frame = say(text="```Loading Video```")

	message_ts = print_frame["ts"]
	channel_id = print_frame["channel"]

	vo = create_video_obj("BadApple.mp4", width, height)
	timer = fpstimer.FPSTimer(1)

	for frame_num in range(0, len(vo), 30):
		frame_raw = frame_to_ascii(frame_to_gs(vo[frame_num].asnumpy()), ASCII_COLOURMAP)
		row_lst = []
		for i in range(0, len(frame_raw), width):
			row_lst.append((frame_raw[i:i + width]))
		frame = "\n".join(row_lst)
		client.chat_update(
				channel=channel_id,
				ts=message_ts,
				text=f"```{frame}```"
			)
		timer.sleep()

########################################################################################################################
# Cat generator
########################################################################################################################

@app.command("/generatecat")
def handle_cat_gen_command(ack, say, command):
	ack()
	print("recieved!")
	client = app.client

	nums = command.get("text", "")
	try:
		width, height = nums.split()
		width = int(width)
		height = int(height)
	except Exception:
		# Defaults in case of no/invalid args
		width = 80
		height = 24

	mypath = "cat"
	onlyfiles = []
	for file in os.listdir(mypath):
		if os.path.isfile(os.path.join(mypath, file)):
			onlyfiles.append(file)

	file_i = random.randint(0, len(onlyfiles) - 1)
	img = cv.imread(f"cat\\{onlyfiles[file_i]}")
	img = cv.resize(img, (width, height))

	img_vals = frame_to_gs(img)
	img = frame_to_ascii(img_vals, ASCII_COLOURMAP)
	img_lst = []
	for i in range(0, len(img), width):
		img_lst.append((img[i:i + width]))

	i = 0
	length = 0
	msg = ""
	# Splits large messages into many small ones
	try:
		while i < len(img_lst):
			length += width
			if length > 3000:
				say(text=f"```{msg}```")
				msg = ""
				length = 0
			msg += "\n" + img_lst[i]
			i += 1
		say(text=f"```{msg}```")

	# Lazy man's error catching
	except Exception as e:
		say(text=f"```{e}```")

# Start your app
if __name__ == "__main__":
	SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
