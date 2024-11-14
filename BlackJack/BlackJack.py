import tkinter as tk
import random
import os
from tkinter import messagebox 
from PIL import Image, ImageTk

CARD_IMAGE_PATH = './cards/'
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', "Clubs", "Spades"]
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

class whiteJackGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("whitejack")
        self.geometry("800x600")
        self.configure(bg="#2e3b4e")

        # Game variables
        self.deck = self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.game_over = False

        # Display elements
        # Player
        self.player_score_label = tk.Label(self, text="Your score: 0", font=("Arial", 16), bg="#2e3b4e", fg="white")
        self.player_score_label.pack(pady=5)
        self.player_label = tk.Label(self, text="Your cards: ", font=("Arial", 16), bg="#2e3b4e", fg="white")
        self.player_label.pack(pady=10)
        self.player_frame = tk.Frame(self, bg="#2e3b4e")
        self.player_frame.pack(pady=10)
        
        # Dealer
        self.dealer_frame = tk.Frame(self, bg="#2e3b4e")
        self.dealer_frame.pack(pady=10)
        self.dealer_label = tk.Label(self, text="Dealer's cards: ", font=("Arial", 16), bg="#2e3b4e", fg="white")
        self.dealer_label.pack(pady=10)
        self.dealer_score_label = tk.Label(self, text="Dealer's score: 0", font=("Arial", 16), bg="#2e3b4e", fg="white")
        self.dealer_score_label.pack(pady=5)
        
        # Actions
        self.hit_button = tk.Button(self, text="Hit", command=self.player_hit, bg="#4caf50", fg="white", font=("Arial", 13), padx=20, pady=10)
        self.hit_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.stand_button = tk.Button(self, text="Stand", command=self.player_stand, bg="#4caf50", fg="white", font=("Arial", 13), padx=20, pady=10)
        self.stand_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.restart_button = tk.Button(self, text="Restart", command=self.restart_game, bg="#4caf50", fg="white", font=("Arial", 13), padx=20, pady=10)
        self.restart_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.card_images = {}
        self.start_game()

    def shuffle_deck(self):
        deck = [(value, suit) for value in VALUES for suit in SUITS]
        random.shuffle(deck)
        return deck

    def player_hit(self):
        print("Player chooses to take a card")
        if not self.game_over:
            self.player_hand.append(self.deck.pop())
            self.update_ui()
            
            # Calcula y muestra la probabilidad de pasarse
            bust_probability = self.calculate_bust_probability()
            messagebox.showinfo("Probability", f"Probability of busting if you take another card: {bust_probability:.2%}")
            
            if self.player_score > 21:
                self.end_game("You busted! Dealer wins.")

    def player_stand(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.dealer_draw_card()

    def dealer_draw_card(self):
        print("Dealer draws one card.")
        if not self.deck:
            self.deck = self.shuffle_deck()
        self.dealer_hand.append(self.deck.pop())
        self.update_ui()
        
        # Determine the winner
        self.dealer_score = self.calculate_score(self.dealer_hand)
        self.determine_winner()

    def determine_winner(self):
        if self.player_score > self.dealer_score:
            self.end_game("You win!")
        elif self.player_score < self.dealer_score:
            self.end_game("Dealer wins!")
        else:
            self.end_game("It's a tie!")

    def restart_game(self):
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.deck = self.shuffle_deck()
        self.game_over = False
        self.hit_button.config(state=tk.ACTIVE)
        self.stand_button.config(state=tk.ACTIVE)
        self.start_game()
    
    def start_game(self):
        print("Start game")
        if len(self.deck) > 10:
            self.deck = self.shuffle_deck()
        self.player_hand = [self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.update_ui()
        # Check for immediate blackjack
        if self.player_score >= 21:
            self.end_game("whitejack! You win!")

    def end_game(self, result_message):
        print("Game Over")
        self.game_over = True
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.show_dealer_cards()
        messagebox.showinfo("Game over", result_message)

    def show_dealer_cards(self):
        if self.game_over:
            return
        while self.dealer_score < 17:
            if not self.deck:
                self.deck = self.shuffle_deck()
            self.dealer_hand.append(self.deck.pop())
            self.dealer_score = self.calculate_score(self.dealer_hand)
            self.update_ui()

    def calculate_score(self, hand):
        score = 0
        ace_score = 0
        for card, _ in hand:
            score += CARD_VALUES[card]
            if card == "A":
                ace_score += 1
        while score > 21 and ace_score:
            score -= 10
            ace_score -= 1
        return score

    def calculate_bust_probability(self):
        target_score = 21 - self.player_score
        bust_cards = 0
        total_cards = len(self.deck)
        
        for value, _ in self.deck:
            if CARD_VALUES[value] > target_score:
                bust_cards += 1
        
        if total_cards == 0:
            return 0.0  # Si no hay cartas restantes, no puede calcularse
        
        probability = bust_cards / total_cards
        return probability

    def load_card_image(self, value, suit):
        card_name = f"{value}_of_{suit}.png"
        if card_name not in self.card_images:
            image_path = os.path.join(CARD_IMAGE_PATH, card_name)
            image = Image.open(image_path)
            image = image.resize((100, 150), Image.Resampling.LANCZOS)
            self.card_images[card_name] = ImageTk.PhotoImage(image)
        return self.card_images[card_name]

    def display_cards(self, hand, frame):
        print("display frame")
        for widget in frame.winfo_children():
            widget.destroy()
        for value, suit in hand:
            card_image = self.load_card_image(value, suit)
            label = tk.Label(frame, image=card_image, bg="#fff")
            label.image = card_image
            label.pack(side=tk.LEFT, padx=5)

    def update_ui(self):
        print("update UI")
        self.player_score = self.calculate_score(self.player_hand)
        self.display_cards(self.player_hand, self.player_frame)
        self.player_score_label.config(text=f"Your score: {self.player_score}")

        if self.game_over or self.stand_button["state"] == tk.DISABLED:
            self.dealer_score = self.calculate_score(self.dealer_hand)
            self.display_cards(self.dealer_hand, self.dealer_frame)
        else:
            self.display_cards(self.dealer_hand, self.dealer_frame)
        self.dealer_score_label.config(text=f"Dealer's score: {self.dealer_score}")

# Main function
def main():
    print("Start whiteJack Version2")
    game = whiteJackGame()
    game.mainloop()

main()
