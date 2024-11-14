import json
import os
import random
import bcrypt

# Function to hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to check a password against a hashed password
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Function to load the leaderboard from a JSON file
def load_leaderboard(filename='leaderboard.json'):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file is missing, not properly formatted, or empty, return an empty dictionary
        return {}

# Function to save the leaderboard to a JSON file
def save_leaderboard(leaderboard, filename='leaderboard.json'):
    with open(filename, 'w') as f:
        json.dump(leaderboard, f, indent=4)

# Function to update the leaderboard with a player's score
def update_leaderboard(leaderboard, name, miles_traveled):
    # Only update the leaderboard if the new score is higher than the current score
    if name in leaderboard and miles_traveled > leaderboard[name]:
        leaderboard[name] = miles_traveled
        save_leaderboard(leaderboard)
    elif name not in leaderboard:
        leaderboard[name] = miles_traveled
        save_leaderboard(leaderboard)

# Function to display the leaderboard
def display_leaderboard(leaderboard):
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    print("Leaderboard:")
    for i, (player, miles_traveled) in enumerate(sorted_leaderboard, start=1):
        print(f"{i}. {player}: {miles_traveled}")

# Function to initialize the leaderboard file
def initialize_leaderboard(filename='leaderboard.json'):
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)


# Function to create a new user account
def create_user():
    users = {}
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file is missing or not properly formatted, create an empty dictionary
        pass

    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    if username in users:
        print("Username already exists.")
    else:
        hashed_password = hash_password(password)
        users[username] = {'password': hashed_password.decode('utf-8'), 'scores': []}
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        print("Account created successfully.")
        return username

    return None

# Function to handle user login
def login():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users found.")
        return None

    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    if username in users and check_password(users[username]['password'].encode('utf-8'), password):
        print("Login successful.")
        return username
    else:
        print("Invalid username or password.")
        return None

# Function to save score to user's account
def save_score_to_user(username, score):
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users found.")
        return

    if username in users:
        users[username]['scores'].append(score)
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        print("Score saved successfully.")
    else:
        print("User not found.")

# Initialize the leaderboard file
initialize_leaderboard()

# Game variables
miles_traveled = 0
water_drank = 0
energy = 100
aliens_distance = -20
water_left = 5
thirst = 0
turn = 0
temperature = 65
name = None
done = True
has_printed = False

# Game loop
while done:        
    # Login or create a new account
    if name is None:
        print("1. Login")
        print("2. Create Account")
        print("V to View Leaderboard:")
        print("Q to quit")
        print("")
        choice = input("Choose an option: ")
        if choice == '1':
            name = login()
        elif choice == '2':
            name = create_user()
        elif choice == 'v' or choice == 'V':
            leaderboard = load_leaderboard()
            display_leaderboard(leaderboard)
            print("")
        elif choice == 'q' or choice == 'Q':
            break
        else:
            print("Invalid choice.")
        continue

    # Game logic here
    if temperature > 85:
        print("it is gettin hot in here")
    if temperature < 40:
        print("brrrr its cold")
    if temperature > 100:
        print("GAME OVER")
        print("you passed out")
        print("")
        print("stats:")
        print("distance traveled:", miles_traveled, "kilometers")
        print("water drank:", water_drank)
        print("water left:", water_left)
        print("aliens distance:", aliens_distance, "kilometers")
        print("energy left:", energy)
        print("thirst:", thirst)
        print("turns survived:", turn)
        print("temperature:", temperature, "degrees fahrenheit")
        print("")
        done = False
        leaderboard = load_leaderboard()  # Load the leaderboard
        update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
        display_leaderboard(leaderboard)  # Display the leaderboard
        save_score_to_user(name, miles_traveled)  # Save score to user's account
        break
    if temperature < 30:
        print("GAME OVER")
        print("you froze")
        print("")
        print("stats:")
        print("distance traveled:", miles_traveled, "kilometers")
        print("water drank:", water_drank)
        print("water left:", water_left)
        print("aliens distance:", aliens_distance, "kilometers")
        print("energy left:", energy)
        print("thirst:", thirst)
        print("turns survived:", turn)
        print("temperature:", temperature, "degrees fahrenheit")
        print("")
        done = False
        leaderboard = load_leaderboard()  # Load the leaderboard
        update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
        display_leaderboard(leaderboard)  # Display the leaderboard
        save_score_to_user(name, miles_traveled)  # Save score to user's account
        break
    if energy < 0:
        energy = 0
    if water_left < 2:
        print("you are running low on water")
    if energy < 50:
        print("your getting very sleepy")
    if aliens_distance > -20:
        print("their getting closer")
        print("👽")
        print("")
    if thirst < 0:
        thirst = 0
    if energy < 1:
        print("")
        print("GAME OVER")
        print("you got too tired and fell asleep, they got you")
        print("")
        print("stats:")
        print("distance traveled:", miles_traveled, "kilometers")
        print("water drank:", water_drank)
        print("water left:", water_left)
        print("aliens distance:", aliens_distance, "kilometers")
        print("energy left:", energy)
        print("thirst:", thirst)
        print("turns survived:", turn)
        print("temperature:", temperature, "degrees fahrenheit")
        print("")
        done = False
        leaderboard = load_leaderboard()  # Load the leaderboard
        update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
        display_leaderboard(leaderboard)  # Display the leaderboard
        save_score_to_user(name, miles_traveled)  # Save score to user's account
        break
    if energy > 100:
        energy = 100
    if aliens_distance > -1:
        print("")
        print("GAME OVER")
        print("they caught up to you")
        print("")
        print("stats:")
        print("distance traveled:", miles_traveled, "kilometers")
        print("water drank:", water_drank)
        print("water left:", water_left)
        print("aliens distance:", aliens_distance, "kilometers")
        print("energy left:", energy)
        print("thirst:", thirst)
        print("turns survived:", turn)
        print("temperature:", temperature, "degrees fahrenheit")
        print("")
        done = False
        leaderboard = load_leaderboard()  # Load the leaderboard
        update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
        display_leaderboard(leaderboard)  # Display the leaderboard
        save_score_to_user(name, miles_traveled)  # Save score to user's account
        break
    if thirst > 2:
        print("your getting thirsty")
    if thirst > 6:
        print("")
        print("GAME OVER")
        print("you got too thirsty")
        print("")
        print("stats:")
        print("distance traveled:", miles_traveled, "kilometers")
        print("water drank:", water_drank)
        print("water left:", water_left)
        print("aliens distance:", aliens_distance, "kilometers")
        print("energy left:", energy)
        print("thirst:", thirst)
        print("turns survived:", turn)
        print("temperature:", temperature, "degrees fahrenheit")
        print("")
        done = False
        leaderboard = load_leaderboard()  # Load the leaderboard
        update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
        display_leaderboard(leaderboard)  # Display the leaderboard
        save_score_to_user(name, miles_traveled)  # Save score to user's account
        break
    if water_left < 1:
        print("you ran out of water")
    if done is True:
        print("W. drink water")
        print("S. speed up")
        print("L. LUDICROUS SPEED")
        print("R. rest")
        print("C. check user status")
        print("Q. quit")
        print("V. view leaderboard")
        print("G. gather water")
        print("F. cool down")
        print("H. heat up")
        print("I. show control")
        print("")
        choice = input("What will you do: ")
        if choice == 'i' or choice == 'I':
            print("")
            print("W. drink water")
            print("S. speed up")
            print("L. LUDICROUS SPEED")
            print("R. rest")
            print("C. check user status")
            print("Q. quit")
            print("V. view leaderboard")
            print("G. gather water")
            print("F. cool down")
            print("H. heat up")
            print("I. show control")
            print("")
        if choice == 'Q' or choice == 'q':
            end = input("Are you sure you want to quit? (y/n): ")
            if end == 'y':
                print("Thanks for playing!")
                print("")
                print("stats:")
                print("distance traveled:", miles_traveled, "kilometers")
                print("water drank:", water_drank)
                print("water left:", water_left)
                print("aliens distance:", aliens_distance, "kilometers")
                print("energy left:", energy)
                print("thirst:", thirst)
                print("turns survived:", turn)
                print("temperature:", temperature, "degrees fahrenheit")
                print("")
                print("")
                leaderboard = load_leaderboard()  # Load the leaderboard
                update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
                display_leaderboard(leaderboard)  # Display the leaderboard
                done = False
                break
            elif end == 'n':
                print("")
                print("OK")
            else:
                print("Invalid, you are going to keep going anyways")
            print("")
        elif choice == 'F' or choice == 'f':
            print("cooling down")
            print("")
            temperature -= 15
        elif choice == 'H' or choice == 'h':
            print("heating up")
            print("")
            temperature += 15
        elif choice == 'C' or choice == 'c':
            ahhh = random.randint(10, 230)
            aliens_distance += ahhh
            temperature += 2
            print("")
            turn += 1
            print("distance traveled:", miles_traveled, "kilometers")
            print("water drank:", water_drank)
            print("water left:", water_left)
            print("aliens distance:", aliens_distance, "kilometers")
            print("energy left:", energy)
            print("thirst:", thirst)
            print("temperature:", temperature, "degrees fahrenheit")
            print("turns survived:", turn)
            print("")
        elif choice == 'R' or choice == 'r':
            energy += 100
            turn += 1
            temperature = 65
            print("you feel well rested")
            distance = random.randint(20, 40)
            aliens_distance += distance
            print("")
        elif choice == 'S' or choice == 's':
            speed = random.randint(10, 25)
            turn += 1
            temperature += 5
            tired = random.randint(5, 20)
            aliens = random.randint(10, 20)
            miles_traveled += speed
            energy -= tired
            aliens_distance -= aliens
            thirst += 1
            print("your zooming at:", speed, "km/h")
            print("")
        elif choice == 'G' or choice == 'g':
            turn += 1
            temperature += 20
            water_left = 5
            energy -= 50
            alien = random.randint(40, 65)
            aliens_distance -= alien
            print("")
            print("gathering water")
        elif choice == 'W' or choice == 'w':
            turn += 1
            temperature -= 10
            print("")
            if water_left > 0:
                print("you drank water...")
                print("mmmm")
                print("")
                water_drank += 1
                water_left -= 1
                aliens = random.randint(20, 35)
                aliens_distance += aliens
                drink = random.randint(1, 5)
                thirst -= drink
        elif choice == 'L' or choice == 'l':
            turn += 1
            temperature += 10
            print("now entering LUDICROUS SPEED")
            speed = random.randint(15, 30)
            tired = random.randint(10, 30)
            aliens = random.randint(15, 30)
            miles_traveled += speed
            energy -= tired
            aliens_distance -= aliens
            thirst += 2
            print("your zooming at:", speed, "km/h")
            print("")
        elif choice == 'V' or choice == 'v':
            print("")
            leaderboard = load_leaderboard()  # Load the leaderboard
            update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
            display_leaderboard(leaderboard)  # Display the leaderboard
    # ... (game logic code)

    if miles_traveled in range(100, 130) and not has_printed:
        has_printed = True
        print("")
        print("CONGRATULATIONS")
        print("")
        print("you escaped alive...")
        print("this time")
        complete = str(input("would you like to keep going? (y/n):"))
        if complete == 'n' or complete == 'N':
            print("")
            print("bye bye")
            print("")
            print("stats:")
            print("distance traveled:", miles_traveled, "kilometers")
            print("water drank:", water_drank)
            print("water left:", water_left)
            print("aliens distance:", aliens_distance, "kilometers")
            print("energy left:", energy)
            print("thirst:", thirst)
            print("turns survived:", turn)
            print("temperature:", temperature, "degrees fahrenheit")
            print("")
            leaderboard = load_leaderboard()  # Load the leaderboard
            update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
            display_leaderboard(leaderboard)  # Display the leaderboard
            done = False
        if complete == 'y' or complete == 'Y':
            print("")
            done = True
        else:
            print("invalid, you are going to keep going anyways")
    if miles_traveled in range(10000, 10050) and not has_printed:
        has_printed = True
        print("")
        print("wow...")
        print("")
        print("i did not think this was possible...")
        print("...")
        print("but here we are")
        print("")
        print("congratulations")
        print("")
        print("you reached 10000 kilometers")
        print("")
        print("feel free to keep going or end here and see your stats")
        print("")
        long_end = str(input("would you like to keep going? (y/n):"))
        if long_end == 'y' or long_end == 'Y':
            print("see how much farther you can go")
            print("")
            done = True
        elif long_end == 'n' or long_end == 'N':
            print("")
            print("ok")
            print("")
            print("stats:")
            print("distance traveled:", miles_traveled, "kilometers")
            print("water drank:", water_drank)
            print("water left:", water_left)
            print("aliens distance:", aliens_distance, "kilometers")
            print("energy left:", energy)
            print("thirst:", thirst)
            print("turns survived:", turn)
            print("temperature:", temperature, "degrees fahrenheit")
            print("")
            leaderboard = load_leaderboard()  # Load the leaderboard
            update_leaderboard(leaderboard, name, miles_traveled)  # Update the leaderboard
            display_leaderboard(leaderboard)  # Display the leaderboard     
            done = False