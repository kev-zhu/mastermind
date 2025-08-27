from .code_maker import CodeMaker
from .code_breaker import CodeBreaker

class Game:
  """Create instance instance of the game, handles game logic."""
  def __init__(self, code_length: int=4, code_range: int=8, max_attempt: int=10):
    if (not str(code_length).isdigit() or code_length < 1):
      raise ValueError("code_length must be a positive integer.")
    elif (not str(code_range).isdigit() or code_range < 1):
      raise ValueError("code_range must be a positive integer.")
    elif (not str(max_attempt).isdigit() or max_attempt < 1):
      raise ValueError("max_attempt must be a positive integer.")
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
    self.code_breaker = CodeBreaker(self.code_length, self.code_range)
    
    #reset game -- keep players, reset other game states
    self.code_maker.generate_code()
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
      print(self.response_to_code_breaker_input(guess_code.sequence.lower()))
      guess_code = self.code_breaker.make_guess()
    return guess_code
  
  def response_to_code_breaker_input(self, user_input) -> str:
    """Analyze and respond to input user input. Returns string back in response to handling input."""
    commands = {
      "rules": "Rules of the game.",
      "help": "List of commands.",
      "hint": "Reveals a number and its position in the secret code.",
      "reset": "Resets the current game.",
      "quit": "Quits the current game.",
      "history": "Print current game guesses and feedbacks.",
      "previous [number]": "Print history of of the n-th game, if played.",
    }
    match(user_input):
      case "rules":
        return f"Mastermind: The goal of this game is to match your guess to a secret code of {self.code_length} numbers ranging from 0-{self.code_range} in {self.max_attempt} attempts."
      case "help":
        statement = []
        for command, brief in commands.items():
          statement.append(f"{command} - {brief}")
        return "\n".join(statement)
      case "hint":
        return "printing hint"
      case "reset":
        return "resetting game"
      case "quit":
        return "quitting game"
      case "history":
        return self.get_history()
      case x if "previous" in x:
        #WIP
        #validations for prev_game number
        _, prev_game = user_input.split()
        return f"printing history of Game #{prev_game}"
      case _:
        return f"Enter {self.code_length} numbers ranging from 0-{self.code_range-1}, or input 'help' to see other commands."

  def request_code_maker_evalulation(self, guess_code) -> "Feedback":
    """Request Code Maker to make evaluation of CodeEntry comparison quality."""
    requested_feedback = self.code_maker.evaluate_code(guess_code)
    print(requested_feedback.to_string())
    return requested_feedback

  def update_game_state(self) -> None:
    """Update history, turn counter, print remaining turn(s)."""
    self.history.append((self.current_guess, self.current_feedback))
    print(f"{self.max_attempt - self.turn} guess{'es' if self.turn != self.max_attempt-1 else ''} remaining.")
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