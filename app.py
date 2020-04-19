import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from predictor import predict
from pygame import mixer

class App:
	def __init__(self, window, window_title, video_source = 0):
		self.window = window
		self.window.title(window_title)
		mixer.init()

		self.vid = MyVideoCapture(video_source)

		self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
		self.canvas.pack()

		self.btn_snapshot = tkinter.Button(window, text = 'PREDICT',
			width=50, command = self.snapshot)

		self.btn_snapshot.pack(anchor=tkinter.CENTER, expand = True)

		self.btn_pause = tkinter.Button(self.window, text = 'PAUSE',
			width=50, command = self.pauseMusic)

		self.btn_pause.pack(anchor=tkinter.CENTER, expand = True)

		self.btn_play = tkinter.Button(self.window, text = 'PLAY',
			width=50, command = self.resumeMusic)

		self.btn_play.pack(anchor=tkinter.CENTER, expand = True)

		self.delay = 15
		self.update()

		self.window.mainloop()

	def resumeMusic(self):
		mixer.music.unpause()

	def pauseMusic(self):
		mixer.music.pause()

	def update(self):
		ret, frame = self.vid.get_frame()

		if ret:
			self.photo = PIL.ImageTk.PhotoImage(
				image = PIL.Image.fromarray(frame))
			self.canvas.create_image(0,0,image = self.photo, anchor = tkinter.NW)

		self.window.after(self.delay, self.update)

	def snapshot(self):
		ret, frame = self.vid.get_frame()

		if ret:
			cv2.imwrite("capture.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
			result = predict()
			print(result)
			self.selectMusic(result)

	def selectMusic(self, result):
		mxReaction = 'Neutral'
		try:
			for i in sorted(result.keys()):
				mxReaction = i
		except:
			print('No Match')

		song = ''
		if mxReaction == 'Happy':
			song='happy.mp3'
		elif mxReaction == 'Disgusted':
			song='disgust.mp3'
		elif mxReaction == 'Angry':
			song='anger.mp3'
		elif mxReaction == 'Fearful':
			song='fearful.mp3'
		elif mxReaction == 'Neutral':
			song='neutral.mp3'
		elif mxReaction == 'Sad':
			song='sad.mp3'
		else:
			#surprised
			song='surprise.mp3'

		mixer.music.load('/home/rohangoyal2014/Desktop/Major Project Work/Tensorflow/songs/'+song)
		mixer.music.play()


class MyVideoCapture:
	def __init__(self, video_source = 0):
		self.vid = cv2.VideoCapture(video_source)
		if not self.vid.isOpened():
			raise ValueError('Unable to open video source', video_source)

		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
	def get_frame(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			if ret:
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)

	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()

App(tkinter.Tk(), "Music Selection using Facial Emotion Recognition")
