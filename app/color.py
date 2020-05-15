import random

class Color:
  BACKGROUND = (20, 20, 20)
  BALL = (0, 240, 240)

  @staticmethod
  def random():
    r = random.randint(20, 240)
    g = random.randint(20, 240)
    b = random.randint(20, 240)
    return (r, g, b)
