from models import BaseItem, Note, Expense

def test_note_is_base_item():
    note = Note("Идея", "Текст заметки")
    assert isinstance(note, BaseItem)


def test_expense_is_base_item():
    e = Expense("Обед", 350)
    assert isinstance(e, BaseItem)

if __name__ == "__main__":
    test_note_is_base_item()
    test_expense_is_base_item()