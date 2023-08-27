import pygame
import random
import nltk
import tkinter as tk
from tkinter import messagebox

# Download the NLTK words dataset (only need to do this once)
nltk.download('words')

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# Load the English words dataset from NLTK
word_list = nltk.corpus.words.words()


class HangmanGame:
    def __init__(self):
        self.word = random.choice(word_list).lower()  # Choose a random word from the dataset
        self.guessed_letters = set()
        self.remaining_attempts = 6
        self.correct_letters = set()

    def guess_letter(self, letter):
        if letter not in self.guessed_letters:
            self.guessed_letters.add(letter)
            if letter in self.word:
                self.correct_letters.add(letter)
            else:
                self.remaining_attempts -= 1

    def game_over(self):
        return self.remaining_attempts == 0 or all(letter in self.correct_letters for letter in self.word)

    def reset(self):
        self.word = random.choice(word_list).lower()
        self.guessed_letters = set()
        self.remaining_attempts = 6
        self.correct_letters = set()

    def draw(self, screen):
        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw hangman stages
        base_y = 450
        if self.remaining_attempts < 6:
            pygame.draw.line(screen, (0, 0, 0), (150, (base_y-100)), (350, (base_y-100)), 5)  # Base
        if self.remaining_attempts < 5:
            pygame.draw.line(screen, (0, 0, 0), (250, (base_y-100)), (250, 50), 5)  # Pole
        if self.remaining_attempts < 4:
            pygame.draw.line(screen, (0, 0, 0), (250, 70), (450, 70), 5)  # Beam
        if self.remaining_attempts < 3:
            pygame.draw.circle(screen, (0, 0, 0), (450, 95), 30, 5)  # Head
        if self.remaining_attempts < 2:
            pygame.draw.line(screen, (0, 0, 0), ((250+200), (210-90)), ((250+200), (320-90)), 5)  # Body
        if self.remaining_attempts < 1:
            pygame.draw.line(screen, (0, 0, 0), ((250+200), (260-90)), ((220+200), (330-90)), 5)  # Left arm
            pygame.draw.line(screen, (0, 0, 0), ((250+200), (260-90)), ((280+200), (330-90)), 5)  # Right arm
            pygame.draw.line(screen, (0, 0, 0), ((250+200), (320-90)), ((220+200), (390-90)), 5)  # Left leg
            pygame.draw.line(screen, (0, 0, 0), ((250+200), (320-90)), ((280+200), (390-90)), 5)  # Right leg

        # Draw guessed letters
        for i, letter in enumerate(ALPHABET):
            x = 50 + i * 30
            y = 500
            if letter in self.guessed_letters:
                color = (0, 0, 0)
            else:
                color = (200, 200, 200)
            font = pygame.font.Font(None, 36)
            letter_text = font.render(letter, True, color)
            screen.blit(letter_text, (x, y))

        # Draw word display
        font = pygame.font.Font(None, 48)
        displayed_word = " ".join([letter if letter in self.correct_letters else "_" for letter in self.word])
        word_text = font.render(displayed_word, True, (0, 0, 0))
        screen.blit(word_text, (200, 400))


# Initialize the game and the screen
game = HangmanGame()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman Game PRO")

# Define button dimensions
button_width = 200
button_height = 60
button_margin = 20

# Button coordinates
play_again_button_rect = pygame.Rect(SCREEN_WIDTH //
                                     2 - button_width //
                                     2, SCREEN_HEIGHT //
                                     2 + button_margin,
                                     button_width,
                                     button_height)
exit_button_rect = pygame.Rect(SCREEN_WIDTH //
                               2 - button_width //
                               2, play_again_button_rect.bottom +
                               button_margin,
                               button_width,
                               button_height)

# Button colors
button_color = (200, 200, 200)
button_hover_color = (150, 150, 150)

# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
result_printed = False  # To keep track of whether the result has been printed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.unicode in ALPHABET:
                game.guess_letter(event.unicode)
            elif game_over and (event.unicode.lower() == 'r' or event.unicode.lower() == 'q'):
                if event.unicode.lower() == 'r':
                    game.reset()
                    game_over = False
                    result_printed = False  # Reset the result printing flag
                else:
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and play_again_button_rect.collidepoint(event.pos):
                game.reset()
                game_over = False
                result_printed = False  # Reset the result printing flag
            elif game_over and exit_button_rect.collidepoint(event.pos):
                running = False

    screen.fill((255, 255, 255))

    if not game_over:
        game.draw(screen)
    else:
        font = pygame.font.Font(None, 72)
        game_over_text = "You won!" if all(letter in game.correct_letters for letter in game.word) else "You lost!"

        if game_over_text == "You lost!":
            game_over_color = (255, 0, 0)  # Red color for "You lost!"
        else:
            game_over_color = (0, 255, 0)  # Green color for "You won!"

        game_over_message = font.render(game_over_text, True, game_over_color)
        screen.blit(game_over_message, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 50))

        pygame.draw.rect(screen, button_color, play_again_button_rect)
        pygame.draw.rect(screen, button_color, exit_button_rect)

        mouse_pos = pygame.mouse.get_pos()
        play_again_hovered = play_again_button_rect.collidepoint(mouse_pos)
        exit_hovered = exit_button_rect.collidepoint(mouse_pos)

        if play_again_hovered:
            pygame.draw.rect(screen, button_hover_color, play_again_button_rect)
        if exit_hovered:
            pygame.draw.rect(screen, button_hover_color, exit_button_rect)

        font = pygame.font.Font(None, 36)
        play_again_text = font.render("PLAY AGAIN (R)", True, (0, 0, 0))
        exit_text = font.render("EXIT (Q)", True, (0, 0, 0))
        screen.blit(play_again_text, (play_again_button_rect.centerx - play_again_text.get_width() //
                                      2, play_again_button_rect.centery - play_again_text.get_height() //
                                      2))
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() //
                                2, exit_button_rect.centery - exit_text.get_height() //
                                2))

        # Print the correct answer if not printed yet
        if game_over_text == "You lost!" and not result_printed:
            correct_answer = "Correct answer: " + game.word
            print(correct_answer)
            result_printed = True  # Set the result printing flag

            # Show a messagebox with the correct answer
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showinfo("Game Over", correct_answer)

    pygame.display.flip()

    if game.game_over():
        game_over = True

    clock.tick(30)

pygame.quit()
