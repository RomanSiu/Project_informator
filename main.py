from types import GeneratorType
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from abc import abstractmethod, ABC

from notes import NoteRecord, add_record, find_by_tag, find_by_note, delete_note, sort_notes, save_notes, load_notes
from classes import Record, AddressBook
import folder_sort


RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

file_name = "book.dat"
STOP_WORDS = [
                'good bye', 
                'goodbye', 
                'bye', 
                'close', 
                'exit', 
                'quit', 
                'stop', 
                'enough',
                'finish',
                'pa',
                'q'
            ]

def input_error(func):
    ''' 
    returns FUNCTION, not string !!!
    '''
    def inner(*args):
        try:
            result = func(*args)
        except KeyError:
            result = "Not found."
        except ValueError:
            result = "Entered incorrect data."
        except IndexError:
            result = "Not enough parameters."
        except TypeError:
            result = "Write command in right format.(Use help!)"
        except AttributeError:
            result = "Not found."
        else:
            return result
        return f'{RED}{result}{RESET}'
    return inner

def hello():
    return f'{BLUE}Hello, how can I help you?{RESET}'

class AddClass(ABC):       
    @abstractmethod
    def add(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def check_args(self) -> None:
        raise NotImplementedError
    
class AddContact(AddClass):
    def __init__(self, name = None, phone = None, *args) -> None:
        self.name = name
        self.phone = phone
    
    @input_error    
    def add(self) -> str:
        self.check_args()
        if self.name in address_book.data.keys():
            record = address_book.data[self.name]
            record.add_phone(self.phone)
        else:
            record = Record(self.name)
            record.add_phone(self.phone)
            address_book.add_record(record)
        return f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Phone: {RESET}{self.phone}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.phone:
            self.phone = base_input.side_inp(f"{BLUE}Write new phone:{RESET} ")
            
class AddBirthday(AddClass):
    def __init__(self, name = None, bd = None, *args) -> None:
        self.name = name
        self.bd = bd
    
    @input_error    
    def add(self) -> str:
        self.check_args()
        if self.name in address_book.data.keys():
            record = address_book.data[self.name]
            record.add_birthday(self.bd)
        else:
            record = Record(self.name)
            record.add_birthday(self.bd)
            address_book.add_record(record)
        return f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Birthday: {RESET}{self.bd}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.bd:
            self.bd = base_input.side_inp(f'{BLUE}Please enter birthday ({GREEN}DD.MM.YYYY{BLUE}): {RESET}')
            
class AddEmail(AddClass):
    def __init__(self, name = None, email = None, *args) -> None:
        self.name = name
        self.email = email
    
    @input_error    
    def add(self) -> str:
        self.check_args()
        if self.name in address_book.data.keys():
            record = address_book.data[self.name]
            if self.email in [e.value for e in record.emails]:
                return f"{BLUE}{self.name} already has this email: {RESET}{self.email} {BLUE}Skipping...{RESET}"
            record.add_email(self.email)
        else:
            record = Record(self.name)
            record.add_email(self.email)
            address_book.add_record(record)
        return f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Email: {RESET}{self.email}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.email:
            self.email = base_input.side_inp(f'{BLUE}Please enter email: {RESET}')
            
class AddAddress(AddClass):
    def __init__(self, name = None, address = None, *args) -> None:
        self.name = name
        self.address = address + " " + " ".join(args)
    
    @input_error    
    def add(self) -> str:
        self.check_args()
        if self.name in address_book.data.keys():
            record = address_book.data[self.name]
            record.add_address(self.address)
        else:
            record = Record(self.name)
            record.add_address(self.address)
            address_book.add_record(record)
        return f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Address: {RESET}{self.address}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.address:
            self.address = base_input.side_inp(f'{BLUE}Please enter address: {RESET}')
                  
class ChangeClass(ABC):
    @abstractmethod
    def change(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def check_args(self) -> None:
        raise NotImplementedError
    
class ChangeContact(ChangeClass):
    def __init__(self, name = None, old_phone = None, new_phone = None, *args) -> None:
        self.name = name
        self.old_phone = old_phone
        self.new_phone = new_phone
    
    @input_error
    def change(self) -> str:
        self.check_args()
        record = address_book.data[self.name]
        record.edit_phone(self.old_phone, self.new_phone)
        return f"\n{GREEN}Changed:\n  {BLUE}Phone: {RESET}{self.old_phone} --> {self.new_phone}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.old_phone:
            self.old_phone = base_input.side_inp(f"{BLUE}Write phone you want to change:{RESET} ")
        elif not self.new_phone:
            self.new_phone = base_input.side_inp(f"{BLUE}Write new phone:{RESET} ")
            
class ChangeBirthday(ChangeClass):
    def __init__(self, name = None, new_bd = None, *args) -> None:
        self.name = name
        self.new_bd = new_bd
    
    @input_error    
    def change(self) -> str:
        self.check_args()
        record = address_book.data[self.name]
        record.add_birthday(self.new_bd)
        return f"\n{GREEN}Changed to:{RESET} {self.new_bd}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.new_bd:
            self.new_bd = base_input.side_inp(f"{BLUE}Write new birthday:{RESET} ")

class ChangeEmail(ChangeClass):
    def __init__(self, name = None, old_email = None, new_email = None, *args) -> None:
        self.name = name
        self.old_email = old_email
        self.new_email = new_email
    
    @input_error    
    def change(self) -> str:
        self.check_args()
        record = address_book.data[self.name]
        record.change_email(self.old_email, self.new_email)
        return f"\n{GREEN}Email changed:\n  {RESET}{self.old_email} --> {self.new_email}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.old_email:
            self.old_email = base_input.side_inp(f"{BLUE}Write email you want to change:{RESET} ")
        elif not self.new_email:
            self.new_email = base_input.side_inp(f"{BLUE}Write new email:{RESET} ")
            
class ChangeAddress(ChangeClass):
    def __init__(self, name = None, new_address = None, *args) -> None:
        self.name = name
        self.new_address = new_address + " " + " ".join(args)
    
    @input_error    
    def change(self) -> str:
        self.check_args()
        record = address_book.data[self.name]
        record.add_address(self.new_address)
        return f"\n{GREEN}Changed to:{RESET} {self.new_address}"
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.new_address:
            self.new_address = base_input.side_inp(f"{BLUE}Write new address:{RESET} ")
            
class DeleteClass(ABC):
    @abstractmethod
    def delete(self) -> str:
        raise NotImplementedError
            
class DeleteContact(DeleteClass):
    def __init__(self, name = None, phone = None, *args) -> None:
        self.name = name
        self.phone = phone
    
    @input_error   
    def delete(self) -> str:
        record = address_book.data[self.name]
        if self.phone:
            record.remove_phone(self.phone)
        else:
            res = base_input.side_inp(f"{RED}Are you sure you want to delete contact {self.name}?{GREEN}[y]es/[n]o:{RESET} ")
            if res != "yes" and res != "y":
                return f"{RED}Contact wasn't delete!{RESET}"
            address_book.delete(self.name)
        return f'{GREEN}Removed.{RESET}'

class DeleteBirthday(DeleteClass):
    def __init__(self, name = None, *args) -> None:
        self.name = name
        
    @input_error
    def delete(self) -> str:
        record = address_book.data[self.name]
        delattr(record, "birthday")
        return f'{GREEN}Removed.{RESET}'
    
class DeleteEmail(DeleteClass):
    def __init__(self, name = None, email = None) -> None:
        self.name = name
        self.email = email
    
    @input_error    
    def delete(self) -> str:
        self.check_args()
        record = address_book.data[self.name]
        if self.email not in [e.value for e in record.emails]:
            return f"{BLUE}{self.name} does not have such email. Skipping...{RESET}"
        else:
            record.delete_email(self.email)
        return f'{GREEN}Removed.{RESET}'
    
    def check_args(self) -> None:
        if not self.name:
            raise TypeError
        elif not self.email:
            self.email = base_input.side_inp(f"{BLUE}Write email you want to delete:{RESET} ")

class DeleteAddress(DeleteClass):
    def __init__(self, name = None, *args) -> None:
        self.name = name
        
    @input_error
    def delete(self) -> str:
        record = address_book.data[self.name]
        delattr(record, "address")
        return f'{GREEN}Removed.{RESET}'

@input_error
def get_phone(*args):
    return address_book.find(args[0])

def all_contacts(N=3, *args):
    return address_book.iterator(N)

def help_(*args):
    with open('README.md', 'r') as fh:
        help_bot = fh.read()
    return help_bot
    
def unknown_command(*args):
    return f"{RED}I do not understand, please use correct command.{RESET}"

def restore_data_from_file() -> str:
    address_book.load(file_name)
    return file_name

def save_data_to_file():
    address_book.save(file_name)
    return f"{GREEN}Saved to {file_name}{RESET}"

@input_error
def random_search(*args) -> GeneratorType:
    search = args[0]
    if len(search) < 3:
        if len(' '.join(args)) > 2:
            search = ' '.join(args)
        else:
            raise IndexError
    search_result = AddressBook()
    if search.isnumeric():
        for record in address_book.values():
            for phone in record.phones:
                if search in str(phone.value):
                    search_result.add_record(record)
    else:
        for name, record in address_book.data.items():
            if search in name:
                search_result.add_record(record)
    if not search_result:
        raise KeyError
    return search_result.iterator(2)

@input_error
def birthday_in_XX_days(*args):
    return address_book.bd_in_xx_days(int(args[0]))

@input_error
def add_note():
    note = base_input.side_inp(f"{BLUE}Please enter new note: {RESET}")
    if not note:
        res = base_input.side_inp(f"{RED}Are you sure you want to save blank note?{GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if res != "y" and res != "yes":
            return f"{RED}Note wasn't save!{RESET}"
    note_rec = NoteRecord(note)
    tags = base_input.side_inp(f"{BLUE}Please enter note tags: {RESET}")
    note_rec.add_tags(tags.split(", ") if "," in tags else tags.split(" "))
    add_record(note_rec)
    save_notes()
    return f"{GREEN}The note was saved.{RESET}"

@input_error
def find_note():
    find_func = base_input.side_inp(f"Select search by {GREEN}[t]{RESET}ags or {GREEN}[n]{RESET}otes.")
    if find_func in "tags":
        use_func = find_by_tag
    elif find_func in "notes":
        use_func = find_by_note
    else:
        return f"{RED}You must choose: search by tags or notes!{RESET}"
    request = base_input.side_inp(f"{BLUE}Searching for: {RESET}")
    res = use_func(request)
    if not res:
        raise KeyError
    return res

@input_error
def find_note_to_func():
    num = 1
    found_notes = find_note()
    if isinstance(found_notes, str):
        return found_notes
    elif len(found_notes) > 1:
        for rec in found_notes:
            base_output.output(f"{num}. {rec.note}")
            num += 1
        indx = base_input.side_inp("{BLUE}Please enter the number of the note you want to edit: {RESET}")
    elif len(found_notes) == 1:
        indx = 1
    base_output.output(found_notes[int(indx)-1])
    return found_notes, indx

@input_error
def change_note():
    found_notes, indx = find_note_to_func()
    changed_note = base_input.side_inp(f"{BLUE}Please enter the note to change: {RESET}")
    if not changed_note:
        request = base_input.side_inp(f"{RED}Do you want save a blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if request != "y":
            return f"{RED}Note was not not changed.{RESET}"
    found_notes[int(indx)-1].edit_note(changed_note)
    return f"{GREEN}The note was changed.{RESET}"

@input_error
def add_tags():
    found_notes, indx = find_note_to_func()
    new_tags = base_input.side_inp(f"{BLUE}Please enter the tags you want to add: {RESET}")
    found_notes[int(indx)-1].add_tags(new_tags.split(", ") if "," in new_tags else new_tags.split(" "))
    return f"{GREEN}Tags were added.{RESET}"

@input_error
def delete_tags():
    found_notes, indx = find_note_to_func()
    tags_to_del = base_input.side_inp(f"{BLUE}Please enter the tags you want to delete: {RESET}")
    found_notes[int(indx)-1].del_tags(tags_to_del.split(", ") if "," in tags_to_del else tags_to_del.split(" "))
    return f"{GREEN}Done.{RESET}"

@input_error
def del_note():
    num = 1
    found_notes = find_note()
    if isinstance(found_notes, str):
        return found_notes
    elif len(found_notes) > 1:
        for rec in found_notes:
            base_output.output(f"{num}. {rec.note}")
            num += 1
        indx = base_input.side_inp(f"{BLUE}Please enter the number of the note you want to delete: {RESET}")
    elif len(found_notes) == 1:
        indx = 1
    base_output.output(found_notes[int(indx)-1])
    check = base_input.side_inp(f"{RED}Are you sure you want to delete this entry? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
    if check == "y":
        delete_note(found_notes[int(indx)-1])
        return f"{GREEN}Note was deleted.{RESET}"
    else:
        return f"{RED}Note was not deleted!{RESET}"
        
def sort_folder(*args):
    ''' Sort files from a single folder into categorized folders '''
    if not args:
        folder = input(f"{BLUE}Please enter the folder name: {RESET}")
        if not folder:
            raise IndexError
    else:
        folder = args[0]
    return folder_sort.main(folder)


address_book = AddressBook()

# order MATTERS!!!! Single word command must be in the end !
OPERATIONS = {
                "hello": hello,
                "help": help_,
                "?": help_,
                "add phone": (AddContact, "add"),
                "add birthday": (AddBirthday, "add"),
                "add note": add_note,
                "add tags": add_tags,
                "add email": (AddEmail, "add"),
                "add address": (AddAddress, "add"),
                "add": (AddContact, "add"),
                "change address": (ChangeAddress, "change"),
                "change phone": (ChangeContact, "change"),
                "change birthday": (ChangeBirthday, "change"),
                "change note": change_note,
                "change email": (ChangeEmail, "change"),
                "change": (ChangeContact, "change"), 
                "get contact": get_phone,
                "get": get_phone,
                "all": all_contacts,
                "show all": all_contacts,
                "delete phone": (DeleteContact, "delete"),
                "delete birthday": (DeleteBirthday, "delete"),
                "delete note": del_note,
                "delete tags": delete_tags,
                "delete address": (DeleteAddress, "delete"),
                "delete email": (DeleteEmail, "delete"),
                "delete": (DeleteContact, "delete"),
                # "d": debug_,
                "load": restore_data_from_file,
                "save": save_data_to_file,
                "find note": find_note,
                "find": random_search,
                "search": random_search,
                "sort notes": sort_notes,
                "birthdays": birthday_in_XX_days,
                "sort folder": sort_folder
              }

ALL_COMMANDS = OPERATIONS.keys()
command_completer = WordCompleter(ALL_COMMANDS, sentence=True, ignore_case=True)

def handler(inp):
        cor_func = unknown_command
        params = []
        for kw, func in OPERATIONS.items():
            if inp.startswith(kw):
                params = inp[len(kw):].strip().split()
                cor_func = func
                break
        if isinstance(func, tuple):
            func = getattr(cor_func[0], cor_func[1])
            result = func(cor_func[0](*params))
        else:
            result = cor_func(*params)
        return result  

class InputBaseClass(ABC):
    @abstractmethod
    def main_inp(self):
        raise NotImplementedError
    
    @abstractmethod
    def side_inp(self, inp_text):
        raise NotImplementedError
    
class TerminalInput(InputBaseClass):        
    def main_inp(self):
        res = prompt(">>> ", completer=command_completer).lower()
        return res
    
    def side_inp(self, inp_text):
        res = input(inp_text)
        return res
    
class OutputBaseClass(ABC):
    @abstractmethod
    def output(self, text):
        raise NotImplementedError
    
class TerminalOutput(OutputBaseClass):
    def output(self, text):
        if isinstance(text, GeneratorType):
            for _selection in text:
                for _entry in _selection:
                    print(_entry)
                    print('----------')
        elif isinstance(text, list):
            for rec in text:
                print(rec)
        else:
            print(f'{text}')

def main():
    global base_input
    global base_output
    address_book.load(file_name)
    load_notes()
    base_input = TerminalInput()
    base_output = TerminalOutput()
    base_output.output(f'{RESET}{hello()}')
    while True:
        input = base_input.main_inp()
        if input.strip() in STOP_WORDS:
            save_data_to_file()
            save_notes()
            base_output.output(f"{GREEN}See you, bye!{RESET}")
            exit()
        if input.strip() == '':
            continue
        result = handler(input)
        base_output.output(result)

if __name__ == "__main__":
    main()
