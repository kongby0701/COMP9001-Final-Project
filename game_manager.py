import random
import os
from player import Player
from game_board import GameBoard

class GameManager:
    def __init__(self):
        self.players = []
        self.board = None
        self.current_player_index = 0
        self.turn = 1
        self.game_over = False
    
    def create_new_game(self, num_players=2):
        self.board = GameBoard(size=10)
        
        colors = [("Red", "R"), ("Blue", "B"), ("Green", "G"), ("Yellow", "Y")]
        for i in range(num_players):
            name = input(f"Enter player {i+1} name: ")
            color, symbol = colors[i % len(colors)]
            self.players.append(Player(name, color, symbol))
        
        self.save_game("game_state.txt")
    
    def load_game(self, filename="game_state.txt"):
        if not os.path.exists(filename):
            print("Save file not found!")
            return False
        
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        self.players = []
        self.turn = 1
        self.current_player_index = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("Turn:"):
                self.turn = int(line.split(":")[1].strip())
            elif line.startswith("CurrentPlayer:"):
                self.current_player_index = int(line.split(":")[1].strip())
            elif line.startswith("Player:"):
                name = line.split(":")[1].strip()
                color = lines[i+1].split(":")[1].strip()
                symbol = lines[i+2].split(":")[1].strip()
                money = int(lines[i+3].split(":")[1].strip())
                position = int(lines[i+4].split(":")[1].strip())
                in_jail = lines[i+5].split(":")[1].strip() == "True"
                jail_turns = int(lines[i+6].split(":")[1].strip())
                
                player = Player(name, color, symbol, money)
                player.position = position
                player.in_jail = in_jail
                player.jail_turns = jail_turns
                self.players.append(player)
                i += 7
            else:
                i += 1
        
        self.board = GameBoard(size=10)
        return True
    
    def save_game(self, filename="game_state.txt"):
        with open(filename, 'w') as f:
            f.write(f"Turn: {self.turn}\n")
            f.write(f"CurrentPlayer: {self.current_player_index}\n")
            f.write("\n")
            
            for player in self.players:
                f.write(f"Player: {player.name}\n")
                f.write(f"Color: {player.color}\n")
                f.write(f"Symbol: {player.symbol}\n")
                f.write(f"Money: {player.money}\n")
                f.write(f"Position: {player.position}\n")
                f.write(f"InJail: {player.in_jail}\n")
                f.write(f"JailTurns: {player.jail_turns}\n")
                f.write("\n")
        
        print(f"Game saved to {filename}")
    
    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)
    
    def handle_chance(self, player):
        events = [
            ("Get out of jail free!", lambda p: p.get_out_of_jail_cards),
            ("Go to jail!", lambda p: p.go_to_jail()),
            ("Collect $200", lambda p: p.add_money(200)),
            ("Pay $100", lambda p: p.remove_money(100)),
            ("Advance to Go", lambda p: p.position == 0),
            ("Move back 3 spaces", lambda p: p.position == (p.position - 3) % 40),
            ("Extra turn!", lambda p: setattr(p, 'extra_turn', True)),
            ("Lose a turn", lambda p: setattr(p, 'lose_turn', True)),
        ]
        
        event_name, action = random.choice(events)
        print(f"\nChance! {event_name}")
        try:
            action(player)
        except:
            pass
    
    def handle_special(self, player):
        events = [
            ("Hotel tax! Pay $50", lambda p: p.remove_money(50)),
            ("Amusement park! Collect $100", lambda p: p.add_money(100)),
            ("Developer steals property!", lambda p: self._steal_property(p)),
        ]
        
        event_name, action = random.choice(events)
        print(f"\nSpecial! {event_name}")
        try:
            action(player)
        except:
            pass
    
    def _steal_property(self, player):
        other_players = [p for p in self.players if p != player and p.properties]
        if other_players:
            target = random.choice(other_players)
            if target.properties:
                prop = random.choice(target.properties)
                target.properties.remove(prop)
                player.properties.append(prop)
                prop.owner = player
                print(f"{player.name} stole a property from {target.name}!")
    
    def play_turn(self):
        player = self.players[self.current_player_index]
        print(f"\n=== Turn {self.turn} - {player.name}'s Turn ===")
        print(f"Current money: ${player.money}")
        print(f"Current position: {player.position}")
        
        if player.in_jail:
            print("You are in jail!")
            player.jail_turns += 1
            
            if player.jail_turns >= 3:
                print("You've been in jail for 3 turns. Paying $50 to get out...")
                if player.remove_money(50):
                    player.get_out_of_jail()
                else:
                    print("Can't pay bail! Staying in jail.")
                    self.next_player()
                    return
            else:
                choice = input("Do you want to pay $50 to get out of jail? (y/n): ").lower()
                if choice == 'y' and player.remove_money(50):
                    player.get_out_of_jail()
                else:
                    print("Staying in jail...")
                    self.next_player()
                    return
        
        input("Press Enter to roll dice...")
        dice = self.roll_dice()
        print(f"You rolled: {dice}")
        
        player.move(dice)
        print(f"Moved to position {player.position}")
        
        cell = self.board.get_cell_at_position(player.position)
        if cell:
            if cell.type == 'start':
                print("Passed Go! Collect $200")
                player.add_money(200)
            elif cell.type == 'jail':
                print("Go directly to jail!")
                player.go_to_jail()
            elif cell.type == 'bank':
                print("Bank! Deposit $100")
                player.add_money(100)
            elif cell.type == 'property' and cell.owner is None:
                choice = input(f"Buy property for ${cell.price}? (y/n): ").lower()
                if choice == 'y' and player.buy_property(cell):
                    print(f"Bought {cell.name}!")
                else:
                    print("Did not buy property.")
            elif cell.type == 'property' and cell.owner != player:
                print(f"Paying rent of ${cell.rent} to {cell.owner.name}")
                if player.remove_money(cell.rent):
                    cell.owner.add_money(cell.rent)
                else:
                    print("Can't pay rent!")
            elif cell.type == 'chance':
                self.handle_chance(player)
            elif cell.type == 'special':
                self.handle_special(player)
        
        self.check_game_over()
        self.next_player()
    
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:
            self.turn += 1
    
    def check_game_over(self):
        bankrupt_players = [p for p in self.players if p.money < 0]
        if len(bankrupt_players) >= len(self.players) - 1:
            winner = next(p for p in self.players if p.money >= 0)
            print(f"\n=== GAME OVER ===")
            print(f"{winner.name} wins with ${winner.money}!")
            self.game_over = True
    
    def play_game(self):
        while not self.game_over:
            self.board.display_board(self.players)
            self.play_turn()
            
            if not self.game_over:
                choice = input("Save game? (y/n): ").lower()
                if choice == 'y':
                    self.save_game()
