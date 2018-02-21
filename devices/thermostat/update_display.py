
def update_display(display, payload):

  def calculate_width(font,text):
    w = 0
    for c in text:
        glyph, char_height, char_width = font.get_ch(c)
        w += char_width
    return w        

  try:
    
    command = {}
    
    if payload is None:
      
       # An example command for testing
      command = {
        "heating_state": True,
        "msg": "auto",
        "inside_temp": 23.456,
        "outside_temp": -9.876
      }
      
    else:
      try:
        import ujson as json
        command = json.loads(payload)
      except (OSError, ValueError):
        import kiota.Util as Util
        Util.log(update_display,"Can't parse payload: '{}'".format(payload))

    display.fill(0)

    ink = 1
    heating_state = command["heating_state"]
    
    if heating_state:
      ink = 0
      display.fill_rect(0,0,128,14,1)

    if command["msg"] is not None:
      display.text(str(command["msg"]), 0, 1, ink)

    if command["heating_state"]:
      display.text("ON", 104, 1, ink) 
    else:
      display.text("OFF", 104, 1, ink) 

    import KameronRegularNumbers25 as font
    from Writer import Writer
    writer = Writer(display, font)
    writer.set_clip(True, True)
    
    inside_temp = "--"
    try: inside_temp=str(int(round(float(command["inside_temp"]))))
    except: pass
    writer.set_textpos(23, int((64-calculate_width(font, inside_temp))/2))
    display.fill_rect(0, 15, 64, 41, 0)
    writer.printstring(inside_temp)
    
    outside_temp = "--"
    try: outside_temp=str(int(round(float(command["outside_temp"]))))
    except: pass
    writer.set_textpos(23, 64+int((64-calculate_width(font, outside_temp))/2))
    display.fill_rect(64, 15, 64, 41, 0)
    writer.printstring(outside_temp)

    display.text("inside", 0, 56) 
    display.text("outside", 72, 56) 

    display.show()
    
  except Exception as e:
    display.text("ERROR", 0, 0) 
    display.show()
    import sys
    sys.print_exception(e)

  return True

