from datetime import datetime
import pickle

BLUE = "\033[94m"
RESET = "\033[0m"

class NoteRecord():
    def __init__(self, note: str) -> None:
        self.note = note
        self.tags = []
        self.create_date = datetime.now().date()
        self.change_date = None

    def add_tags(self, tags: list) -> None:
        for i in tags:
            self.tags.append(i.lower())

    def del_tags(self, tags_to_del: list) -> None:
        for i in tags_to_del:
            self.tags.remove(i) if i in self.tags else ...

    def edit_note(self, new_note: str) -> None:
        self.note = new_note

    def __str__(self):
        return f"{BLUE}Tags:{RESET} {', '.join(self.tags)}\n{BLUE}Note:{RESET} {self.note}\n{BLUE}Date of creation:{RESET} {self.create_date}.\n"

try:
    notes_lst[0]
except NameError:
    notes_lst = []

def add_record(record: NoteRecord) -> None:
    notes_lst.append(record)
    
def find_by_tag(key: str) -> list:
    notes = []
    for i in notes_lst:
        if key.lower() in i.tags:
            notes.append(i)
    return notes
    
def find_by_note(key: str) -> list:
    notes = []
    for i in notes_lst:
        if key in i.note:
            notes.append(i)
    return notes

def sort_notes() -> list:
    lst = []
    notes_lst.sort(key = lambda x: len(x.tags), reverse=True)
    for i in notes_lst:
        lst.append(i)
    return lst

def delete_note(key) -> None:
    notes_lst.remove(key)

def save_notes(filename="notes_book.bin") -> None:
    with open(filename, 'wb') as fh:
        pickle.dump(notes_lst, fh)
        
def load_notes(filename="notes_book.bin") -> None:
    global notes_lst
    try:
        with open(filename, 'rb') as fh:
            notes_lst = pickle.load(fh)
    except FileNotFoundError:
        ...

if __name__ == "__main__":
    ...