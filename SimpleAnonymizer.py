# import spellchecker
# from spellchecker import SpellChecker
import re

_nicknames = ['rick', 'ricky', 'richie', 'dick', 'stu', 'elle', 'liz', 'jay', 'kat', 'cat']
_ignore = ['i', 'you']

"""
Inputs:
Takes a word W

Returns:
Either the word W or an anonymized word

Function:
Works by check to see if W is a known pronoun

@todo The list should not really be hardcoded but should come from some external source?
"""


def AnonymizeWord_Pronoun(W):
    result = W

    if ((W == "he") or
            (W == "she") or
            (W == "him") or
            (W == "her") or
            (W == "his") or
            (W == "hers") or
            (W == "himself") or
            (W == "herself") or
            (W == "man") or
            (W == "woman") or
            (W == "men") or
            (W == "women") or
            (W == "boy") or
            (W == "girl") or
            (W == "mother") or
            (W == "father") or
            (W == "lady") or
            (W == "uncle") or
            (W == "aunt") or
            (W == "son") or
            (W == "daughter") or
            (W == "husband") or
            (W == "wife")):
        result = "PRONOUN"

    return result


"""
Inputs:
    W: A string. The word under consideration.

Returns:
    result: A string. Either the original word or the anonymized word

Function:
    Checks to see if the word is a known adjective that needs to be anonymized.
    Currently, this is "male" and "female".

@todo The list should not really be hardcoded but should come from some external source?    
"""


def AnonymizeWord_Adjective(W):
    result = W

    if ((W == "male") or
            (W == "female")):
        result = "ADJECTIVE"

    return result


"""
Inputs:
    W: A string. The word under consideration.

Returns:
    result: A string. Either the original word or the anonymized word

Function:
    Checks to see if the word is a known abbreviation.
    Currently, this is "m" (for male) and "f" (for female). However, other abbreviations may be added.

@todo The list should not really be hardcoded but should come from some external source?    
"""


def AnonymizeWord_Abbreviations(W):
    result = W

    if ((W == "m") or
            (W == "f")):
        result = "FLAGGED"

    return result


"""
Inputs:
    W: The word under consideration
    Name: A name of a person associated to the EPA record. Usually this will be either the resident or observer
    Note the name could be the first, last, or middle name

Returns:
    result: Either the original word W or the anonymized word

Function:
    Simply checks to see if the word is exactly the same as the first name or last name
"""


def AnonymizeWord_Name(W, Name):
    result = W

    if (W == Name):
        result = "NAME"

    return result


"""
Inputs:
    W: The word under consideration
    Name: A name of a person associated to the EPA record. Usually this will be either the resident or observer
    Note the name could be the first, last, or middle name

Returns:
    result: Either the original word W or the anonymized word

Function:
    Checks to see if the name is a known nickname stored in the global variable _nicknames (this was a property in the Java version)
    @todo Currently, this is a hardcoded list but it really should come from an external source
    @todo Also,it might be necessary to have nickname associated to a name. E.g., Ricky associated to Richard 
"""


def AnonymizeWord_NickName(W, Name):
    result = W
    found = False
    index = 0

    while (index < len(_nicknames)) and (not found):
        # seperated the check in case we want to return a different value for first and last name nicknames
        if (Name == _nicknames[index].lower()):
            result = "NICKNAME"
            found = True
        index = index + 1

    return result


"""
Inputs:
    W: A string. This is the word under consideration.
    Name: A string. This can be a first or last name.

Returns:
    result: A string. This is either the original word or the anonymized word

Functions:
    This function attempts to determine if a word is a nickname (or name) by applying a series of logical rules
    Each of the rules usually will set a flag, and then different combinations of flags are checked at the end.

    @todo We need a spellchecker for Python
"""


def AnonymizeWord_NameSubword(W, Name):
    result = W
    processing = W  # as the word is modified, this is used to prevent changing the original

    flagDone = False  # indicates if functioning should terminate
    flagPrefix = False  # track if the prefix matches a possible name / nickname
    flagSpelling = False  # tracks if the word is misspelled (currently not working, need a spellchecker)
    flagNotWord = False  # tracks if the word is not recognized  at all (currently not working, need a spellchecker)
    flagSuffix = False  # tracks if the  suffix is in general odd

    # does the word end in Y, I, K, etc.?
    flagSuffixY = False
    flagSuffixI = False
    flagSuffixK = False
    flagSuffixH = False
    flagSuffixIE = False
    flagSuffixCH = False
    flagSuffixKY = False
    flagSuffixHY = False

    # Need a Python based spellchecker to replace this Java code
    # pyspellchecker is too good, it recognizes names properly
    #    spell = SpellChecker()

    # find those words that may be misspelled
    #   misspelled = spell.unknown(['brent'])
    #   for word in misspelled:
    #      print(word + ": " + str(spell.candidates(word)))

    # if the name starts with the W, and W is not a word
    # currently not working, need spellchecker
    if (Name.find(W) == 0 and flagNotWord):
        result = "NICKNAME?"
        flagPrefix = True
        flagDone = True

    # if the name starts with the W
    if (Name.find(W) == 0):
        result = "FLAGGED"
        flagPrefix = True
        flagDone = True

    if (not flagDone):
        # does the word end in y or i or ie
        # if so strip it off
        if (processing.endswith("y")):
            flagSuffixY = True;
            flagSuffix = True;
            processing = processing[0:len(processing) - 1]
        elif (processing.endswith("i")):
            flagSuffixI = True
            flagSuffix = True;
            processing = processing[0:len(processing) - 1]
        elif (processing.endswith("k")):
            flagSuffixK = True
            flagSuffix = True
            processing = processing[0:len(processing) - 1]
        elif (processing.endswith("h")):
            flagSuffixH = True
            flagSuffix = True
            processing = processing[0:len(processing) - 1]

        # check to see if the original word has the processing string as a prefix
        # if so it is a likely nickname
        if (flagSuffix and Name.startswith(processing)):
            result = "NICKNAME?"
            flagPrefix = True

        # if this is not already flagged, then take a look at strange two letter endings
        # reset the processing string
        processing = W
        if (not flagPrefix):
            if (processing.endswith("ie")):
                flagSuffixIE = True
                flagSuffix = True
                processing = processing[0:len(processing) - 2]
            elif (processing.endswith("ch")):
                flagSuffixCH = True
                flagSuffix = True
                processing = processing[0:len(processing) - 2]
            elif (processing.endswith("ky")):
                flagSuffixKY = True
                flagSuffix = True
                processing = processing[0:len(processing) - 2]
            elif (processing.endswith("hy")):
                flagSuffixHY = True
                flagSuffix = True
                processing = processing[0:len(processing) - 2]

            # if after removing the ending the word matches the name
            if (flagSuffix and Name.startswith(processing)):
                result = "NICKNAME?"
                flagPrefix = True

    # this word has a strange suffix, flag it
    if (not flagPrefix and (flagSuffixIE or flagSuffixI or flagSuffixKY)):
        result = "FLAGGED"

    # this isn't a word and it has a strange ending
    if (flagNotWord and flagSuffix):
        result = "FLAGGED"

    return result


def AnonymizeWord_Flag(W, F):
    result = W

    if (F):
        result = "FLAGGED"

    return result


"""
DEPRECATED - Replaced with a new version that takes an array of names
Inputs:
    String W: The current word under consideration
    String FirstNameR: The resident's first name
    String LastNameR: The resident's last name
    String FirstNameO: The observer's first name
    String LastNameO: The observer's last name
    Boolean F: A flag that indicates the previous word was unusual

Returns:
    String: the word W or the anonymized word

AnonymizeWord functions by calling several other functions to do the actual work of anonymization.
Think of it as a collection of rules to be applied.
def AnonymizeWord(W, FirstNameR, LastNameR, FirstNameO, LastNameO, F):
    # make sure everything is in lowercase in local copies
    result = W.lower()
    _FirstNameR = FirstNameR.lower();
    _LastNameR = LastNameR.lower();
    _FirstNameO = FirstNameO.lower();
    _LastNameO = LastNameO.lower();

    # for each rule first check to see if the word has already changed, if it is already changed then do not run anymore rules
#    print(result)
    result = AnonymizeWord_Pronoun(result)
#    print(result)

    if (result == W.lower()):
        result = AnonymizeWord_Adjective(result)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_Abbreviations(result)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_Name(result, _FirstNameR, _LastNameR)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_Name(result, _FirstNameO, _LastNameO)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_NickName(result, _FirstNameR, _LastNameR)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_NickName(result, _FirstNameO, _LastNameO)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_NameSubword(result, _FirstNameR)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_NameSubword(result, _LastNameR)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_NameSubword(result, _FirstNameO)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_NameSubword(result, _LastNameO)
        #print(result)

    if (result == W.lower()):
        result = AnonymizeWord_Flag(result, F)
        #print(result)

    return result
"""

"""
Inputs:
    String W: The current word under consideration
    Array[String] Names: The array of names to consider
    Boolean F: A flag that indicates the previous word was unusual

Returns:
    String: the word W or the anonymized word

AnonymizeWord functions by calling several other functions to do the actual work of anonymization.
Think of it as a collection of rules to be applied.
"""


def AnonymizeWord(W, Names, F):
    # make sure everything is in lowercase in local copies
    result = W.lower()
    regex = re.compile('[^a-zA-Z0-9\s]')
    # First parameter is the replacement, second parameter is your input string
    result = regex.sub('', result)

    index = 0
    ignore = False
    while (index < len(_ignore)) and (not ignore):
        # seperated the check in case we want to return a different value for first and last name nicknames
        if (W == _ignore[index].lower()):
            ignore = True
        index = index + 1

    if (not ignore):
        # for each rule first check to see if the word has already changed, if it is already changed then do not run anymore rules
        #    print(result)
        result = AnonymizeWord_Pronoun(result)
        #    print(result)

        if (result == W.lower()):
            result = AnonymizeWord_Adjective(result)
            # print(result)

        if (result == W.lower()):
            result = AnonymizeWord_Abbreviations(result)
            # print(result)

        for name in Names:
            _name = name.lower();
            if (result == W.lower()):
                result = AnonymizeWord_Name(result, _name)
                # print(result)

            if (result == W.lower()):
                result = AnonymizeWord_NickName(result, _name)
                # print(result)

            if (result == W.lower()):
                result = AnonymizeWord_NameSubword(result, _name)
                # print(result)

        if (result == W.lower()):
            result = AnonymizeWord_Flag(result, F)
            # print(result)

        if (result == W.lower()):
            result = None

    return result


"""
Inputs:
    String W: The current word under consideration
    Boolean F: A flag that indicates the previous word was unusual

Returns:
    Boolean: Return an anonymization flag

SetAnonFlag takes the word and determines if it is a title. If so then the next word should be anonymized. Also, if the word is an initial then the next word should also be anonymized.
"""
def SetAnonFlag(W, F):
    result = False
    processing = W.lower();

    if ((processing == "doctor") or
            (processing == "dr") or
            (processing == "mister") or
            (processing == "miss") or
            (processing == "mr") or
            (processing == "ms") or
            (processing == "mrs")):
        result = True
    elif (F == True and len(W) == 1):
        # if the flag is set and
        # the word is one character long (an initial) then flag the next word as well
        result = True

    return result


def Test():
    samples = ['Grayson as discussed Dr. A Henderson think you need to work on strategies to help you ensure',
               'that you are completing full reassessments including being aware of what results',
               'or tests that you have ordered are still outstanding.    You also would improve by',
               'being more mindful of timing to reassess patients.    Your patient care was very EB',
               'and you are quite good at accessing relevant guidelines and critically thinking',
               'your way through them as they would apply to your particular patient.']
    for sample in samples:
        regex = re.compile('[^a-zA-Z0-9\s]')
        # First parameter is the replacement, second parameter is your input string
        sample = regex.sub('', sample)
        words = sample.split()
        names = ['Grayson', 'Wilson', 'Joanna', 'Smith']
        flag = False

        for w in words:
            w = w.lower()
            index = 0
            ignore = False
            while (index < len(_ignore)) and (not ignore):
                # seperated the check in case we want to return a different value for first and last name nicknames
                if (w == _ignore[index].lower()):
                    ignore = True
                index = index + 1

            if (not ignore):
                result = AnonymizeWord(w, names, flag)
                flag = SetAnonFlag(w, flag)
                result = "None" if result is None else result
                print("word = " + w + ", result = " + result + ", flag = " + str(flag))


result = ""
flag = False

# comment this out when the test is not needed
# Test()

#print("done")