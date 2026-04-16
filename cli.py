import re
from runner import run_review
from github import get_pr_diff, handle_confirm
from rich import print

def parse_prs(text):
    nums = re.findall(r"#(\d+)", text)
    return [int(n) for n in nums]

def main():
    user_input = input("Enter command (review #23,#24): ")
    prs = parse_prs(user_input)

    if not prs:
        print("[red]No PR numbers found[/red]")
        return

    # fetch all diffs
    diffs = []
    for pr in prs:
        print(f"[yellow]Fetching PR #{pr}...[/yellow]")
        diffs.append(get_pr_diff(pr))

    full_diff = "\n\n".join(diffs)

    refinements = []
    confirmed = False

    while not confirmed:
        instruction_text = "\n".join(refinements)

        print("\n[cyan]Running AI review...[/cyan]")
        result = run_review(full_diff, instruction_text)

        print("\n[bold green]Summary:[/bold green]")
        print(result.get("summary"))
        print("\nRAW OUTPUT:\n", result)

        print("\n[bold red]Issues:[/bold red]")
        for i, issue in enumerate(result.get("issues", []), 1):
            print(f"{i}. {issue['file']}:{issue['line']} [{issue['severity']}]")
            print(f"   {issue['comment']}")
            print(f"   💡 {issue['suggestion']}")

        print("\nCommands:")
        print("- refine <text>")
        print("- confirm")
        print("- cancel")
        print("- reset")

        cmd = input("\n> ")

        if cmd.startswith("refine"):
            refinements.append(cmd.replace("refine", "").strip())

        elif cmd == "reset":
            refinements = []

        elif cmd == "confirm":
            confirmed = True

            print("\nPosting review to GitHub...")

            handle_confirm(prs[0], result)

            print("Done ✅")

        elif cmd == "cancel":
            print("[red]Cancelled[/red]")
            break

if __name__ == "__main__":
    main()