from rich import print

# print("Jak nastawienie na dzisiejszy dzień?")
# print("1 - Dobrze")
# print("2 - Chujowo")
# print("3 - Średnio")
# odpowiedz = input("Wybierz odpowiedź 1, 2, 3: ")
# dobrze = "1"
# chujowo = "2"
# srednio = "3"

# if odpowiedz == dobrze:
#     print("To powodzenia")
# elif odpowiedz == chujowo:
#     print("To pierdol to idź spać")
# elif odpowiedz == srednio:
#     print("To zrób pół normy")
# else:
#     print("Nir pierdol wybieraj")


# enter in terminal ->  .\.venv\Scripts\activate.ps1    <-  before run the script
# # to run the script use => uv run POZDOWIENIA.py  <= pozdro
# this code is better.
while True:
    answer = input("Czy chcesz kontynuować? (tak/nie): ")
    if answer.lower() == "tak":
        print(
            "[red]Kontynuujemy...[/red]",
            "\nJak nastawienie na dzisiejszy dzień?",
        )
        options = {
            "1": "[yellow]To powodzenia[/yellow]",
            "2": "[green]To pierdol to idź spać[/green]",
            "3": "[pink]To zrób pół normy[/pink]",
        }
        odpowiedz = input("Wybierz odpowiedź 1, 2, 3: ")
        print(options.get(odpowiedz, "Nir pierdol wybieraj"))

    else:
        print("[blue]Dziękujemy za skorzystanie z programu. Do widzenia![/blue]")
        exit(0)  # Exit the program with a success status code
