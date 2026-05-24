from game_manager import GameManager

def main():
    print("=" * 50)
    print("         MONOPOLY GAME         ")
    print("=" * 50)
    
    gm = GameManager()
    
    while True:
        choice = input("\n1. New Game\n2. Load Game\n3. Exit\nChoose an option: ")
        
        if choice == '1':
            num_players = int(input("Enter number of players (2-4): "))
            num_players = max(2, min(4, num_players))
            gm.create_new_game(num_players)
            gm.play_game()
        elif choice == '2':
            if gm.load_game():
                gm.play_game()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()
