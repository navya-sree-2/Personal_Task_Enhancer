# utils.py (create a new file if necessary) 
import random 
import string 
 
def generate_random_string(length=6): 
    letters_and_digits = string.ascii_letters + string.digits 
    return ''.join(random.choice(letters_and_digits) for i in range(length))