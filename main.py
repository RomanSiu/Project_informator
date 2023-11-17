from types import GeneratorType
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from notes import NoteRecord, add_record, find_by_tag, find_by_note, delete_note, sort_notes, save_notes, load_notes
from classes import Record, AddressBook
import folder_sort


RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

FILENAME = "book.dat"
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
            result = "Sorry, I do not understand."
        else:
            return result
        return f'{RED}{result}{RESET}'
    return inner

def hello(*args):
    return f'{BLUE}Hello, how can I help you?{RESET}'

@input_error
def add_phone(contact_name: str, *args, **kwargs) -> str:
    if len(args) > 0:
        new_phone = args[0]
    else:
        new_phone = input(f'{BLUE}Please enter the phone number ({GREEN}10 digits{BLUE}): {RESET}')
    if contact_name in address_book.data.keys():
        record = address_book.data[contact_name]
        record.add_phone(new_phone)
    else:
        record = Record(contact_name)
        record.add_phone(new_phone)
        address_book.add_record(record)
    if len(args) >=2 :
        birthday = args[1]
        record.add_birthday(birthday)
    message = f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Phone: {RESET}{new_phone}"
    return message

@input_error
def add_birthday(contact_name: str, *args, **kwargs) -> str:
    if len(args) > 0:
        birthday = args[0]
    else:
        birthday = input(f'{BLUE}Please enter birthday ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
    if contact_name in address_book.data.keys():
        record = address_book.data[contact_name]
        record.add_birthday(birthday)
    else:
        if datetime.strptime(contact_name, '%Y-%m-%d'):
            raise ValueError
        record = Record(contact_name)
        record.add_birthday(birthday)
        address_book.add_record(record)
    message = f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Birthday: {RESET}{birthday}"
    return message

@input_error
def change_phone(*args):
    if len(args) == 1:
        contact_name = args[0]
    else: 
        contact_name = input(f'{BLUE}Please enter contact name: {RESET}')
    record = address_book.data[contact_name]
    if len(args) == 3:
        old_phone, new_phone = args[1:2]
    else:
        old_phone = input(f'{BLUE}Please enter old number: {RESET}')
        if old_phone not in record.phones:
            raise KeyError
        new_phone = input(f'{BLUE}Please enter new number ({GREEN}10 digits{BLUE}): {RESET}')
    record.edit_phone(old_phone, new_phone)
    return f"\n{GREEN}Changed:\n  {BLUE}Phone: {RESET}{old_phone} --> {new_phone}"

@input_error
def change_birthday(*args):
    if len(args) > 0:
        contact_name = args[0]
    else:
        contact_name = input(f'{BLUE}Please enter contact name: {RESET}')
    record = address_book.data[contact_name]
    if len(args) == 3:
        old_birthday, new_birthday = args[1:]
    else:
        new_birthday = input(f'{BLUE}Please enter new birthday date ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
    record.add_birthday(new_birthday)
    return f"\n{GREEN}Changed to:{RESET} {new_birthday}"

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

@input_error
def delete_phone(*args):
    contact_name = args[0]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if args[1:]:
        phones = args[1:]
        record = address_book.data[contact_name]
        for phone in phones:
            record.remove_phone(phone)
    else:
        res = input(f"{RED}Are you sure you want to delete contact {contact_name}?{GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if res != "yes" and res != "y":
            return f"{RED}Contact wasn't delete!{RESET}"
        address_book.delete(contact_name)
    return f'{GREEN}Removed.{RESET}'

@input_error
def delete_birthday(*args):
    contact_name = args[0]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record = address_book.data[contact_name]
    delattr(record, "birthday")
    return f'{GREEN}Removed.{RESET}'

def restore_data_from_file(*args, file_name=FILENAME) -> str:
    address_book.load(file_name)
    return file_name

def save_data_to_file(file_name=FILENAME, *args):
    address_book.save(file_name)
    return f"{GREEN}Saved to {file_name}{RESET}"


@input_error
def add_email(*args):
    if len(args) < 1:
        contact = input(f"{BLUE}Please enter the name: {RESET}")
        contact_name = contact
    else:
        contact_name = args[0]
    record = Record(contact_name)
    if contact_name not in list(address_book.data.keys()):
        address_book.add_record(record)
    if len(args) <= 1:
        email = input(f"{BLUE}Please enter the email: {RESET}")
        if email in [e.value for e in record.emails]:
            return f"{BLUE}{contact_name} already has this email: {RESET}{email} {BLUE}Skipping...{RESET}"
        email_to_add = email
    else:
        email_to_add = args[1]
    address_book.find(contact_name).add_email(email_to_add)
    return f"{GREEN}Added: {RESET}{email_to_add}"


@input_error
def change_email(*args):
    contact_name = args[0]
    record:Record = address_book.data[contact_name]
    if len(args) <= 1:
        old_email = input(f"{BLUE}Please enter email you want to change: {RESET}")
        if old_email not in [e.value for e in record.emails]:
            return f"{BLUE}{contact_name} does not have {RESET}{old_email} {BLUE}Skipping...{RESET}"
        new_email = input(f"{BLUE}Please enter new email: {RESET}")
    else:
        old_email = args[1]
        new_email = args[2]
    record.change_email(old_email, new_email)
    return f"\n{GREEN}Email changed:\n  {RESET}{old_email} --> {new_email}"


@input_error
def delete_email(*args):
    contact_name = args[0]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
    if args[1:]:
        emails_to_delete = args[1:]
    else:
        emails_to_delete = [input(f"{BLUE}Please enter email: {RESET}")]
    for email in emails_to_delete:
        if email not in [e.value for e in record.emails]:
            return f"{BLUE}{contact_name} does not have such email. Skipping...{RESET}"
        else:
            record.delete_email(email)
    return f'{GREEN}Done.{RESET}'


@input_error
def add_adress(*args):
    contact_name = args[0]
    record:Record = address_book.data[contact_name]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if len(args) <= 1:
        adress_to_add = [input(f"{BLUE}Enter adress: {RESET}")]
    else:
        adress_to_add = args[1:]
    if len(adress_to_add[0].strip()) < 1:
        raise ValueError
    if hasattr(record, 'adress'):
        ask = input(f"{BLUE}Previous adress '{record.adress}' will be deleted. OK? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: {RESET}")
        if "y" not in ask.lower():
            raise ValueError
    adress = ' '.join(str(e).capitalize() for e in adress_to_add)
    address_book.find(contact_name).add_adress(adress)
    return f"{GREEN}New adress added: {RESET}{adress}"


@input_error
def change_adress(*args):
    contact_name = args[0]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if len(args) <= 1:
        new_adress = [input(f"{BLUE}Please enter new adress: {RESET}")]
        new_adress = new_adress[0].split(" ")
        if len(new_adress[0]) < 1:
            raise IndexError
        else:
            new_adress = ' '.join(str(e).capitalize() for e in new_adress)
    else:
        new_adress = ' '.join(str(e).capitalize() for e in args[1:])
    record:Record = address_book.data[contact_name]
    record.delete_adress()
    record.add_adress(new_adress)
    return f'{GREEN}New adress:\n{RESET}{new_adress}'


@input_error
def delete_adress(*args):
    contact_name = args[0]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
    if not hasattr(record, "adress"):
        return f"{BLUE}{contact_name} does not have any addresses. Skipping...{RESET}"
    record.delete_adress()
    return f'{GREEN}Done.{RESET}'


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
    note = input(f"{BLUE}Please enter new note: {RESET}")
    if not note:
        res = input(f"{RED}Are you sure you want to save blank note?{GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if res != "y" and res != "yes":
            return f"{RED}Note wasn't save!{RESET}"
    note_rec = NoteRecord(note)
    tags = input(f"{BLUE}Please enter note tags: {RESET}")
    note_rec.add_tags(tags.split(", ") if "," in tags else tags.split(" "))
    add_record(note_rec)
    save_notes()
    return f"{GREEN}The note was saved.{RESET}"

@input_error
def find_note():
    find_func = input(f"Select search by {GREEN}[t]{RESET}ags or {GREEN}[n]{RESET}otes.")
    if find_func in "tags":
        use_func = find_by_tag
    elif find_func in "notes":
        use_func = find_by_note
    else:
        return f"{RED}You must choose: search by tags or notes!{RESET}"
    request = input(f"{BLUE}Searching for: {RESET}")
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
            print(f"{num}. {rec.note}")
            num += 1
        indx = input("{BLUE}Please enter the number of the note you want to edit: {RESET}")
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    return found_notes, indx

@input_error
def change_note():
    found_notes, indx = find_note_to_func()
    changed_note = input(f"{BLUE}Please enter the note to change: {RESET}")
    if not changed_note:
        request = input(f"{RED}Do you want save a blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if request != "y":
            return f"{RED}Note was not not changed.{RESET}"
    found_notes[int(indx)-1].edit_note(changed_note)
    return f"{GREEN}The note was changed.{RESET}"

@input_error
def add_tags():
    found_notes, indx = find_note_to_func()
    new_tags = input(f"{BLUE}Please enter the tags you want to add: {RESET}")
    found_notes[int(indx)-1].add_tags(new_tags.split(", ") if "," in new_tags else new_tags.split(" "))
    return f"{GREEN}Tags were added.{RESET}"

@input_error
def delete_tags():
    found_notes, indx = find_note_to_func()
    tags_to_del = input(f"{BLUE}Please enter the tags you want to delete: {RESET}")
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
            print(f"{num}. {rec.note}")
            num += 1
        indx = input(f"{BLUE}Please enter the number of the note you want to delete: {RESET}")
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    check = input(f"{RED}Are you sure you want to delete this entry? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
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
                "add phone": add_phone,
                "add birthday": add_birthday,
                "add note": add_note,
                "add tags": add_tags,
                "add email": add_email,
                "add address": add_adress,
                "add": add_phone,
                "change address": change_adress,
                "change phone": change_phone,
                "change birthday": change_birthday,
                "change note": change_note,
                "change email": change_email,
                "change": change_phone, 
                "get contact": get_phone,
                "get": get_phone,
                "all": all_contacts,
                "show all": all_contacts,
                "delete phone": delete_phone,
                "delete birthday": delete_birthday,
                "delete note": del_note,
                "delete tags": delete_tags,
                "delete address": delete_adress,
                "delete email": delete_email,
                "delete": delete_phone,
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
command_completer = WordCompleter(ALL_COMMANDS)

def parse(input_text: str):
    for kw, func in OPERATIONS.items():
        if input_text.startswith(kw):
            params = input_text[len(kw):].strip()
            return func, params.split()
    return unknown_command, []


def main():
    file_name = FILENAME
    address_book.load(file_name)
    load_notes()
    print(f'{RESET}{hello()}')
    while True:
        input_ = prompt(">>> ", completer=command_completer)
        input_ = input_.lower()
        if input_.strip() in STOP_WORDS:
            # TODO: format dependent
            save_data_to_file(file_name)
            save_notes()
            print(f"{GREEN}See you, bye!{RESET}")
            break
        if input_.strip() == '':
            continue
        command, parameters = parse(input_)
        command_to_run = command(*parameters)
        if isinstance(command_to_run, GeneratorType):
            for _selection in command_to_run:
                for _entry in _selection:
                    print(_entry)
                    print('----------')
                _ = input(f"{RESET}....Press {BLUE}Enter{RESET} to continue....\n")
        elif isinstance(command_to_run, list):
            for rec in command_to_run:
                print(rec)
        else:
            print(f'{RESET}{command_to_run}')

if __name__ == "__main__":
    main()
