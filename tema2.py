import json

def regex_to_postfix(regex):
    cuv = ""
    for i in range(len(regex) - 1):
        cuv += regex[i]
        if regex[i] not in "(|" and regex[i + 1] not in "|)*+?":
            cuv += '.'
    cuv += regex[-1]
    regex = cuv

    precedence = {'|' : 1, '.' : 2, '*' : 3, '+' : 3, '?' : 3}
    st = []
    rez = []

    for ch in regex:
        if ch.isalnum():
            rez.append(ch)
        elif ch == '(':
            st.append(ch)
        elif ch == ')':
            while len(st) > 0 and st[-1] != '(':
                rez.append(st.pop())
            st.pop()
        else:
            while (len(st) > 0 and st[-1] != '(' 
                   and precedence[ch] < precedence.get(st[-1], 0)):
                rez.append(st.pop())
            st.append(ch)

    while len(st) > 0:
        rez.append(st.pop())

    return rez

def thompson(forma_postfix):
    state_cnt = 0
    alphabet = set()

    def new_state():
        nonlocal state_cnt
        state = f"q{state_cnt}"
        state_cnt += 1
        return state

    stack = []

    for ch in forma_postfix:
        if ch.isalnum():
            alphabet.add(ch)
            start = new_state()
            end = new_state()
            start_state = {'transitions': {ch: {end}}, 'eps': set()}
            end_state = {'transitions': {}, 'eps': set()}
            nfa = {'states': {start, end}, 'start': start, 'accepts': {end}, 'transitions': {start: start_state, end: end_state}}
            stack.append(nfa)
        elif ch == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            for state in nfa1['accepts']:
                nfa1['transitions'][state]['eps'].add(nfa2['start'])
            nfa1['states'].update(nfa2['states'])
            nfa1['accepts'] = nfa2['accepts']
            nfa1['transitions'].update(nfa2['transitions'])
            stack.append(nfa1)
        elif ch == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = new_state()
            end = new_state()
            start_state = {'transitions': {}, 'eps': {nfa1['start'], nfa2['start']}}
            end_state = {'transitions': {}, 'eps': set()}
            for state in nfa1['accepts']:
                nfa1['transitions'][state]['eps'].add(end)
            for state in nfa2['accepts']:
                nfa2['transitions'][state]['eps'].add(end)
            all_states = nfa1['states'] | nfa2['states'] | {start, end}
            all_trans = {**nfa1['transitions'], **nfa2['transitions'], start: start_state, end: end_state}
            stack.append({'states': all_states, 'start': start, 'accepts': {end}, 'transitions': all_trans})
        elif ch == '*':
            nfa = stack.pop()
            start = new_state()
            end = new_state()
            start_state = {'transitions': {}, 'eps': {nfa['start'], end}}
            end_state = {'transitions': {}, 'eps': set()}
            for state in nfa['accepts']:
                nfa['transitions'][state]['eps'].update({nfa['start'], end})
            all_states = nfa['states'] | {start, end}
            nfa['transitions'][start] = start_state
            nfa['transitions'][end] = end_state
            stack.append({'states': all_states, 'start': start, 'accepts': {end}, 'transitions': nfa['transitions']})
        elif ch == '+':
            nfa = stack.pop()
            start = new_state()
            end = new_state()
            start_state = {'transitions': {}, 'eps': {nfa['start']}}
            end_state = {'transitions': {}, 'eps': set()}
            for state in nfa['accepts']:
                nfa['transitions'][state]['eps'].update({nfa['start'], end})
            all_states = nfa['states'] | {start, end}
            nfa['transitions'][start] = start_state
            nfa['transitions'][end] = end_state
            stack.append({'states': all_states, 'start': start, 'accepts': {end}, 'transitions': nfa['transitions']})
        elif ch == '?':
            nfa = stack.pop()
            start = new_state()
            end = new_state()
            start_state = {'transitions': {}, 'eps': {nfa['start'], end}}
            end_state = {'transitions': {}, 'eps': set()}
            for state in nfa['accepts']:
                nfa['transitions'][state]['eps'].add(end)
            all_states = nfa['states'] | {start, end}
            nfa['transitions'][start] = start_state
            nfa['transitions'][end] = end_state
            stack.append({'states': all_states, 'start': start, 'accepts': {end}, 'transitions': nfa['transitions']})

    result_nfa = stack.pop()
    result_nfa['alphabet'] = sorted(alphabet)
    return result_nfa

def convert_nfa_to_dfa(nfa):
    alphabet = nfa["alphabet"]
    transitions = nfa["transitions"]
    start = nfa["start"]
    accept = nfa["accepts"]

    def epsilon_closure(states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in transitions.get(state, {}).get('eps', set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    dfa_start = frozenset(epsilon_closure([start]))
    dfa_states = []
    dfa_transitions = {}
    dfa_accept = set()
    unprocessed = [dfa_start]

    while unprocessed:
        current = unprocessed.pop(0)
        if current not in dfa_states:
            dfa_states.append(current)
        if any(state in accept for state in current):
            dfa_accept.add(current)
        for symbol in alphabet:
            next_state = set()
            for state in current:
                if symbol in transitions.get(state, {}).get('transitions', {}):
                    targets = transitions[state]['transitions'][symbol]
                    for target in targets:
                        next_state.update(epsilon_closure([target]))
            if not next_state:
                continue
            next_state_frozen = frozenset(next_state)
            dfa_transitions.setdefault(current, {})[symbol] = next_state_frozen
            if next_state_frozen not in dfa_states and next_state_frozen not in unprocessed:
                unprocessed.append(next_state_frozen)

    return {
        "states": dfa_states,
        "alphabet": alphabet,
        "transitions": dfa_transitions,
        "start": dfa_start,
        "accept": dfa_accept
    }

def acceptare_dfa(dfa, line):
    Transitions = dfa["transitions"]
    q0 = dfa["start"]
    F = dfa["accept"]

    stare_curenta = q0
    for ch in line.strip():
        if stare_curenta not in Transitions or ch not in Transitions[stare_curenta]:
            return False
        stare_curenta = Transitions[stare_curenta][ch]

    return stare_curenta in F


def verify():
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    with open("tests.json") as fstream:
        tests = json.load(fstream)

    all_correct = True

    for test in tests:
        name = test['name']
        regex = test['regex']
        forma_postfix = regex_to_postfix(regex)
        nfa = thompson(forma_postfix)
        dfa = convert_nfa_to_dfa(nfa)

        print(f"Rezultate test {name} cu regex {regex} :")
        for string in test['test_strings']:
            input = string['input']
            expected = string['expected']
            rez = acceptare_dfa(dfa, input)
            if expected == rez:
                print(f"Pentru string-ul {input} trebuia sa obtinem {expected} si am obtinut {rez} -> {GREEN}PASS{RESET}")
            else:
                print(f"Pentru string-ul {input} trebuia sa obtinem {expected} si am obtinut {rez} -> {RED}FAIL{RESET}")
        print()

verify()
