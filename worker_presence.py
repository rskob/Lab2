from costs import Expense, Category


class InfoWorker:
    @staticmethod
    def get_expenses_info(expenses: list[Expense], category: Category | None = None) -> str:
        """Выводит на экран все расходы по категории, если она указана. В противном случае все расходы"""
        if category:
            expenses = filter(lambda exp: exp.category == category, expenses)
            head = f"========== РАСХОДЫ (Категория: '{category}') ===========\n"
        else:
            head = f"========== РАСХОДЫ ==========="

        for number, ex in enumerate(expenses, start=1):
            head += f"\n  [{number}] {ex}"

        return head

    @staticmethod
    def get_total_info(expenses: list[Expense], category: Category | None = None) -> str:
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
        return f"Суммарная стоимость расходов{category_string}: {total:.2f}"
