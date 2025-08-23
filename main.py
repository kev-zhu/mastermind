# 10 attempts
# guess against set of 4 numbers that is randomly generated intially (of 8 diff numbers)
# computer feedback is given on how many numbers are correct and how many are at the right location
# computer feedback does not reveal which number player guessed is correct
# 
# any UI is fine, command line is fine
# players must be able to interact: 
#   guess 4 combo
#   view history of guesses and feedback
#   number of guesses remaining is displayed
# 
# implementation:
# use random num generator API to selected 4 numbers from 0-7 (dupes allowed)
# any language, tools, frameworks, and libraries are allowed within reason 

class Game:
  """For creating an instance of the game and handles ONLY the game logic"""
  def __init__(self, code_length=4, code_range=8):
    self.code_length = code_length
    self.code_range = code_range
    self.turn = 1
    self.max_attempt = 10
    self.history = [] # [(guess, feedback)]
    self.code_maker = None
    self.code_breaker = None
  
  def start():
    """Initialize players to begin game and loop through turns."""
    pass

  def make_move():
    """
    Singular game move that run logic/functions, validations, and updates variables for each turn.

    This will encompass the following:
    - Ask CodeBreaker to make a vaid guess
    - Ask CodeMaker to check guess
    - Get feedback
    - Update turns, history, and any other variables
    - Check state of game
    """
    pass

  def is_over() -> bool:
    """
    Analyze feedback's properties and ends round if winner is determined.

    Returns:
      bool: True if either player wins, False otherwise.
    """
    pass

  def get_history() -> str:
    """
    Print out formatted history of current game.

    Returns:
      string: Formatted string/log of history: (Turn) - (Code), (Feedback).
    """
    pass


class CodeBreaker:
  """For creating an instance of CodeBreaker player and handles ONLY its logic."""
  def __init__(self, code_length, code_range):
    self.code_length = code_length
    self.code_range = code_range

  def make_guess(self) -> "Code":
    """
    Request user input until valid guess is given.

    Validate user's guess with Code requirements/rules
    If invalid, reiterate this request until Code is valid

    Returns:
      Code: Object to hold information about valid user input.
    """
    pass

  def validate_guess(self) -> bool:
    """
    Ensures the guess input is valid in both length and value.
    
    Calls on Code.validate() to verify

    Returns:
      bool: True if code sequence is valid, else False.
    """
    pass


class CodeMaker:
  """For creating instance of CodeMaker player and handles ONLY its logic."""
  def __init__(self, code_length, code_range):
    self.code_length = code_length
    self.code_range = code_range
    self.secret_code = None

  def make_code(self) -> "Code":
    """
    Generate secret code.
    
    Use API call (or user entry option later)
    - Ensure that API call has try/except block to handle failure with API call promise
    - Ensure this method is asynchronous to account for time of API call
    - Parse, format the Code, and make sure it is also valid
    - Store generated code as Code obj under secret_code

    Returns:
      Code: Valid Code obj with sequence generated from random API.
    """
    pass

  def evaluateCode(self, guess_code) -> "Feedback":
    """
    Calls on a comparison between CodeMaker's secrete code and CodeBreaker's guess code.
    
    Returns:
      Feedback: Formatted object of the user's guess comparison result.
    """
    pass


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
    pass

  def validate(self) -> bool:
    """
    Checks if Code sequence follows rule.
    
    Returns:
      bool: True if sequence is valid, otherwise False.
    """
    pass

  def to_string(self) -> str:
    """Return Code object into a readable user friendly format."""
    pass


class Feedback():
  """For formatting result of Code comparison and quality of guess."""
  def __init__(self, correct_number, correct_location, code_length):
    self.correct_number = correct_number
    self.correct_location = correct_location
    self.code_length = code_length

  def is_perfect(self) -> bool:
    """
    Response to a guess being a perfect match.
    
    Returns:
      bool: True if guess all correct numbers and locations at max code length."""
    pass

  def to_string(self) -> str:
    """Returns a readable formatted string of this result."""
    pass
  