from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance, ImageColor

def createBarGraphBar(layer, bottomRight, label, value, height, width, rectangleFill, textFill, textFont):
  #the bar
  layer.createRectangle(((bottomRight[0]-width, bottomRight[1]+height),(bottomRight[0], bottomRight[1])), fill=rectangleFill, outline=None, width=1)
  #value 
  layer.createText((bottomRight[0]-width, bottomRight[1]+height+15), value, fill=textFill, font=textFont)
  #label
  layer.createText((bottomRight[0]-width, bottomRight[1]-15), label, fill=textFill, font=textFont)
  

def createBarGraphLine(layer, values, coords, lineHeight, graphLineFill, width=2):
  #the side line
  layer.createLine([coords[0],coords[1]], fill=graphLineFill, width=width)
  #bottom line
  layer.createLine([coords[0],(coords[0][0]+lineHeight, coords[0][1])], fill=graphLineFill, width=width)
  #layer.createText((), values[0], fill=None, font=None)
  for i in range(len(values)-1):
    addition = (coords[1][1]-coords[0][1])*(i+1)
    layer.createLine([(coords[0][0], coords[0][1]+addition),(coords[0][0], coords[0][1]+addition)], fill=graphLineFill, width=width)
    #add text to the line
    #layer.createText((), values[i+1], fill=None, font=None)
