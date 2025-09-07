# Basic text-based menu simulation

def show_menu():
    print("\nEO/IR Simulator Menu")
    print("1. Infrared Mode")
    print("2. Daylight Mode")
    print("3. Zoom In")
    print("4. Zoom Out")
    print("q. Quit")

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Select option: ")
        if choice == "q":
            break
        elif choice == "1":
            print("[EOIR] Switching to Infrared Mode")
        elif choice == "2":
            print("[EOIR] Switching to Daylight Mode")
        elif choice == "3":
            print("[EOIR] Zooming In")
        elif choice == "4":
            print("[EOIR] Zooming Out")
        else:
            print("Invalid choice")
