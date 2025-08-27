from .code_maker import CodeMaker
from .code_breaker import CodeBreaker

class Game:
  """Create instance instance of the game, handles game logic."""
  def __init__(self, code_length: int=4, code_range: int=8, max_attempt: int=10):
    self.code_length = code_length
    self.code_range = code_range
    self.max_attempt = max_attempt
    self.code_maker = None
    self.code_breaker = None
    self.turn = 0
    self.history = [] # List[Tuple(CodeEntry, Feedback)]
    self.active_game = False
    self.current_guess = None
    self.current_feedback = None
    self.winner = None
  
  def start(self) -> None:
    """Initialize players, set up game, and prepare to run game loop."""
    self.code_maker = CodeMaker(self.code_length, self.code_range)
    self.code_maker.generate_code()
    self.code_breaker = CodeBreaker(self.code_length, self.code_range)
    ### delete later -- for testing purposes only
    print(f'secret code generated it is {self.code_maker.secret_code.to_string()}')
    self.active_game = True
    self.turn = 1
    self.history.clear()
    self.current_guess = None
    self.current_feedback = None
    self.winner = None

  def run(self) -> None:
    """Runs the game loop after."""
    while self.active_game and not self.is_over():
      self.make_move()
    self.active_game = False
    print(f"The secret code was {self.code_maker.secret_code.sequence}. Congratulations, {self.winner} won this round!")  

  def make_move(self) -> None:
    """Perform a single game move: CodeBreaker guess, CodeMaker evaluate, update game's current_guess and current_feedback."""
    guess_code = self.request_code_breaker_guess()
    self.current_guess = guess_code
    guess_feedback = self.request_code_maker_evalulation(guess_code)
    self.current_feedback = guess_feedback
    self.update_game_state()
  
  def request_code_breaker_guess(self) -> "CodeEntry":
    """Request Code Breaker to input a valid guess, returns a valid CodeEntry object that follows game restraints."""
    guess_code = self.code_breaker.make_guess()
    while not guess_code.is_valid():
      #case switch here for inputs that arent code history, rules, quit, hint?
      if guess_code.sequence.lower() == "h" or guess_code.sequence.lower() == "history":
        print(self.get_history())
      else:
        print(f"Enter {self.code_length} numbers ranging from 0-{self.code_range - 1}.")
      guess_code = self.code_breaker.make_guess()
    return guess_code
  
  # def analyze_code_breaker_input(self, user_input) -> str:
  #   """Analyze the input and print a statement/handle game logic before returning it back?"""
  #   pass

  def request_code_maker_evalulation(self, guess_code) -> "Feedback":
    """Request Code Maker to make evaluation of CodeEntry comparison quality."""
    requested_feedback = self.code_maker.evaluate_code(guess_code)
    print(requested_feedback.to_string())
    return requested_feedback

  def update_game_state(self) -> None:
    """Update history and turn counter."""
    self.history.append((self.current_guess, self.current_feedback))
    self.turn += 1
    self.code_breaker.turn = self.turn

  def is_over(self) -> bool:
    """Check if game has ended and determine winner."""
    if self.turn > self.max_attempt:
      self.winner = "Code Maker"
      return True
    elif self.current_feedback and self.current_feedback.is_perfect():
      self.winner = "Code Breaker"
      return True
    return False

  def get_history(self) -> str:
    """Print out formatted history of current guesses and feedback"""
    formatted = []
    for guess_count in range(len(self.history)):
      guess_code, guess_feedback = self.history[guess_count]
      formatted.append(f"Guess #{guess_count + 1}: {guess_code.to_string()} - {guess_feedback.to_string()}")
    return ("\n").join(formatted)