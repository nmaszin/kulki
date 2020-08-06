class Config:
  def __init__(self, default, custom):
    self.default = default
    self.custom = custom
  
  def __contains__(self, property):
    return property in self.custom or property in self.default

  def __getitem__(self, property):
    return self.custom.get(property, self.default.get(property, None))
  
  def __setitem__(self, property, value):
    self.custom[property] = value
  
  def __delitem__(self, property):
    del self.custom[property]

  def clear(self):
    self.custom.clear()

  def all(self):
    return {**self.default, **self.custom}