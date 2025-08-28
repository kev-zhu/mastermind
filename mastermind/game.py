from .code_maker import CodeMaker
from .code_breaker import CodeBreaker

class Game:
  """Create instance instance of the game, handles game logic."""
  def __init__(self, code_length: int=4, code_range: int=8, max_attempt: int=10):
    if not str(code_length).isdigit() or code_length < 1:
      raise ValueError("code_length must be a positive integer.")
    if not str(code_range).isdigit() or code_range < 1:
      raise ValueError("code_range must be a positive integer.")
    if code_range > 9:
      raise ValueError("code_range must be less than 10. Increase code_length to accommodate for 10 if needed.")
    if not str(max_attempt).isdigit() or max_attempt < 1:
      raise ValueError("max_attempt must be a positive integer.")
    self.code_length = code_length
    self.code_range = code_range
    self.max_attempt = max_attempt
    self.code_maker = None
    self.code_breaker = None
    self.turn = 0
    self.current_game_history = [] # List[Tuple(CodeEntry, Feedback)]
    self.active_game = False
    self.hint_answer_dict = {}
    self.hint = ""
    self.current_guess = None
    self.current_feedback = None
    self.winner = None
    self.game_count = 0
    self.quit_game = None
    self.prev_match_history = {} #Dict{game_count (int): game_history (list)}
  
  def start(self) -> None:
    """Initialize players and set up start of game."""
    self.code_maker = CodeMaker(self.code_length, self.code_range)
    self.code_breaker = CodeBreaker(self.code_length, self.code_range)
    self.reset_game_state()

  def reset_game_state(self) -> None:
    """Resets the state of the game to simulate a start of a new game."""
    #reset game -- keep players, reset other game states
    self.code_maker.generate_code()
    self.hint_answer_dict = self.code_maker.get_hint_position_dict()
    self.hint = "x" * self.code_length
    self.active_game = True
    self.turn = 1
    self.code_breaker.turn = self.turn
    self.current_game_history = []
    self.current_guess = None
    self.current_feedback = None
    self.winner = None
    self.quit_game = False

  def run(self) -> None:
    """Runs entire game loop."""
    play_again = False
    #runs many iterations of the game
    while self.active_game or play_again:
      self.run_one_game()
      if not self.quit_game:
        self.update_prev_match_history()
      play_again = self.ask_play_again()
    print(f"Match history: {self.format_match_history()}Goodbye!")
 
  def run_one_game(self) -> None:
    """Runs one iteration of the game until winner decided."""
    self.game_count += 1
    while not self.is_over():
      if self.quit_game:
        return
      self.make_move()
    self.active_game = False
    print(f"The secret code was {self.code_maker.secret_code.sequence}. Congratulations, {self.winner} won this round!")  

  def quitting_game(self) -> None:
    """Set game states for quitting game."""
    #uncount this game_count before quitting
    self.game_count -= 1
    self.active_game = False
    self.quit_game = True

  def update_prev_match_history(self) -> None:
    """Update previous match history dictionary of current game's winner and game history."""
    self.prev_match_history[self.game_count] = (self.winner, self.current_game_history)

  def ask_play_again(self) -> bool:
    """Asks user if want to play again."""
    play_again_input = input("Do you want to play again (y/n)? ")
    if play_again_input and len(play_again_input) > 0 and play_again_input.lower()[0] == "y":
      self.reset_game_state()
      return True
    return False

  def make_move(self) -> None:
    """Perform a single game move: CodeBreaker guess, CodeMaker evaluate, update game's current_guess, current_feedback, and game state."""
    guess_code = self.request_code_breaker_guess()
    if self.quit_game:
      return
    self.current_guess = guess_code
    guess_feedback = self.request_code_maker_evalulation(guess_code)
    self.current_feedback = guess_feedback
    self.update_game_state()
  
  def request_code_breaker_guess(self) -> "CodeEntry":
    """Request Code Breaker to input a valid guess, returns a valid CodeEntry object that follows game restraints."""
    guess_code = self.code_breaker.make_guess()
    while not guess_code.is_valid():
      print(self.response_to_code_breaker_input(guess_code.sequence.lower()))
      if self.quit_game:
        return
      guess_code = self.code_breaker.make_guess()
    return guess_code
  
  def response_to_code_breaker_input(self, user_input: str) -> str:
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
        self.reveal_one_hint()
        return self.hint
      case "reset":
        self.reset_game_state()
        return "This game has been reset. A new secret code has been made and CodeBreaker is starting from turn #1."
      case "quit":
        self.quitting_game()
        return "You have left this game."
      case "history":
        formatted_curr_game_history = self.format_game_history(self.current_game_history)
        return formatted_curr_game_history
      case x if "previous" in x:
        prev_request_format_issue = "Please follow the format when looking up previous match histories: 'previous [number]'."
        user_input_arr = user_input.split()
        #validate proper format
        if len(user_input_arr) == 2:
          prev_str, prev_game_num = user_input_arr
          if prev_str == "previous" and prev_game_num.isdigit():
            #check for valid prev game num
            if 0 < int(prev_game_num) <= len(self.prev_match_history):
              target_match_history = self.prev_match_history[int(prev_game_num)]
              prev_game_winner, prev_game_history = target_match_history
              return f"Winner: {prev_game_winner}\n{self.format_game_history(prev_game_history)}"
            return f"You've only played {len(self.prev_match_history)} game(s) and can only look up the history for those."
          return prev_request_format_issue
        return prev_request_format_issue
      case _:
        return f"Enter {self.code_length} numbers ranging from 0-{self.code_range-1}, or input 'help' to see other commands."

  def reveal_one_hint(self) -> None:
    """Update current game's hint to reveal left most number of hidden sequence."""
    hidden_hint_pos = list(self.hint_answer_dict.keys())
    if len(hidden_hint_pos) > 0:
      selected_hint_pos = hidden_hint_pos[0]
      hint_array = list(self.hint)
      hint_array[selected_hint_pos] = self.hint_answer_dict[selected_hint_pos]
      self.hint = "".join(hint_array)
      del self.hint_answer_dict[selected_hint_pos]
    else:
      print(f"There are no more hints to give! The answer is:")

  def request_code_maker_evalulation(self, guess_code: "Code") -> "Feedback":
    """Request Code Maker to make evaluation of CodeEntry comparison quality."""
    requested_feedback = self.code_maker.evaluate_code(guess_code)
    print(requested_feedback.to_string())
    return requested_feedback

  def update_game_state(self) -> None:
    """Update current game history, turn counter, print remaining turn(s)."""
    self.current_game_history.append((self.current_guess, self.current_feedback))
    print(f"{self.max_attempt - self.turn} guess{'es' if self.turn != self.max_attempt-1 else ''} remaining.")
    self.turn += 1
    self.code_breaker.turn = self.turn

  def is_over(self) -> bool:
    """Check if game has ended and determine winner."""
    if self.turn > self.max_attempt:
      self.winner = "Code Maker"
      self.active_game = False
      return True
    elif self.current_feedback and self.current_feedback.is_perfect_response():
      self.winner = "Code Breaker"
      self.active_game = False
      return True
    return False

  def format_game_history(self, history: list) -> str:
    """Return formatted history of current guesses and feedback"""
    formatted = []
    for guess_count in range(len(history)):
      guess_code, guess_feedback = history[guess_count]
      formatted.append(f"Guess #{guess_count + 1}: {guess_code.to_string()} - {guess_feedback.to_string()}")
    return ("\n").join(formatted)

  def format_match_history(self) -> str:
    """Return shortened result of all games played and its winner."""
    matches = self.prev_match_history.keys()
    if not matches:
      return "No games played.\n"
   
    match_result_arr = [] 
    for match in matches:
      round_winner, _ = self.prev_match_history[match]
      match_result_arr.append(f"Game {match} Winner: {round_winner}")
    match_str = '\n'.join(match_result_arr)
    return f"\n{match_str}\n"