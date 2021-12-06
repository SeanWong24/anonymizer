from typing import List, NamedTuple
from SimpleAnonymizer import AnonymizeText

TestCase = NamedTuple('Test', [('text', str), ('names', List[str])])

tests: List[TestCase] = [
    TestCase('Tom thinks this isn\'t a great idea. D/W.', ['Tom']),
    TestCase('Managed the resp distress, approp ddx, proper interp of ABG, Discussed disposition, tx', [
             'Someone']),
    TestCase('EPA completed by Dr. A. McConnell on ID rotation \r\nSubmitted on Oct 22 for week of Sept 4-7 \r\nNeeded to review the microbiology of the infection and characteristics of the appropriate antibiotic for the infection.',
             ['Grayson', 'Wilson', 'Lynsey', 'Martin'])
]
nicknames = {"richard": ['rick', 'ricky', 'richie', 'dick'],
             "stewart": ['stu'],
             "samuel": ['sam', 'sammy'],
             "elizabeth": ['elle', 'liz'],
             "jason": ['jay']
             }
for test in tests:
    text = test.text
    names = test.names
    result = AnonymizeText(text, names, nicknames)
    print(result)
