class Rectangle:
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
  
  def contains(self, point):
    """
    Returns True if rectangle contains point
    """
    return self.x <= point.x <= self.width and self.y <= point.y <= self.height
  
  def left(self):
    return self.x

  def top(self):
    return self.y
  
  def right(self):
    return self.x + self.width
  
  def bottom(self):
    return self.y + self.height


    