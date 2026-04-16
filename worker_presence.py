from costs import Expense, Category



def print_expenses(expenses: list[Expense], category: Category | None = None) -> None:
    """Выводит на экран все расходы по категории, если она указана. В противном случае все расходы"""
    if category:
        expenses = filter(lambda exp: exp.category == category, expenses)
        head = f"========== РАСХОДЫ (Категория: '{category}') ==========="
    else:
        head = f"========== РАСХОДЫ ==========="

    print(head)
    for number, ex in enumerate(expenses, start=1):
        print(f"  [{number}] {ex}")


def print_total(expenses: list[Expense], category: Category | None = None) -> None:
    """
    Выводит на экран сумму расходов по категории, если она указана.
    В противном случае суммарную стоимость всех расходов.
    """
    if category:
        category_string = f" (Категория: '{category}')"
        expenses = filter(lambda exp: exp.category == category, expenses)
    else:
        category_string = ""

    total = sum(map(lambda exp: exp.cost, expenses))
    print(f"Суммарная стоимость расходов{category_string}: {total:.2f}")