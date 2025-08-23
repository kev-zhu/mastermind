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
    """
    This will start the game itself

    Initialize CodeMaker and CodeBreaker to begin game
    Run game into a loop for the range in number of attempts
    Run functions, validations, and updates for each turn
    """
    pass

  def make_move():
    """
    Singular game move

    This will encompass the following:
    - Ask CodeBreaker to make a vaid guess
    - Ask CodeMaker to check guess
    - Get feedback
    - Update turns, history, and any other variables
    - Check state of game
    """
    pass

  def is_over() -> str:
    """
    Analyze feedback's properties to see if game is over
    
    Ends round if winner determined, otherwise continue with game

    Returns a string of who the winner is this round
    """
    pass

  def get_history() -> str:
    """
    Print out formatted history of current game

    Returns a formatted string/log of history: (Turn) - (Code), (Feedback)
    """
    pass


class CodeBreaker:
  """For creating an instance of CodeBreaker player and handles ONLY its logic"""
  def __init__(self, code_length, code_range):
    self.code_length = code_length
    self.code_range = code_range

  def make_guess(self) -> "Code":
    """
    Asks user to input a guess
    Validate user's guess with Code requirements/rules
    If invalid, reiterate this request until Code is valid
    """
    pass

  def validate_guess(self) -> bool:
    """
    Ensures that the guess that the CodeBreaker inputs is of valid length and value
    
    Calls on Code.validate() to verify

    Returns true if code is valid, otherwise, game will ask player to make another guess following rules
    """
    pass


class CodeMaker:
  """
  For creating instance of CodeMaker and handles ONLY its logic
  - Stores secret code
  - Calls on code comparison
  """
  def __init__(self, code_length, code_range):
    self.code_length = code_length
    self.code_range = code_range
    self.secret_code = None

  def make_code(self) -> "Code":
    """
    Generate secret code
    
    Use API call (or user entry option later)
    - Ensure that API call has try/except block to handle failure with API call promise
    - Ensure this method is asynchronous to account for time of API call
    - Parse, format the Code, and make sure it is also valid
    - Store generated code as Code obj under secret_code
    """
    pass

  def evaluateCode(self, guess_code) -> "Feedback":
    """
    Calls on Code.compare() to make a comparison between guess_code and secret_code
    Returns Feedback object
    """
    pass


class Code():
  """Handles ONLY Code logic"""
  def __init__(self, sequence, length_rule, range_rule):
    self.sequence = sequence
    pass
  
  def compare_with(self) -> "Feedback":
    """
    Comparison logic between two codes, regardless of where it comes from
    Returns Feedback object after comparison
    """
    pass

  def validate(self) -> bool:
    """Validates if Code follows rule, if not return False"""
    pass

  def to_string(self) -> str:
    """Return Code object into a readable user friendly format"""
    pass


class Feedback():
  """For formatting result of Code comparison and quality of guess"""
  def __init__(self, correct_number, correct_location):
    self.correct_number = correct_number
    self.correct_location = correct_location

  def is_perfect(self) -> bool:
    """Return True if guess is a perfect replica of the secret and trigger the game's end"""
    pass

  def to_string(self) -> str:
    """Return Feedback object into a readable user friendly format"""
    pass
  