from collections import Counter
import requests
import time
import random

class Game:
  """For creating an instance of the game and handles ONLY the game logic"""
  def __init__(self, code_length=4, code_range=8, max_attempt=10):
    self.code_length = code_length
    self.code_range = code_range
    self.turn = 1
    self.max_attempt = max_attempt
    self.history = [] # [(Code, Feedback)]
    self.code_maker = None
    self.code_breaker = None
    self.active_game = False

    self.current_guess = None
    self.current_feedback = None
    self.winner = None
  
  def start(self):
    """Initialize players to begin game and loop through turns."""
    self.code_maker = CodeMaker(self.code_length, self.code_range)
    self.code_maker.generate_code()
    ### delete later -- for testing purposes only
    # print(f'secret code generated it is {self.code_maker.secret_code.to_string()}')

    self.code_breaker = CodeBreaker(self.code_length, self.code_range)
    self.active_game = True

    while self.active_game and not self.is_over():
      self.code_breaker.turn = self.turn
      self.make_move()

    self.active_game = False
    print(f"The secrete code was {self.code_maker.secret_code}. {self.winner} won this round!")  

  def make_move(self):
    """
    Singular game move that run logic/functions, validations, and updates variables for each turn.

    This will encompass the following:
    - Ask CodeBreaker to make guess
    - Validate CodeBreaker's guess or ask to re-guess
    - Ask CodeMaker to check guess with secret
    - Get feedback
    - Update turns, history, and any other variables
    - Check state of game
    """
    guess_code = self.code_breaker.make_guess()
    while not guess_code.is_valid():
      #case switch here for inputs that arent code history, rules, quit, hint?
      if guess_code.sequence.lower() == "h" or guess_code.sequence.lower() == "history":
        print(self.get_history())
        guess_code = self.code_breaker.make_guess()
        continue
      print(f"Enter {self.code_length} numbers ranging from 0-{self.code_range - 1}.")
      guess_code = self.code_breaker.make_guess()

    self.current_guess = guess_code
    fb = self.code_maker.evaluate_code(guess_code)
    # fb = self.code_maker.secret_code.compare_with(guess_code)
    self.current_feedback = fb
    print(fb.to_string())
    self.update_game_state()
  
  def update_game_state(self):
    """Update history, turns, and other variables that the game tracks."""
    self.history.append((self.current_guess, self.current_feedback))
    self.turn += 1

  def is_over(self) -> bool:
    """
    Analyze feedback's properties and game state to determine if game is over.

    Returns:
      bool: True if either player wins, False otherwise.
    """
    if self.turn > 10:
      self.winner = "Code Maker"
      return True
    elif self.current_feedback and self.current_feedback.is_perfect():
      self.winner = "Code Breaker"
      return True
    return False

  def get_history(self) -> str:
    """
    Print out formatted history of current game.

    Returns:
      string: Formatted string/log of history: (Turn): (Code) - (Feedback).
    """
    f_history = []
    for guess_count in range(len(self.history)):
      guess_code, guess_feedback = self.history[guess_count]
      f_history.append(f"Guess #{guess_count + 1}: {guess_code.to_string()} - {guess_feedback.to_string()}")
    return ("\n").join(f_history)


class CodeBreaker:
  """For creating an instance of CodeBreaker player and handles ONLY its logic."""
  def __init__(self, code_length, code_range):
    self.code_length = code_length
    self.code_range = code_range
    self.turn = 0
  
  def make_guess(self) -> "Code":
    """Request user to input guess."""
    guess = input(f"Input #{self.turn}: ")
    return Code(guess, self.code_length, self.code_range)


class CodeMaker:
  """For creating instance of CodeMaker player and handles ONLY its logic."""
  def __init__(self, code_length, code_range):
    self.code_length = code_length
    self.code_range = code_range
    self.secret_code = None

  def generate_code(self, max_retries=3, delay=3):
    """
    Generate secret code.
    
    Use API call (or user entry option later)
    - Ensure that API call has try/except block to handle failure with API call promise
    - Parse, format the Code, and make sure it is also valid
    - Store generated code as Code obj under secret_code

    Returns:
      Code: Valid Code obj with sequence generated from random API.
    """
    api_url = f"https://www.random.org/integers/?num={self.code_length}&min=0&max={self.code_range - 1}&col=1&base=10&format=plain&rnd=new"
    
    for attempt in range(max_retries):
      try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = "".join(response.text.strip().split())
        self.secret_code = Code(data, self.code_length, self.code_range)
        return
      except requests.exceptions.RequestException:
        print(f"Problem with connecting to random API. Reattempting API call...")
        if attempt < max_retries - 1:
          time.sleep(delay)
        else:
          self.secret_code = Code(self.in_house_random_seq_gen(), self.code_length, self.code_range)
          print("Max retries exceeded. Generated random code again later, or try playing with in-house generated secret code :).")

  def in_house_random_seq_gen(self):
    """Generates random code as backup when API is down"""
    s = ""
    for _ in range(self.code_length):
      s += (str)(random.randint(0, self.code_range - 1))
    return s

  def evaluate_code(self, guess_code) -> "Feedback":
    """
    Calls on a comparison between CodeMaker's secrete code and CodeBreaker's guess code.
    
    Returns:
      Feedback: Formatted object of the user's guess comparison result.
    """
    return self.secret_code.compare_with(guess_code)


class Code():
  """Handles ONLY Code logic."""
  def __init__(self, sequence, length_rule, range_rule):
    self.sequence = sequence
    self.length_rule = length_rule
    self.range_rule = range_rule
  
  def compare_with(self, other_code) -> "Feedback":
    """
    Comparison logic between two Code objects, regardless of where it comes from.

    Args:
      other_code(Code): the other Code object being compared to.
   
    Returns:
      Feedback: Organized format for based off of the comparsion logic.
    """
    def count_num():
      count = 0
      this_dict = Counter(self.sequence)
      other_dict = Counter(other_code.sequence)
      
      for key in other_dict.keys():
        if this_dict[key]:
          count += min(this_dict[key], other_dict[key])
      return count

    def count_loc():
      count = 0
      for i in range(len(self.sequence)):
        if(self.sequence[i] == other_code.sequence[i]):
          count += 1
      return count

    correct_num_count = count_num()
    correct_loc_count = count_loc()

    return Feedback(correct_num_count, correct_loc_count, self.length_rule)

  def is_valid(self) -> bool:
    """
    Checks if Code sequence follows digit, length, and range rules.
    
    Returns:
      bool: True if sequence is valid, otherwise False.
    """
    # length validity
    if len(self.sequence) != self.length_rule:
      return False
    # digits validity
    elif not self.sequence.isdigit():
      return False
    # range validiity
    elif not all(map(lambda x: 0 <= int(x) < self.range_rule, self.sequence)):    
      return False
    else:
      return True

  def to_string(self) -> str:
    """Return Code object into a readable user friendly format."""
    return self.sequence


class Feedback():
  """For formatting result of Code comparison and quality of guess."""
  def __init__(self, correct_number, correct_location, code_length):
    self.correct_number = correct_number
    self.correct_location = correct_location
    self.code_length = code_length

  def is_perfect(self) -> bool:
    """Response to a guess being a perfect match."""
    return self.correct_location == self.code_length and self.correct_number == self.code_length

  def to_string(self) -> str:
    """Returns a readable formatted string of this result."""
    plural = lambda x: "s" if x != 1 else ""
    return f"{self.correct_number} correct number{plural(self.correct_number)} and {self.correct_location} correct location{plural(self.correct_location)}"
  

def main():
  new_game = Game()
  new_game.start()

if __name__ == "__main__":
  main()