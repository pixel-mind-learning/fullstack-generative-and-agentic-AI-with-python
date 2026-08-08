from agent import run_agent


def main():

    print("AI Agent")
    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        try:
            answer = run_agent(user_input)

            print("\nFINAL ANSWER:")
            print(answer)

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
