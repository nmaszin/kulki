import random

class Color:
  BACKGROUND = (20, 20, 20)
  BALL = (240, 0, 0)
  TRACKED_BALL = (100, 100, 240)
  TRACK = (14, 163, 54)

  @staticmethod
  def random():
    r = random.randint(20, 240)
    g = random.randint(20, 240)
    b = random.randint(20, 240)
    return (r, g, b)
