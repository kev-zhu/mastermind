class Feedback:
  """Formats result of code comparison and quality of guess."""
  def __init__(self, correct_number: int, correct_location: int, code_length: int):
    self.correct_number = correct_number
    self.correct_location = correct_location
    self.code_length = code_length

  def is_perfect(self) -> bool:
    """Returns True if all parts of Feedback responses match code length."""
    return self.correct_location == self.code_length and self.correct_number == self.code_length

  def to_string(self) -> str:
    """Returns a readable string of result."""
    plural = lambda x: "s" if x != 1 else ""
    return f"{self.correct_number} correct number{plural(self.correct_number)} and {self.correct_location} correct location{plural(self.correct_location)}"