# Mastermind Introduction

Mastermind is a game where a player tries to break a secret code. In this project, the default setup asks the player to break a random, 4 digit-code with numbers ranging from 0-7. The player wins a round if they discover the secret code sequence within 10 attempts.

## Installation and Setup

1. Ensure that Python is installed on your operating system.<br><br>
   Python version 3.10.5 was used for this project.<br>
   Download Python here: https://www.python.org/downloads/

2. Ensure that these external libraries are installed (“pip install” if you have pip):
   - `requests`	&rarr; `pip install requests`
   - `pytest`	&rarr; `pip install pytest`

3. Navigate to the directory containing `main.py`.

4. Run the program on the terminal with:`python main.py()`

## Playing the game

After running `python main.py()`, you will be given instructions and prompted on the terminal to make a guess. As the rules state, you must input a sequence of numbers to guess the code within the allowed attempts. You can also enter the command `help` for more options.<br><br> Good luck and have fun! :)

## Technologies

- `Python`
- `RANDOM.ORG API`
- `pytest Testing Framework`

## The Process (at a high level)

I began this project by spending some time researching the game and playing a few rounds of it online. This allowed me to understand the core features of the game. After receiving more instructions on how it should be implemented, I noted key features for implementation and listed the game logic on the side. A high-level plan for the structure of the game was drawn out on a whiteboard. While I initially thought that this game could be implemented in a single file, I ultimately decided to organize the program into different classes to better deconstruct the problem as a whole and plan the logic behind each of the components. This modular approach enabled better organization for future extensions and implementation, and allowed for easier unit testing of the classes’ methods in the future.

Once I decided on the key classes and their interactions, I built a prototype with skeleton code in a single file. After clarifying how each class and method should interact, with careful documentation using docstrings and type hints, I coded the logic. As the file grew in size, I refactored the classes into separate files to allow for better organization, easier lookup, and unit testing in the future. The structure of the code is more thoroughly explained in the “Code Structure" section.

Refactoring the classes into individual files helped me organize my code better. At this point, I had not written any unit tests yet, but I engaged in manual testing while building out each class. While this was not efficient, it allowed me to do quick tests in the moment while I was building out the logic for the game and connecting each class to one another. This approach also allowed me to debug on the spot while I completed the logic for the remaining project and was particularly useful when working on the RANDOM.ORG API implementation, which I have discussed further in the “Conflict and Resolution” section. Although I initially had large clumps of code in some class methods, I later refactored those methods into smaller ones to allow for better testability.

After finishing my initial version of the game’s code and running the program a few times as a whole, I began writing unit tests for each of the classes and their methods using the pytest testing framework. Here, I tested every method thoroughly and accounted for any edge cases I had noted earlier during implementation. These unit tests also tested class interactions and how the game state variables were affected with every method call. This continuous process of integrating and testing is similar to what I have done for all of my other projects, so much of it felt familiar. While I ran into some issues with testing, I did some research on unit testing and found strategies and tools to resolve these issues. These are also described in the “Conflict and Resolution” section.

After building out the core game functionality and logic and writing unit tests for it, I began extending the game by implementing more features. I approached it from a user’s perspective and thought, “What would I want if I were playing this version of the game?” I implemented features that allowed for smoother gameplay from the controller’s end and provided better UX feedback. This game logic allows the player, as the single-player Code Breaker, to have more control of the game and experience gameplay similar to many modern games. I have described these features more extensively in the “Extensions” section of the README. After writing unit tests for these features, I decided this was a good stopping point for the project. Although I am proud of this project at this stage, I would like to revisit it in the future to extend the game further. I have already considered some suggestions and approaches for these potential implementations, which I have noted in the “Goals and Future Direction” section.

## Code Structure

The project is structured into key classes, where each of them specifically focuses on its role and the logic that drives it. While there may be more components to each class, I chose to only highlight important variables and primary methods here.

### Game:
Key Variables | Description
-----|-----
code_length | sets up the code’s length for the secret_code and the CodeBreaker’s guesses
code_range | sets up the code’s range for the secret_code and the CodeBreaker’s guesses
max_attempt | max attempt for the CodeBreaker to guess
current_game_history | tracks the CodeBreaker’s inputs so far in this game
hint | tracks the revealed hint
prev_match_history | tracks all previous game played

Key Methods | Description
-----|-----
start() | prints rules and initiate the start of the game
reset_game_state() | resets the game state into how it is at the start of the game
run() | runs the entire game multiple times until player is done playing
quitting_game() | sets game states to prepare for quitting
make_move() | a single game move that asks for CodeBreaker guess, CodeMaker analysis, and game’s logic to update game states based on move
response_to_code_breaker_input(user_input) | takes in user input to execute listed commands
reveal_one_hint() | updates hint to reveal one hidden number of the secret_code
is_over() | checks if the game is over based on game state, called after make_move()

### CodeBreaker:
Key Methods | Description
-----|-----
make_guess() | requests user to make an input, returns CodeEntry type

### CodeMaker:
Key Variables | Description
-----|-----
secret_code | the secret code the CodeBreaker is trying to guess

Key Methods | Description
-----|-----
generate_code() | updates secret code with API call or uses fallback in-house sequence generator
use_in_house_random_seq_gen() | the fallback random code sequence generator
get_hint_position_dict() | returns a dictionary for the secret code values and their index position
evaluate_code(guess_code) | this is the CodeMaker’s role to call a comparison between the a guess_code and its secret_code, returns as Feedback

### CodeEntry:
Key Variables | Description
-----|-----
sequence | a string sequence of a CodeEntry object

Key Methods | Description
-----|-----
compare_with(other_code) | compares its sequence to another code’s sequence, returns a Feedback response
is_valid() | validates its sequence to see if it follows length and range rules
to_string() | returns code sequence

### Feedback:
Key Methods | Description
-----|-----
is_perfect_response() | returns True if all parts of Feedback response match code length
to_string() | returns a readable string of Feedback result


## Conflict and Resolution

The main thing I love about programming is that I am constantly learning new concepts and I always look forward to these moments. Although this project was focused on building a game and its logic, I encountered several key concepts along the way that expanded my understanding of software development. These types of problems, and the process of resolving them, are what make me value my future in this field.

One bug I’d like to highlight arose while building the CodeMaker class. I planned to write a method that makes an HTTP GET request to the RANDOM.ORG API. While my initial implementation worked, I soon ran into a familiar problem I had seen in previous projects. To confirm what was happening, I dug deeper. I knew API calls return different status codes, and when mine failed, it consistently returned a 503 error. To be sure, I reviewed the RANDOM.ORG API documentation and confirmed my suspicion: I am getting this error because I had essentially been temporarily IP banned due to rate limits. Their denial-of-service protection had kicked in, making my API calls unreliable.

To address this, I did two things. First, I wrapped the API call in a try block to gracefully handle the error if it occurred. Second, I built an in-house sequence generator that could mimic the API response as a fallback. While this wasn’t part of the original project instructions, I implemented it to ensure reliability. To avoid defaulting to the fallback too quickly, I programmed the try block to reattempt the API request a few times before switching over. To test this, I deliberately altered the API URL to force a 503 response, which confirmed that my fallback generator worked as expected.

During my research, I also discovered the concept of exponential backoff, an error-handling strategy that gradually increases the delay between retry attempts. This gives overloaded servers time to recover and reduces repeated failures. Although I have not yet implemented this for the RANDOM.ORG calls, I plan to research it further and apply it to features that rely heavily on external APIs.

Another issue I faced came during testing. The first challenge was testing methods that required user input. While I could have refactored my code to avoid this, it seemed excessive. After researching, I found that the pytest framework offers a feature called monkeypatch that allows me to mock input responses when necessary. This made it possible to automate tests for user inputs instead of manually entering values into the console every time.

As I moved onto testing more complex class methods, I needed to test interactions across multiple components. Managing several classes in larger test cases quickly became overwhelming and convoluted. This is where my research led me to learn about unittest.MagicMock(). By creating mock objects, I could simulate specific methods of a class without having to initialize or manage all of its dependencies. This approach streamlined my tests, reduced memory usage, and saved time while validating core logic.

While these concepts were new at first, I quickly became familiar with them through practice and use. More importantly, this experience reinforced what I love most about programming: continuous learning. I’m not only grateful to have found solutions to these problems, but also to have gained skills that will be valuable beyond this project.

## Extensions

Feature | Description | Implementation
--------|--------|--------
CodeMaker’s fallback code sequence generation | A fallback to RANDOM.ORG API failing. Ensures that the game can run if or when the API call ever fails. | Implemented using Python’s random standard library to generate a string sequence that follows the current game’s code sequence constraints, similarly to the result of the API call.
CodeBreaker Input: “rules” | States the rules to the player. | Prints out the game rules following the game code’s constraints.
CodeBreaker Input: “help” | Iterates the list of implemented commands to the player. | Prints out a formatted list of commands and what it does to the player.
CodeBreaker input: “hint” | Tells the player one number and its location. | CodeMaker’s stored secret code is stored in a dictionary, where the Game can keep track of and reveal its contents one at a time when called.
CodeBreaker Input: “clear” | Clears the terminal. | Uses os.system to clear shell terminal for cleanliness.
CodeBreaker Input: “reset” | Resets the current game. | Resets the game completely by updating all of the game’s state, including CodeBreaker’s turn and generating a new secret code.
CodeBreaker Input: “quit” | Quits the current game. | Updates the game state to signify that the player wants to quit. This later causes an upstream effect that exits the player’s current game and undo any changes to the game states for this game round.
CodeBreaker Input: “history” | Prints the players move this game. | Formats and prints all of the moves that this CodeBreaker player has made so far in this game.
CodeBreaker Input: “previous [number]” | Recalls a previous match history and result. | Finds a target game that the player has previously played, recalls information about the game, and prints out its formatted result.

## Goals and Future Extensions

As mentioned in the "Conflict and Resolution" section, I plan to research and implement exponential backoff for API calls. Since the game relies heavily on successful API responses, exponential backoff would help improve reliability in cases of repeated failures. Without the fallback sequence generator, the program would fail completely, so this improvement would make the system more robust.

Another planned extension is to add a multiplayer option. The idea is to introduce a Player class that tracks both score and role (CodeMaker or CodeBreaker). After each game, the players’ roles could be switched. The CodeMaker’s and CodeBreaker’s behaviors would remain the same in the game instance, but the reference to which player takes on each role could be updated at the end of a round. This would allow for a two-player version of the game while keeping the existing game logic intact.

I also want to add a game setup menu at the beginning of play. While not strictly necessary, this would give users the ability to customize their game experience and specificity before starting. The game has already been implemented to accommodate to variables such as code length, code range, and maximum attempts, but there is currently no way to access or adjust these values from the controller’s side. Adding a setup menu would make these existing features accessible and could also provide options to choose between different game modes:

- Single player (the current implementation)
- Quick game (a single iteration of the game, already supported)
- Two player mode (to be developed alongside the Player class design)
