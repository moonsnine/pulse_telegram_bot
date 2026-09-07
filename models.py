class Note:
    def __init__(self, text, tag="без тега", done=False):
        self.text = text
        self.tag= tag
        self.done = done

note1 = Note("Сдать дз", "test")
note2 = Note("Сделать алгем", "homework")
note3 = Note("Купить молоко", "магазин", True)

print(note1.text, "|", note1.tag, "|", note1.done)
print(note2.text, "|", note2.tag, "|", note2.done)
print(note3.text, "|", note3.tag, "|", note3.done)