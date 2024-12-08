#Frequently used Constants
YES_ANSWER=["Yes","YEs","YES","yEs","yES","yeS","yes","Y","y",1,"1"]
NO_ANSWER=["NO","No","nO","no","N","n",2,"2"]
CANCEL_ANSWER = ["Cancel","cancel","CANCEL","c","C",3,"3"]

# -------------------------------------------------------------------------------------------------
# Check if a number is within a range
def within_range(num, minimum=None, maximum=None):
    """
    Function - within_range
        Checks whether a value is within a range of values
    Parameters:
        num - the number to check (None will always return false)
        minimum - The minimum value (None is no minimum)
        maximum - The maximum value (None is no maximum)
    """
    if num is None:
        return False

    if (minimum is None or num >= minimum) and (maximum is None or num <= maximum):
        return True

    return False

# -------------------------------------------------------------------------------------------------
def validate_integer(text,n_min=None,n_max=None):
    """
        Function validate_integer
            Verify input is a valid integer and return a dictionary with details
        Parameters:
            text - Text to validate
            n_min - (Optional) Minimum acceptable value
            n_max - (Optional) Maximum acceptable value
        Returns:
            Dictionary - is_valid, error, message
            is_valid - True/False (Valid/Invalid)
            error - if invalid, reason why
            message - Message to user
            value - cast value
    """
    result = {
        "is_valid":False,
        "error":"",
        "message":""
    } #Variable to store results of validation

    try:
        num = int(text)     #Attempt to cast to integer (Throws exception if fails)
        result.update({"value": num})   #Update return value
        # If cast was successful, check if within range:
        if within_range(num, n_min, n_max):
            result.update({"is_valid": True})      #True if within specified range

        else:
            #If out of range, create error messages and store to dictionary
            result.update({"is_valid": False, "error": "Out of range"})
            err_message = ""    #Variable to store the error message
            if n_min is not None:
                err_message += f"The number cannot be less than {n_min}. "
            if n_max is not None:
                err_message += f"\nThe number cannot be more than {n_max}. "
            result.update({"message": err_message})

    except ValueError:
        result.update({
                "value": 0,
                "is_valid":False,
                "error": "Type error",
                "message": "Please enter a valid integer value."
                          " No decimals, fractions, letters, "
                          "or special characters."
                       })
    finally:
        if result["is_valid"] is False:
            result["message"] += "\nTry again.\n"
        else:
            result["message"] += "\nThank you.\n"

        return result
# -------------------------------------------------------------------------------------------------
def validate_float(text, n_min=None, n_max=None):
    """
        Function validate_float
            Verify input is a valid floating point value and return a dictionary with details
        Parameters:
            text - Text to validate
            n_min - (Optional) Minimum acceptable value
            n_max - (Optional) Maximum acceptable value
        Returns:
            Dictionary - is_valid, error, message
            is_valid - True/False (Valid/Invalid)
            error - if invalid, reason why
            message - Message to user
            value - cast value
    """
    result = {
        "value":0,
        "is_valid": False,
        "error": "",
        "message": ""
    }  # Variable to store results of validation

    try:
        num = float(text)  # Attempt to cast to float (Throws exception if fails)
        result.update({"value": num})  # Update return value
        # If cast was successful, check if within range:
        if within_range(num, n_min, n_max):
            result.update({"is_valid": True})  # True if within specified range

        else:
            # If out of range, create error messages and store to dictionary
            result.update({"is_valid": False, "error": "Out of range"})
            err_message = ""  # Variable to store the error message
            if n_min is not None:
                err_message += f"The number cannot be less than {n_min}. "
            if n_max is not None:
                err_message += f"\nThe number cannot be more than {n_max}. "
            result.update({"message": err_message})

    except ValueError:
        #Triggers if user enters a value that does not meet format
        #Update result
        result.update({
            "value":0,
            "is_valid": False,
            "error": "Type error",
            "message": "Please enter a valid floating point value. No letters, or special characters."
        })
    finally:
        "Set final message"
        if result["is_valid"] is False:
            result["message"] += "\nTry again.\n"
        else:
            result["message"] += "\nThank you.\n"

        #Return result
        return result

# -------------------------------------------------------------------------------------------------
def validate_string(text,valid_list=(),invalid_list=()):
    """
        Function validate_string
            Verify input is a valid string and return a dictionary with details
            Note - does not return original input
        Parameters:
            text - Text to validate
            valid_list - (Optional) List of allowed values
            invalid_list - (Optional) List of invalid values
        Returns:
            Dictionary - is_valid, error, message
            is_valid - True/False (Valid/Invalid)
            error - if invalid, reason why
            message - Message to user
            value - returned value
    """
    result = {
        "value":text,
        "is_valid": True,   #Assume valid
        "error": "",
        "message": "Thank you."
    }  # Variable to store results of validation

    # if a list of valid strings has been specified:
    if len(valid_list) > 0:
        # Cycle through list for valid input values:
        for valid_text in valid_list:
            #Default to false if a list exists
            result.update({
                "is_valid": False,
                "error": "Not allowed",
                "message": "Invalid entry"
            })
            if text == valid_text:
                # If found on list, break out and set validate to true
                result.update({
                    "is_valid": True,
                    "error": "",
                    "message": "Thank you"
                })
                break


    # If there is an invalid list and the text hasn't already been marked as invalid:
    if len(invalid_list) > 0 and result["is_valid"]==True:
        # Cycle through invalid list for non-valid input values:
        for invalid_text in invalid_list:
            if text == invalid_text:
                # If found on list, break out and set validate to false
                err_message=""
                if text =="":
                    #Special error message for empty text
                    err_message = "Text cannot be blank."
                else:
                    #Error message if text found on list
                    err_message = "The text you entered is not allowed"

                #Update result
                result.update({
                    "is_valid": False,
                    "error": "Not allowed",
                    "message": err_message
                })
                break
    #Return result
    return result
# -------------------------------------------------------------------------------------------------
def validate_phone(text):
    """
        Function validate_phone
            Verify input is a valid phone number format and return a dictionary with details
            Note - does not return original input
        Parameters:
            text - Text to validate
        Returns:
            Dictionary - is_valid, error, message
            is_valid - True/False (Valid/Invalid)
            error - if invalid, reason why
            message - Message to user
    """
    from re import match        #Library needed for regex

    #Regex pattern for phone number with or without dashes, but no letters
    regex_pattern = (r"^(1-?)?(\(\d{3}\)|\d{3})-?\d{3}-?\d{4}$|^(1-?)?(\(\d{3}\)|\d{3})-?\d{3}-?\d{4}$"
                     r"|^(1-?)?(\(\d{3}\)|\d{3})?\d{3}-?\d{4}$|^(1-?)?(\(\d{3}\)|\d{3}) ?\d{7}$")

    result = {
        "value":text,
        "is_valid": False,   #Assume valid
        "error": "",
        "message": ""
    }  # Variable to store results of validation

    #Regex evaluation of text:
    if match(regex_pattern,text):
        #Match:
        result.update({
            "is_valid":True,
            "error": "",
            "message": "Thank you."
        })
    else:
        #Fail:
        result.update({
            "is_valid": False,
            "error": "Invalid",
            "message": "Invalid phone number format."
        })
    #Return result
    return result

# -------------------------------------------------------------------------------------------------
def validate_email(text):
    """
        Function validate_email
            Verify input is a valid email format and return a dictionary with details
            Note - does not return original input
        Parameters:
            text - Text to validate
        Returns:
            Dictionary - is_valid, error, message
            is_valid - True/False (Valid/Invalid)
            error - if invalid, reason why
            message - Message to user
    """
    from re import match        #Library needed for regex
    #Regex pattern for email:
    regex_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+[.][A-Za-z.]{2,}$"

    result = {
        "value":text,
        "is_valid": False,   #Assume valid
        "error": "",
        "message": ""
    }  # Variable to store results of validation

    #Regex evaluation:
    if match(regex_pattern,text):
        #Match
        result.update({
            "is_valid":True,
            "error": "",
            "message": "Thank you."
        })
    else:
        #Fail
        result.update({
            "is_valid": False,
            "error": "Invalid",
            "message": "Invalid email format."
        })
    return result

# -------------------------------------------------------------------------------------------------
def get_user_input(*, message="", in_type="string", valid_list=(), invalid_list=(), n_min=None, n_max=None, is_test=False, test_input="0"):
    """
    Function - get_user_input
        Validate user input by type
    Parameters:
        message - a valid string to display to the user
        in_type - determine the type of input validation("float","string", "integer", "phone", "email")
        valid_list - a list of valid values that user is allowed to input (Applies only to strings)
        invalid_list - a list of invalid values that user is not allowed to input (Applies only to strings)
        n_min - minimum integer or float value allowed
        n_max - maximum integer or float value allowed
        is_test - (Boolean) used for testing only
        test_input - used for testing only
    Returns:
        user input in specified type (float, integer, string)
    """
    #Declare Variables:
    valid_input = False     #Boolean to test for valid input
    user_input = ""         #Stores user input
    INVALID_TEST_OUTPUT = "__invalid__"  #Invalid message for testing

    #Add a >> to the prompt to distinguish it from other text on screen
    message = " >> " + message
    res={}

    #Will continually ask for user input until valid response is received
    while not valid_input:
        if is_test:
            # While testing will use test_input for validation
            user_input = test_input
        else:
            # Get user input if not test
            user_input = input(message)

        #For each input type a different validation method is needed:
        #Will call the appropriate function depending on in_type
        if in_type=="integer":
            res = validate_integer(user_input,n_min,n_max)
            print (res["message"])
            valid_input=res["is_valid"]
        elif in_type=="float":
            res = validate_float(user_input,n_min,n_max)
            print (res["message"])
            valid_input=res["is_valid"]
        elif in_type=="string":
            res = validate_string(user_input,valid_list,invalid_list)
            print (res["message"])
            valid_input=res["is_valid"]
        elif in_type=="phone":
            res = validate_phone(user_input)
            print (res["message"])
            valid_input=res["is_valid"]
        elif in_type=="email":
            res = validate_email(user_input)
            print (res["message"])
            valid_input=res["is_valid"]

        else:
            #If in_type is not a recognized type, test will automatically pass
            valid_input=True

        #If testing and invalid, return invalid response
        if is_test and not valid_input:
            return INVALID_TEST_OUTPUT

    #Return user input if validation passes:
    return res["value"]

# -------------------------------------------------------------------------------------------------
def main():
    x=get_user_input(in_type="email",n_max=100, n_min=1,message="Enter value: ", valid_list=["yes","no","y","n"])
    print(x)

if __name__ == "__main__":
    main()