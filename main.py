from mastermind import Game

def main() -> None:
  """Entry point for starting a new Mastermind game."""
  new_game = Game()
  new_game.start()
  new_game.run()

if __name__ == "__main__":
  main()