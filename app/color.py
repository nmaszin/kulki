import random

class Color:
  BACKGROUND = (20, 20, 20)
  BALL = (240, 0, 0)
  TRACKED_BALL = (100, 100, 240)
  BOUNCED_BALL = (240, 100, 100)
  TRACK = (14, 163, 54)

  @staticmethod
  def mix(weight, first_color, second_color):
    return tuple(map(lambda x: int(x[0] * weight + x[1] * (1 - weight)), zip(first_color, second_color)))

  @staticmethod
  def random():
    r = random.randint(20, 240)
    g = random.randint(20, 240)
    b = random.randint(20, 240)
    return (r, g, b)
