# __Bot assistant__
This is the __CLI Address Book__ - an application that will simplify your work with contact information and save your time for more interesting cases.
Updated and improved by __"Bot farm"__ team.

# __Installation instructions__ :
```sh
1. Create a new folder on the local computer, and sqitch to it
2. git clone https://github.com/piavik/Team_project_01
3. cd Team_project_01
4. python setup.py install
```

# __User manual__
## _When using commands, note the following features:_
- (information for the command).
- the input information should be separated by space.
- Use date format "YYYY-MM-DD".
- If the contact is absent - the command will create a new contact.

## 1. _Commands to work with address book:_
| Instruction name | Arguments | Explanations |
| ------ | ------ | ------ |
| "hello" or "hi"  | - | greeting |
| "help" or "?" | - | calling for help |
| "show all" or "all" | - | display all the contents of the address book |
| "add phone" or "add"| (name and phone) | add phone number to the contact |
| "change phone" | (name, old phone, new phone) | edit contact's phone |
| "get contact" | (name) | show all the information about the contact |
| "delete" | (name or phone) | delete the contact's phone number or the contact record itself |
| "load" | - | load address book from file |
| "save" | - | save address book to file |
| "find" | (string) | search for matches in the address book |
| "birthdays" | (number of days) | show the contacts that have a birthday in the next XX days |
| "add email" | (name and email) | add contact's email |
| "change email" | (name, old email and new email) | change contact's email |
| "delete email" | (name) |  remove contact's email |
| "add adress" | (name and address) | add contact's address |
| "change adress" | (name and new address)| change contact's address |
| "delete adress" | (name and address) | delete contact's adress |

## 2. _Commands to work with address book:_
| Instruction name | Explanations |
| ------ | ------ |
| "add note" | add notes |
| "add tags" | add tags |
| "change note" | change notes |
| "delete note" | delete notes |
| "delete tags" | remove tags |        
| "find note" |  find note |
| "sort notes" | sort notes by tag |
_***Notes search will ask of you want to search by a tag or search for the text inside all the notes_

## 3. _Command to organize files in a folder:_
| Instruction name | Arguments | Explanations |
| ------ | ------ | ------ |
| "sort folder" | (name folder) | organize files in a specified folder |
# _Good luck!_