import random

def generate_target():
    """Generate a 4-digit number with all different digits"""
    digits = list(range(10))
    random.shuffle(digits)
    target = digits[:4]
    return target

def get_user_guess():
    """Get a valid 4-digit guess from the user"""
    while True:
        guess_str = input("Enter your 4-digit guess (digits must not repeat): ")
        if len(guess_str) != 4 or not guess_str.isdigit():
            print("❌ Invalid input! Please enter exactly 4 digits.")
            continue
        guess = [int(x) for x in guess_str]
        if len(set(guess)) != 4:
            print("❌ Digits must be unique! Try again.")
            continue
        return guess

def check_guess(target, guess):
    """Compare guess with target and return (A, B)"""
    A = 0  # Bulls
    B = 0  # Cows
    for i in range(4):
        if guess[i] == target[i]:
            A += 1
        elif guess[i] in target:
            B += 1
    return A, B

def main():
    print("🎯 Welcome to the 1A2B (Bulls & Cows) Game!")
    target = generate_target()
    attempts = 0
    
    while True:
        guess = get_user_guess()
        attempts += 1
        A, B = check_guess(target, guess)
        print(f"Result: {A}A{B}B")
        if A == 4:
            print(f"🏆 Congratulations! You guessed the number in {attempts} attempts!")
            print("The number was:", "".join(map(str, target)))
            break

# Start the game
if __name__ == "__main__":
    main()
