from pprint import pprint
import re
import csv



def read_csv(filename):
    """Read data from file"""
    with open(filename, encoding="utf-8") as f:
       rows = csv.reader(f, delimiter=",")
       contacts_list = list(rows)

    return contacts_list
       

def save_to_csv(filename, data):
   """Write data to file"""
   with open(filename, "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(data)


def fix_names(data):
    '''Fix name structure'''
    transformed_data = []
    for item in data:
       name_parts = ' '.join(item[:3]).strip().split(' ')  # Join first, middle and last names and strip spaces
       name_parts = [part for part in name_parts if part]  # Remove empty strings
       transformed_item = name_parts + item[len(name_parts):]  # Create new list with name and other data
       transformed_data.append(transformed_item)  # Add new list to the main list
    return transformed_data 


def unique_names(data):
    '''Find unique names'''
    unique_names_list = []  # Create an empty list
    unique_names = {}  # Create an empty dictionary

    # Go through the list without the first line 
    for names in data[1:]: 
        key = (names[0], names[1])  # Create a key with the first and second name
        if key not in unique_names:  
            unique_names[key] = names  # If the key is not in the dictionary, add elements to the dictionary
        else:
            # Go through the rest of the names
            for i in range(2, len(names)):  
                # If the name is not empty
                if names[i] != '':
                    unique_names[key][i] = names[i]  # Add the name to the dictionary

    into_list = list(unique_names.values())  # Create a list with unique names
    into_list.insert(0, data[0])  # Add the first line
    
    # Return all data into a list
    for item in into_list:
       unique_names_list.append(item) 

    return unique_names_list


def format_phone_number(phone):
    """Format phone numbers to the desired pattern"""
    pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*(доб\.)\s*(\d+))?")  # Create a regular expression pattern
    match = pattern.search(phone)  # Search for the pattern in the phone number
    if match:
        formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(7):
            formatted_phone += f" доб.{match.group(7)}"
        return formatted_phone
    return phone


def fix_phone_numbers(data):
    """Fix the phone numbers in the contact list"""
    for contact in data:  # Go through the list
        contact[5] = format_phone_number(contact[5])  # Replace the old phone number with the new one
    return data


def main():
    """Call all functions"""
    data = read_csv("/file_storage/homework_rep/regular/phonebook_raw.csv")
    fix_data = fix_names(data)
    unique_data = unique_names(fix_data)
    save_to_csv("/file_storage/homework_rep/regular/phonebook.csv", fix_phone_numbers(unique_data))

if __name__ == "__main__":
    main()



