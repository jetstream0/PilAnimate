from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance, ImageColor
import cv2
import numpy
from time import sleep
import os

class Animation:
  def __init__(self, layer_num, size=(1600,900), fps=25, mode="RGBA", color=0):
    self.layers = []
    self.fps = fps
    self.mode = mode
    self.size = size
    for i in range(layer_num):
      self.layers.append(Layer(size, fps, mode=mode, color=color))
  def export(self):
    frames = 0
    for frame_num in range(len(self.layers[0].frames)):
      frames += 1
      frame = Image.new(self.mode, self.size)
      for i in range(len(self.layers)):
        frame.paste(self.layers[i].frames[frame_num], mask=self.layers[i].frames[frame_num])
      frame.save("frames/"+str(frame_num)+".png")
    video = cv2.VideoWriter("hey.avi", cv2.VideoWriter_fourcc(*'XVID'), 30, self.size)
    #video = cv2.VideoWriter("hey.avi", 0, 1, self.size) 
    for frame_num in range(frames): 
      #video.write(numpy.array(frame))
      video.write(cv2.imread("frames/"+str(frame_num)+".png"))
    video.release()

class Layer:
  def __init__(self, size, fps, mode="RGBA", color=0):
    self.size = size;
    self.img = Image.new(mode, size, color=0)
    self.layer = ImageDraw.Draw(self.img)
    self.fps = fps;
    self.frames = [];
    self.mode = mode;

  #functions that draw stuff on
  def createPoint(self, coords, fill=None):
    self.layer.point(coords, fill=fill)
  def createLine(self, coords, fill=None, width=0, joint=None):
    self.layer.line(coords, fill=fill, width=width, joint=joint)
  def createArc(self, boundingBox, startAngle, endAngle, fill=None, width=0):
    self.layer.arc(boundingBox, startAngle, endAngle, fill=fill, width=width)
  def createEllipse(self, boundingBox, fill=None, outline=None, width=0):
    self.layer.ellipse(boundingBox, fill=fill, outline=outline, width=width)
  def createPolygon(self, coords, fill=None, outline=None):
    self.layer.polygon(coords, fill=fill, outline=outline)
  def createRectangle(self, boundingBox, fill=None, outline=None, width=1):
    self.layer.rectangle(boundingBox, fill=fill, outline=outline, width=width)
  def createRoundedRectangle(self, boundingBox, radius=0, fill=None, outline=None, width=0):
    self.layer.rounded_rectangle(boundingBox, radius=radius, fill=fill, outline=outline, width=width)
  def fillAll(self, fill=None, outline=None, width=0):
    self.layer.rectangle(((0,0),(1600,900)), fill=fill, outline=outline, width=width)
  def createText(self, anchorCoords, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None, features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False):
    self.layer.text(anchorCoords, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None, features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False)
  def addImage(self, imageToAdd, coords=None):
    self.img.paste(imageToAdd,box=coords)

  #translation functions
  def rotate(self, angle, center=None, outsideFillColor=None):
    self.img.rotate(angle, resample=0, center=center, fillcolor=outsideFillColor)
  def translate(self,x,y,img):
    """
    self.img.transform(self.size, Image.AFFINE, (0, 0, x, 0, 0, y))
    """
    newimg = Image.new(self.mode, self.size, color=0)
    newimg.paste(img, (round(0+x),round(0+y)), img)
    self.img = newimg

  #transparency functions

  #color change functions

  #image filter functions

  #blend

  #clear image functions
  def clear(self, coords):
    self.img.paste(0, coords)
  def clearAll(self):
    self.img.paste(Image.new(self.mode, self.size, color=0))

  #save frame image
  def saveFrame(self):
    self.frames.append(self.img.copy())
  def doNothing(self, frames):
    self.frames = self.frames+[self.img.copy()]*frames
    #for i in range(frames): self.saveFrame()

  #shortcut save functions (ie a function that translates every frame and also saves frame)
  def rise(self, frames, total_rise_amount):
    copy = self.img.copy()
    for i in range(frames):
      self.clearAll()
      #if last frame
      if i == frames-1:
        newimg = Image.new(self.mode, self.size, color=0)
        newimg.paste(copy, (0,total_rise_amount), copy)
        self.img = newimg
      self.translate(0,total_rise_amount/frames*i,copy)
      self.saveFrame()