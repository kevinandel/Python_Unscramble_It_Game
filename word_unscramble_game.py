import random
import csv
import os

# Function to check if the player exists in the leaderboard
def check_player(name, Class):
    if not os.path.exists('leaderboard.csv'):
        print("Leaderboard file not found. Starting fresh.")
        return 'no', 0

    with open('leaderboard.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for index, row in enumerate(reader, start=1):
            if row and name == row[0] and Class == row[1]:
                print(f"{row[0]} {row[1]}\nIs it you?")
                if input('Enter response Yes/No: ').strip().lower() == 'yes':
                    print(f'Welcome back, {name}!')
                    return 'yes', index
        print("Welcome to the Word Unscramble Game!")
        return 'no', 0

# Function to update or append player score and level to the leaderboard
def update_leaderboard(response, name, Class, score, level, index):
    if not os.path.exists('leaderboard.csv'):
        print("Leaderboard file not found.")
        return

    if response == 'yes':
        with open('leaderboard.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            records = list(reader)

        # Update score and level if the new score is higher
        if int(records[index - 1][2]) < score:
            print('You updated your score!')
            records[index - 1][2] = str(score)
            records[index - 1][3] = level
        else:
            print("You didn't beat your previous score.")

        with open('leaderboard.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(records)
    else:
        with open('leaderboard.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, Class, score, level])

# Function to select and jumble a random word from a level
def choose_word(level, used_indices):
    if len(used_indices) >= len(level):
        return None, None

    while True:
        index = random.randrange(len(level))
        if index not in used_indices:
            used_indices.append(index)
            word_parts = level[index].split('-')
            if len(word_parts) < 2:
                continue
            word = word_parts[0].strip().upper()
            jumbled = ''.join(random.sample(word, len(word)))
            return word_parts, jumbled

# Function to check the player's answer
def check_answer(answer, correct_word, life, score, points, remaining_words):
    if answer.upper() == correct_word.upper():
        print('Correct Answer!')
        return life, score + points, remaining_words - 1
    else:
        print(f'Wrong Answer! The correct answer is {correct_word}. You lost one life.')
        return life - 1, score, remaining_words

# Main game loop
def play_game():
    score = 0
    name = input('Enter your name: ').strip().upper()
    Class = input('Enter your class: ').strip().upper()
    response, index = check_player(name, Class)

    # Load words from files
    try:
        with open('easy.txt', 'r') as f:
            easy = f.readlines()
        with open('medium.txt', 'r') as f:
            medium = f.readlines()
        with open('hard.txt', 'r') as f:
            hard = f.readlines()
    except FileNotFoundError:
        print("One or more word files are missing.")
        return

    life, skips = 3, 3
    easy_indices, medium_indices, hard_indices = [], [], []
    remaining_words = 35
    level = "Easy"

    print('You have 35 questions from 3 levels: 20 easy, 10 medium, and 5 hard.')
    print('You start at the easy level with 3 lives and 3 skips.')

    while life > 0 and remaining_words > 0:
        if score < 200:
            word_data, jumbled = choose_word(easy, easy_indices)
            points = 10
            level = "Easy"
        elif 200 <= score < 500:
            word_data, jumbled = choose_word(medium, medium_indices)
            points = 30
            level = "Medium"
        else:
            word_data, jumbled = choose_word(hard, hard_indices)
            points = 100
            level = "Hard"

        if not word_data:
            print("No more words in this level. Level completed.")
            break

        print(f'Jumbled word: {jumbled}\nMeaning: {word_data[1].strip()}')
        print(f'Life: {life}, Skips: {skips}, Words left: {remaining_words}')
        answer = input('Enter the unscrambled word (or "skip"/"quit"): ').strip().lower()

        if answer == 'skip':
            if skips > 0:
                skips -= 1
                print(f'Skipped! Skips left: {skips}. Correct answer: {word_data[0].strip().upper()}')
                continue
            else:
                print('No skips left.')
        elif answer == 'quit':
            print(f'You quit. Correct answer: {word_data[0].strip().upper()}')
            break

        life, score, remaining_words = check_answer(answer, word_data[0].strip(), life, score, points, remaining_words)

        # Check level completion and provide options
        if score == 200:
            print('Congratulations! You completed the Easy level! 🎉')
            update_leaderboard(response, name, Class, score, level, index)
            while True:
                choice = input('Do you want to continue to the Medium level, view the leaderboard, or quit? (medium/leaderboard/quit): ').strip().lower()
                if choice == 'medium':
                    break
                elif choice == 'leaderboard':
                    show_leaderboard()
                elif choice == 'quit':
                    return
                else:
                    print("Invalid choice. Please try again.")

        if score == 500:
            print('Congratulations! You completed the Medium level! 🎉')
            update_leaderboard(response, name, Class, score, level, index)
            while True:
                choice = input('Do you want to continue to the Hard level, view the leaderboard, or quit? (hard/leaderboard/quit): ').strip().lower()
                if choice == 'hard':
                    break
                elif choice == 'leaderboard':
                    show_leaderboard()
                elif choice == 'quit':
                    return
                else:
                    print("Invalid choice. Please try again.")

    # Final congratulations message if the player completes the Hard level
    if score >= 500 and remaining_words == 0:
        print('Congratulations! You have completed all levels of the game! 🏆🎉')

    update_leaderboard(response, name, Class, score, level, index)

# Function to display the leaderboard
def show_leaderboard():
    if not os.path.exists('leaderboard.csv'):
        print("Leaderboard is empty.")
        return

    with open('leaderboard.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        records = [row for row in reader if row]
        records.sort(key=lambda x: int(x[2]), reverse=True)

    if records:
        print(f'{header[0]:<10} {header[1]:<6} {header[2]:<6} {header[3]:<6}')
        for record in records:
            print(f'{record[0]:<10} {record[1]:<6} {record[2]:<6} {record[3]:<6}')
    else:
        print("Leaderboard is empty.")

# Function to display the introduction
def show_intro():
    try:
        with open('introduction.txt', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Introduction file not found.")

# Main menu
def main_menu():
    while True:
        print('unscramble')
        print('1. Introduction')
        print('2. Play')
        print('3. Leaderboard')
        print('4. Exit')
        choice = input('Enter your choice (1-4): ').strip()

        if choice == '1':
            show_intro()
        elif choice == '2':
            play_game()
        elif choice == '3':
            show_leaderboard()
        elif choice == '4':
            print('Goodbye!')
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Start the game
main_menu()