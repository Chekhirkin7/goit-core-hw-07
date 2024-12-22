from collections import UserDict
from functools import wraps

class Field:
	def __init__ (self, value):
		self.value = value
	
	def __str__ (self):
		return str(self.value)

class Name (Field):
	def __init__(self, value):
		super().__init__(value)
		if not value:
			raise ValueError("Name cannot be empty!")

class Phone(Field):
	def __init__(self, value):
		super().__init__(value)
		if not value.isdigit() or len(value) != 10:
			raise ValueError("Phone number must be 10 digits.")

class Record:
	def __init__(self, name):
		self.name = Name(name)
		self.phones = []
	
	def __str__(self):
		phones_str = '; '.join(str(phone) for phone in self.phones)
		return f"Contact name: {self.name.value}, phones: {phones_str}"
	
	def add_phone(self, phone):
		self.phones.append(Phone(phone))
	
	def remove_phone(self, phone):
		self.phones = [phon for phon in self.phones if phon.value != phone]
	
	def edit_phone(self, old_phone, new_phone):
		for i, phone in enumerate(self.phones):
			if phone.value == old_phone:
				self.phones[i] = Phone(new_phone)
				return
		raise ValueError(f"Phone number {old_phone} not found!")
	
	def find_phone(self, phone):
		for p in self.phones:
			if p.value == phone:
				return p
		return None

class AddressBook(UserDict):
	def __init__(self):
		super().__init__()
	
	def __str__(self):
		return '\n'.join(str(record) for record in self.data.values())
	
	def add_record(self, record):
		self.data[record.name.value] = record
	
	def find(self, name):
		return self.data.get(name, None)
	
	def delete(self, name):
		if name in self.data:
			del self.data[name]
	
	def find_by_phone(self, phone):
		for record in self.data.values():
			for p in record.phones:
				if p.value == phone:
					return record
		return None



def input_error(func):
	@wraps(func)
	def inner(*args, **kwargs):
		try:
			return(func(*args, *kwargs))
		except ValueError:
			return "Error: Give me name and phone please."
		except KeyError:
			return "Error: Contact not found."
		except IndexError:
			return "Error: Insufficient arguments provided."
	return inner

@input_error
def parse_input(user_input):
	cmd, *args = user_input.split()
	cmd = cmd.strip().lower()
	return cmd, *args

@input_error
def add_contact(args, contacts):
	name, phone = args
	contacts[name] = phone
	return "Contacts added"

@input_error
def change_contact (args, contacts):
	name, new_phone = args
	if name in contacts:
		contacts[name] = new_phone
		return "Contact updated"
	else:
		return f"Error: Contact with name '{name}' not found."

@input_error
def show_phone (args, contacts):
	name = args [0]
	if name in contacts:
		return contacts[name]
	else:
		return f"Error: Contact with name '{name}' not found."

@input_error
def show_all (contacts):
	if not contacts:
		return "Contacts not found"
	
	result = []
	for name, phone in contacts.items():
		result.append(f"{name}: {phone}")
	
	return "\n".join(result)

def main ():
	contacts = {}
	print("Welcome to the assistant bot")
	while True:
		user_input = input("Enter a command: ")
		command, *args = parse_input(user_input)

		if command in ["close", "exit"]:
			print("Good bye!")
			break

		elif command == "hello":
			print("How can I help you?")
		
		elif command == "add":
			print(add_contact(args, contacts))

		elif command == "change":
			print(change_contact(args, contacts))
		
		elif command == "phone":
			print(show_phone(args, contacts))

		elif command == "all":
			print(show_all(contacts))

		else:
			print("Invalid command")

if __name__ == "__main__":
	main()