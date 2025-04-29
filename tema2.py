import json

# 1. Convertor de expresii regulate in notatie postfixata
def regex_to_postfix(regex):
    #inseram operatorul de concatenare . in expresie
    cuv = ""
    for i in range(len(regex) - 1):
        cuv += regex[i]
        if regex[i] not in "(|" and regex[i + 1] not in "|)*+?":
            cuv += "."
    cuv += regex[-1]
    return cuv

def verify():
    with open("tests.json") as fstream:
        tests = json.load(fstream)
    
    all_correct = True

    for test in tests:
        name = test['name']
        regex = test['regex']
        forma_postfix = regex_to_postfix(regex)

        print(f"Results for test {name} with regex {regex} :")
        print(forma_postfix)
        for string in test['test_strings']:
            input = string['input']
            expected = string['expected']
            print(input)
            print(expected)

        print()

verify()