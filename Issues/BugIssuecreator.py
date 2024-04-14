import datetime

def count_bugs(filename):
    with open(filename, 'r') as file:
        return sum(1 for line in file if line.startswith('Bug'))

def add_bug_report(filename, bug_desc, resolved):
    bug_number = count_bugs(filename) + 1
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a') as file:
        file.write('--------------------------------\n')
        file.write(f'Bug{bug_number}\n')
        file.write(f'Description: {bug_desc}\n')
        file.write(f'Date of Notice: {current_time}\n')
        file.write(f'Resolved: {resolved}\n')
        file.write('--------------------------------\n\n')

# Example usage:
bug_desc = input("Description: ")
resolved = input("Resolved? (YES/NO): ")

add_bug_report('Issues\\bugs.txt', bug_desc, resolved.upper())
