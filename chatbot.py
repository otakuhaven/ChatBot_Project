# Importing necessary libraries
import random  # Used for selecting random greetings or responses from predefined lists
from datetime import datetime  # Provides current date and time for time-based greetings
from colorama import Fore, Style  # Adds color and style to text output in the console
import pyjokes  # Library to retrieve random jokes
from textblob import TextBlob  # For sentiment analysis on user input
import pyttsx3  # Library for text-to-speech conversion
import re  # Provides regular expression support for pattern matching

# Memory dictionary to store user-related data (e.g., past interactions, preferences)
memory = {}

# Predefined greetings for different times of day
morning_greetings = [
    "Hope you had a restful sleep.☀️",
    "A brand new day is here.🌸",
    "Let's make today awesome!🌟",
    "How are you feeling today?",
    "Ready to start your day?🌞",
    "Good to see you this morning!🌞",
    "Wakey wakey! It's a beautiful morning.🌞",
    "Rise and shine! Another day to do great things.",
    "What are your plans for today?",
    "The sun's out! Let’s get going!"
]

afternoon_greetings = [
    "How’s your day going so far?",
    "Hope your day has been productive.",
    "Ready to continue your day?",
    "What’s new with you today?",
    "I hope everything is going well.",
    "Got anything exciting planned?",
    "How’s the afternoon treating you?",
    "I hope you're having a great afternoon!",
    "Still going strong this afternoon?",
    "How’s everything going this afternoon?"
]

evening_greetings = [
    "How was your day?",
    "I hope you had a great day.",
    "Time to relax and unwind.",
    "What did you do today?",
    "How can I help you tonight?",
    "What’s on your mind?",
    "The day is winding down, how was it?",
    "I hope you enjoyed your day!",
    "Anything interesting today?",
    "Time to relax! How can I assist you this evening?"
]

# Predefined responses for unrecognized input
unexpected_responses = [
    "Oops, I'm not sure what you mean. Can you try again?",
    "I didn't quite catch that! Can you explain it again?",
    "Hmm, that's a new one! But I'm not sure how to respond to that.",
    "I don't understand that. But I'm still here to chat!",
    "Interesting... but I'm not sure how to reply. Maybe try something else?",
    "I think I need more coffee! I didn't get that.",
    "Sorry, my circuits are a little confused. Can you ask something else?",
    "That's a great question... but I have no idea how to answer it! 😅",
    "Well, that’s outside of my knowledge range. Can we talk about something else?",
    "Uh-oh! I'm stumped. But feel free to ask me anything else!"
]

# Voice initialization for text-to-speech
voice = None
try:
    voice = pyttsx3.init()  # Initialize the text-to-speech engine
    voice.setProperty('rate', 200)  # Set speech rate to 200 words per minute
except Exception as e:
    print(f"{Fore.RED}Warning: Unable to initialize voice. Text-to-speech will not work. {Style.RESET_ALL}")

# Function to convert text to speech
def speak(text):
    if voice:
        voice.say(text)
        voice.runAndWait()
    else:
        print(f"{Fore.RED}Voice not available. {Style.RESET_ALL} {text}")

# Function to get a time-based greeting (morning, afternoon, evening)
def get_time_based_greeting():
    time = datetime.now().hour  # Get the current hour
    if time < 12:
        return "Good Morning!", random.choice(morning_greetings)
    elif time < 18:
        return "Good Afternoon!", random.choice(afternoon_greetings)
    else:
        return "Good Evening!", random.choice(evening_greetings)

# Detect mood based on user's input using sentiment analysis
def detect_mood(user_input):
    try:
        blob = TextBlob(user_input)
        sentiment_score = blob.sentiment.polarity  # Determine the sentiment polarity
        if sentiment_score > 0.2:
            return 'happy'
        elif sentiment_score < -0.2:
            return 'sad'
        else:
            return 'neutral'
    except Exception as e:
        print(f"{Fore.RED}Error in sentiment analysis: {e}{Style.RESET_ALL}")
        return 'neutral'

# Function to tell a joke based on mood
def jokes(mood):
    mood_emoji = {"happy": "😄", "sad": "😞", "neutral": "😐"}  # Mood-based emoji
    try:
        joke = pyjokes.get_joke(category='neutral' if mood == 'happy' else 'chuck' if mood == 'sad' else 'all')
        return f"{mood_emoji[mood]} {joke}"  # Return joke with corresponding emoji
    except Exception as e:
        print(f"{Fore.RED}Error getting joke: {e}{Style.RESET_ALL}")
        return "Sorry, I couldn't find a joke right now."

# Check if user input matches a specific category (creator, joke, name, how are you)
def is_related_to_the_input(user_input, category):
    query_patterns = {
        "creator": r"(who created|who made|creator|creator's name|made you|your creator)",
        "joke": r"(tell me a joke|make me laugh|tell a joke|joke)",
        "name": r"(what's your name|who are you|what is your name)",
        "how are you": r"(how are you|how do you feel|how are you doing)",
        "help": r"(i need help|can you assist me|i need your help|please help|can you help|assist me|help)"
    }
    # Match user input with predefined category patterns
    try:
        if re.search(query_patterns[category], user_input.lower()):
            return True
    except KeyError:
        print(f"{Fore.RED}Error: No pattern found for category: {category}{Style.RESET_ALL}")
    return False


# Function to store information in memory
def store_in_memory(key, value):
    memory[key] = value


# Extra Word Guessing game to make the chatbot more interesting
def play_level(level, word, clues):
    try:
        print(f"{Fore.RED}Welcome to the WORD PUZZLE Game!{Style.RESET_ALL}")
        print(f"{Fore.RED}Level {level}: Solve the puzzle!{Style.RESET_ALL}")

        points = 0
        for i in range(5):
            print(f"{Fore.RED}Clue {i + 1}: {clues[i]}{Style.RESET_ALL}")
            user_input = input("You: ").strip().lower()

            if user_input == word:
                points = [10, 6, 4, 2, 1][i]
                print(f"{Fore.RED}Correct! You got {points} points!{Style.RESET_ALL}")
                return points

        print(f"{Fore.RED}Sorry, The correct word was {word}. You failed this level.{Style.RESET_ALL}")
        return 0
    except Exception as e:
        print(Fore.RED + f"An error occurred in this level: {e}" + Style.RESET_ALL)
        return 0  # Return 0 points in case of an error


def start_word_puzzle():
    # List of puzzles with clues and answers
    try:
        puzzles = [
            {
                "word": "dog",
                "clues": [
                    "The best friend of humans.",
                    "It barks and can be a pet.",
                    "It loves to fetch a ball.",
                    "Common breeds include Labrador, Beagle, and Poodle.",
                    "It has four legs and a tail."
                ]
            },
            {
                "word": "ball",
                "clues": [
                    "Used in many sports like football, basketball, and tennis.",
                    "It’s round and often made of rubber or leather.",
                    "Children play with it in the park.",
                    "You kick it in soccer and throw it in basketball.",
                    "It bounces when you drop it."
                ]
            },
            {
                "word": "bicycle",
                "clues": [
                    "I am a mode of transportation.",
                    "I have two wheels.",
                    "I don't require gasoline.",
                    "I am powered by pedaling.",
                    "You often see me in parks or on roads."
                ]
            },
            {
                "word": "computer",
                "clues": [
                    "I process information.",
                    "I can be a desktop or laptop.",
                    "I can run various software applications.",
                    "I am used to browse the internet.",
                    "I have a keyboard and screen."
                ]
            },
            {
                "word": "guitar",
                "clues": [
                    "I am a musical instrument.",
                    "I have six strings.",
                    "I can be electric or acoustic.",
                    "I am played by strumming or plucking.",
                    "I am popular in rock and roll."
                ]
            }
        ]

        total_score = 0
        level = 1

        while level <= len(puzzles):
            try:
                puzzle = puzzles[level - 1]  # Get the puzzle for the current level
                word = puzzle["word"]
                clues = puzzle["clues"]

                points = play_level(level, word, clues)
                total_score += points

                # Check if the user wants to quit after each level
                print(Fore.RED + f"Your total score so far: {total_score}" + Style.RESET_ALL)
                quit_game = ""

                # Loop until valid input is given
                while quit_game not in ["yes", "no"]:
                    quit_game = input(
                        Fore.RED + "Chatbot: Do you want to quit the game? (Yes/No) " + Style.RESET_ALL).strip().lower()

                    if quit_game not in ["yes", "no"]:
                        print(Fore.RED + "Invalid input. Please enter 'Yes' or 'No'." + Style.RESET_ALL)

                if quit_game == 'yes':
                    print(Fore.RED + "You chose to quit the game. Your progress will not be saved." + Style.RESET_ALL)
                    break  # Exit the game if the user chooses to quit

                level += 1  # Only increment the level if the user chooses 'no'

            except IndexError:
                print(Fore.RED + "No more puzzles available for this level. Game over!" + Style.RESET_ALL)
                break  # End the game if no puzzles are available

        print(Fore.RED + f"The game is over! Your final score is {total_score} points." + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + "\nYou exited the game unexpectedly. Your progress will not be saved." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)


# Main function to integrate with chatbot
def main():
    try:
        print("Chatbot: Hi! Let's play a word puzzle game.")
        start_word_puzzle()
    except Exception as e:
        print(Fore.RED + f"Chatbot: An error occurred in the main game: {e}" + Style.RESET_ALL)


# Chatbot core: The central hub of the program that interacts with users
if __name__ == "__main__":
    # Initialize use_voice variable with a default value (False) before asking for user input
    use_voice = False  # Default to text-only if no valid input is given

    # Ask the user if they want voice responses
    print(
        Fore.RED + "Chatbot: Hi! I'm your virtual assistant. Would you like me to respond with voice as well as text?(yes/no) " + Style.RESET_ALL)
    user_choice = input("You: ").strip().lower()

    # Loop until a valid response is received
    while user_choice not in ['yes', 'y', 'no', 'n']:
        print(f"{Fore.RED}Chatbot: Please enter a valid input (yes/no).{Style.RESET_ALL}")
        user_choice = input("You: ").strip().lower()

    # Set user's preference for text-to-speech responses based on valid input
    if user_choice in ['yes', 'y']:
        use_voice = True  # Enable voice responses
        print(f"{Fore.RED}Chatbot: I'll respond with both text and voice.{Style.RESET_ALL}")
        speak("I'll respond with both text and voice.")
    elif user_choice in ['no', 'n']:
        use_voice = False  # Disable voice responses
        print(f"{Fore.RED}ChatBot: I'll respond with text only.")

    # Main interaction loop that runs until the user decides to exit
    while True:
        user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip().lower()  # Get user input

        # Handle greetings
        if user_input in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]:
            time_greeting, random_greeting = get_time_based_greeting()  # Generate time-based greeting
            print(f"{Fore.RED}Chatbot: {time_greeting} {random_greeting}{Style.RESET_ALL}")
            if use_voice:
                speak(f"{time_greeting} {random_greeting}")

        # Handle "How are you?" inputs
        elif is_related_to_the_input(user_input, "how are you"):
            response = "I'm just a digital creation, but I'm here to help you!"
            print(f"{Fore.RED}Chatbot: {response}{Style.RESET_ALL}")
            if use_voice:
                speak(response)

        # Handle queries related to the chatbot's name
        elif is_related_to_the_input(user_input, "name"):
            response = "I don't have a specific name, but you can call me whatever you'd like."
            print(f"{Fore.RED}Chatbot: {response}{Style.RESET_ALL}")
            if use_voice:
                speak(response)

        # Handle queries related to the creator
        elif is_related_to_the_input(user_input, "creator"):
            if "creator_info" in memory:
                response = memory["creator_info"]  # Fetch data from memory
            else:
                response = "I was created by Otaku Haven."
                store_in_memory("creator_info", response)  # Store information in memory
            print(f"{Fore.RED}Chatbot: {response}{Style.RESET_ALL}")
            if use_voice:
                speak(response)

        # Handle joke queries
        elif is_related_to_the_input(user_input, "joke"):
            mood = detect_mood(user_input)  # Detect mood from user input
            response = jokes(mood)  # Get a joke based on the mood
            print(f"{Fore.RED}Chatbot: {response}{Style.RESET_ALL}")
            if use_voice:
                speak(response)

            # Ask user for more jokes
            while True:
                ask_user = input(f"{Fore.RED}Do you want to hear another joke (Yes/No)? {Style.RESET_ALL}").lower()
                if ask_user == "yes":
                    response = jokes(mood)
                    print(f"{Fore.RED}Chatbot: {response}{Style.RESET_ALL}")
                    if use_voice:
                        speak(response)
                else:
                    print(f"{Fore.RED}Chatbot: Alright! Let me know if you need anything else.{Style.RESET_ALL}")
                    if use_voice:
                        speak("Alright! Let me know if you need anything else.")
                    break

        elif user_input == "play game":
            start_word_puzzle()

        # Handle help/assistance requests
        elif is_related_to_the_input(user_input, "help"):
            response = "I will try to help you with my knowledge. What do you need assistance with?"
            print(f"{Fore.RED}Chatbot: {response}{Style.RESET_ALL}")
            if use_voice:
                speak(response)

        # Handle exit commands
        elif user_input in ["exit", "quit", "bye"]:
            # Ask for feedback before exiting
            feedback = input(
                f"{Fore.RED}Chatbot: Before you go, I would love your feedback! How was your experience? {Style.RESET_ALL}")

            # Store or display the feedback (You can write it to a file if desired)
            print(
                f"{Fore.RED}Chatbot: Thank you for your feedback! We appreciate it. Have a great day!{Style.RESET_ALL}")
            print(f"{Fore.RED}Chatbot: Your feedback: {feedback}{Style.RESET_ALL}")  # Display feedback (optional)

            if use_voice:
                speak("Thank you for your feedback! Have a great day!")

            break  # Exit the chatbot loop

        # Handle unrecognized commands
        else:
            response = random.choice(unexpected_responses)
            print(f"{Fore.RED}Chatbot: {response}{Style.RESET_ALL}")
            if use_voice:
                speak(response)



