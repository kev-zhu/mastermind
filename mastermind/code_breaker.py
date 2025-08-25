from .code_entry import CodeEntry

class CodeBreaker:
  """Instance of CodeBreaker player, handles ONLY its logic."""
  def __init__(self, code_length: int, code_range: int):
    self.code_length = code_length
    self.code_range = code_range
    self.turn = 1
  
  def make_guess(self) -> CodeEntry:
    """Request user to input guess, returns CodeEntry object."""
    guess = input(f"Input #{self.turn}: ")
    return CodeEntry(guess, self.code_length, self.code_range)