import os, base64, requests
from plaid import Client
from plaid.errors import *

PLAID_ENVIRONMENT = "sandbox" # sandbox || development || production
PLAID_PUBLIC_KEY = "b9830e8e5309d7512fe8597e386935"
PLAID_CLIENT_ID_FILE_B64 = "secrets/plaidclientidb64.txt"
PLAID_SECRET_KEY_FILE_B64 = "secrets/plaidsecretkeyb64.txt"

BOFA_USERNAME_FILE_B64 = "secrets/bofausernameb64.txt"
BOFA_PASSWORD_FILE_B64 = "secrets/bofapassb64.txt"

# UTIL CLASS
class Util:
    #def __init__(self):

    """Read a (in this case Plaid key/id) secret from secret_key_file. If this
    file is base-64 encoded, set is_base_64 to True. Returns the text retrieved
    as a string.
    """
    def get_secret(self, secret_key_file, is_base_64 = False):
        if not os.path.exists(secret_key_file):
            print("There's no secret key file at \'" +
                  str(secret_key_file) + "\' you STUPID IDIOT")
            return None

        with open(secret_key_file, 'rb'
                  if is_base_64 else 'r') as secret_key_file:
            file_text = secret_key_file.read()
            secret_key_file.close()

            if is_base_64:
                return base64.decodebytes(file_text).decode()
            else:
                return file_text

    """Read a text file with standard encoding, and write the text file to
    to_file base 64 encoded. Returns True on success or False on failure.
    """
    def make_base64_text_file_from_standard_file(self, from_file, to_file):
        if not os.path.exists(from_file):
            print(str(from_file) + " doesn't exist you STUPID IDIOT. Failed" +
                  " to base 64 encode.")
            return False

        from_file = open(from_file, 'r')
        to_file = open(to_file, 'wb')
        
        standard_text = from_file.read()
        to_file.write(base64.b64encode(standard_text.encode()))

        from_file.close()
        to_file.close()
        
        return True
        
        
if __name__ == "__main__":
    util = Util()
    #util.make_base64_text_file_from_standard_file("bofapass.txt", "bofapassb64.txt")
    #print(util.get_secret(PLAID_CLIENT_ID_FILE, True))
    #print(util.get_secret("plaidsecretkey.txt"))
    plaid_client_id = util.get_secret(PLAID_CLIENT_ID_FILE_B64, True)
    plaid_secret_key = util.get_secret(PLAID_SECRET_KEY_FILE_B64, True)
    bofa_username = util.get_secret(BOFA_USERNAME_FILE_B64, True)
    bofa_password = util.get_secret(BOFA_PASSWORD_FILE_B64, True)
    plaid_client = Client(plaid_client_id, plaid_secret_key, PLAID_PUBLIC_KEY, PLAID_ENVIRONMENT)
    try:
        """
        client.Item.create(
            credentials=dict(username='user_good', password='pass_good'),
            institution_id='ins_109508',
            initial_products=['transactions', 'auth'],
            webhook='https://example.com/webhook');
        """
        print("attempting to create new item")
        ret = plaid_client.Item.create(
            credentials = dict(username = bofa_username, password = bofa_password),
            institution_id='ins_1',
            initial_products=['transactions', 'auth'],
            webhook='https://example.com/webhook')
        print(str(ret))
    except APIError as api_err:
        print("Plaid API error: " + str(api_err))
    except InvalidInputError as invalid_input_err:
        print("Plaid API error: " + str(invalid_input_err))
