from app.math.vector import Vector

class TransformationMatrix:
  def __init__(self, unit_vector_x, unit_vector_y):
    self.a, self.b = unit_vector_x.x, unit_vector_x.y
    self.c, self.d = unit_vector_y.x, unit_vector_y.y
  
  def __mul__(self, scale):
    return TransformationMatrix(
      Vector(self.a, self.b) * scale,
      Vector(self.c, self.d) * scale
    )

  def inverse(self):
    a, b, c, d = self.a, self.b, self.c, self.d
    scale = 1 / (a * d - b * c)
    matrix = TransformationMatrix(
      Vector(d, -b),
      Vector(-c, a)
    )

    return matrix * scale
  
  def multiple_by_vector(self, vector):
    a, b, c, d = self.a, self.b, self.c, self.d
    return Vector(
      a * vector.x + c * vector.y,
      b * vector.x + d * vector.y
    )

  def to_base(self, vector):
    matrix = self.inverse()
    return matrix.multiple_by_vector(vector)
  
  def from_base(self, vector):
    return self.multiple_by_vector(vector)