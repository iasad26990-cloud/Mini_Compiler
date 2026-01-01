import os

def show_file(filename, title):
    """Helper to display file contents nicely."""
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = f.read().strip()
            print(content if content else "[Empty File]")
    else:
        print("[File not found!]")
    print("="*50 + "\n")

def cli_menu():
    """Interactive command-line interface."""
    while True:
        print("\nMiniLang Lexical Analyzer Menu")
        print("---------------------------------")
        print("1. View Tokens")
        print("2. View Symbol Table")
        print("3. View Token Statistics")
        print("4. View Cleaned Source Code")
        print("5. View Lexical Errors")
        print("6. View Semantic Analysis Report")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            show_file("tokens.txt", "TOKEN STREAM")
        elif choice == '2':
            show_file("symbol_table.txt", "SYMBOL TABLE")
        elif choice == '3':
            show_file("token_stats.txt", "TOKEN STATISTICS")
        elif choice == '4':
            show_file("clean_source.mini", "CLEANED SOURCE CODE")
        elif choice == '5':
            show_file("lexical_errors.txt", "LEXICAL ERRORS")
        elif choice == '6':
            show_file("semantic_analysis.txt", "SEMANTIC ANALYSIS")
        elif choice == '0':
            print("Exiting MiniLang Analyzer. ✅")
            break
        else:
            print("Invalid choice. Please try again.")

# Call CLI menu at the end
if __name__ == "__main__":
    cli_menu()
