import requests
import time
import random
from .code_entry import CodeEntry
from .feedback import Feedback

class CodeMaker:
  """Instance of CodeMaker player, stores secret code, handles ONLY its logic."""
  def __init__(self, code_length: int, code_range: int):
    self.code_length = code_length
    self.code_range = code_range
    self.secret_code = None

  def generate_code(self, max_retries: int=3, delay: int=3) -> None:
    """Update secrete code after API call or fallback in-house random sequence generation."""
    api_url = f"https://www.random.org/integers/?num={self.code_length}&min=0&max={self.code_range - 1}&col=1&base=10&format=plain&rnd=new"
    
    for attempt in range(max_retries):
      try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = "".join(response.text.strip().split())
        self.secret_code = CodeEntry(data, self.code_length, self.code_range)
        return
      except requests.exceptions.RequestException:
        print(f"Problem with connecting to random API. Reattempting API call...")
        if attempt < max_retries - 1:
          time.sleep(delay)
        else:
          self.secret_code = CodeEntry(self.use_in_house_random_seq_gen(), self.code_length, self.code_range)
          print("Max retries exceeded. Generate random code again later, or try playing with in-house generated secret code :).")

  def use_in_house_random_seq_gen(self) -> str:
    """Generates random code sequence as fallback, returns random sequence."""
    s = ""
    for _ in range(self.code_length):
      s += (str)(random.randint(0, self.code_range - 1))
    return s

  def evaluate_code(self, guess_code: CodeEntry) -> Feedback:
    """
    Calls a comparison between CodeMaker's secrete code and CodeBreaker's guess code, return Feedback object.
    
    Returns:
      Feedback: Formatted object of the user's guess comparison result.
    """
    return self.secret_code.compare_with(guess_code)