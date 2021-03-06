import random
import time


class State:

    def __init__(self, input_map):
        self.state_map = dict()
        self.mario_loc = None
        self.possible_actions = []

        if input_map is not None:
            self.state_map = input_map
            self.bigH = 2147483647
            self.h = 2147483647
            key_list = list(self.state_map.keys())
            val_list = list(self.state_map.values())
            self.mario_loc = key_list[val_list.index('mario')]
            self.possible_actions_update()

    def big_h_update(self, amount):
        self.bigH = min(self.bigH, amount)

    def h_update(self, amount):
        self.h = min(self.h, amount)

    def possible_actions_update(self):
        self.possible_actions.clear()
        if self.mario_loc[0] != m and self.state_map.get((self.mario_loc[0] + 1, self.mario_loc[1])) != 'block':
            self.possible_actions.append('right')
        if self.mario_loc[1] != n and self.state_map.get((self.mario_loc[0], self.mario_loc[1] + 1)) != 'block':
            self.possible_actions.append('up')
        if self.mario_loc[0] != 1 and self.state_map.get((self.mario_loc[0] - 1, self.mario_loc[1])) != 'block':
            self.possible_actions.append('left')
        if self.mario_loc[1] != 1 and self.state_map.get((self.mario_loc[0], self.mario_loc[1] - 1)) != 'block':
            self.possible_actions.append('down')


def final_print():
    print('\n**********-----------------RESULT-----------------**********'
          '\nNumber of steps to reach both RED and BLUE Mushrooms: <<%i>>' % stepNums)
    print('------------------------------------------------------------')

    print('final amount of mushrooms:\nRED = %i , BLUE = %i' % (reds, blues))
    print('**********----------------------------------------**********')


def minimum_distance_heuristic(input_state):
    first_try = True
    min_dist = 2147483647
    for temp in input_state.state_map:
        if input_state.state_map.get(temp) == 'blue' or input_state.state_map.get(temp) == 'red':
            if first_try:
                min_dist = abs(temp[0] - input_state.mario_loc[0]) + abs(temp[1] - input_state.mario_loc[1])
            else:
                min_dist = min(min_dist,
                               abs(temp[0] - input_state.mario_loc[0]) + abs(temp[1] - input_state.mario_loc[1]))
                first_try = False
    return min_dist


def maximum_distance_heuristic(input_state):
    max_dist = -1
    for first in input_state.state_map:
        for second in input_state.state_map:
            if (input_state.state_map.get(first) == 'blue' or input_state.state_map.get(first) == 'red') and (
                    input_state.state_map.get(second) == 'blue' or input_state.state_map.get(second) == 'red'):
                max_dist = max(max_dist, abs(first[0] - second[0]) + abs(first[1] - second[1]))

    return max_dist


def lrta_star_cost(input_state):
    min_big_h = 2147483647
    found = False

    for temp_action in input_state.possible_actions:

        for temp_tuple in result:
            if temp_tuple[0].state_map == input_state.state_map and temp_tuple[1] == temp_action:
                found = True
                min_big_h = min(min_big_h, result.get(temp_tuple).bigH + step_cost)
                break

        if not found:
            min_big_h = min(min_big_h, input_state.h)

        found = False

    return min_big_h


def move(input_state):
    state = input_state
    ideal_action = ''
    minimum_cost = 2147483647
    found = False
    global reds
    global blues
    global redBool
    global blueBool
    global remaining

    # randomize possible actions for state in order not to choose repeated actions and not to stay in a loop
    actions = state.possible_actions.copy()
    random.shuffle(actions)

    # finding the best move with the least cost:
    for temp_action in actions:

        for temp_tuple in result:

            # repeated actions may have new cost amounts
            if temp_tuple[0].state_map == state.state_map and temp_tuple[1] == temp_action:
                found = True

                if ideal_action == '' or result.get(temp_tuple).bigH < minimum_cost:
                    ideal_action = temp_action
                    minimum_cost = min(minimum_cost, result.get(temp_tuple).bigH + step_cost)

                break

        # new actions cost the amount of H(state)
        if not found:
            if ideal_action == '' or state.bigH <= minimum_cost:
                ideal_action = temp_action
                minimum_cost = min(minimum_cost, state.h)

        found = False

    next_map = state.state_map.copy()
    next_mario_loc = tuple()
    next_state = State(next_map)
    # print('\ncurrent map ', next_state.state_map)
    # print('possible actions for current state ', next_state.possible_actions)

    if ideal_action == 'left':
        next_mario_loc = (state.mario_loc[0] - 1, state.mario_loc[1])
    if ideal_action == 'down':
        next_mario_loc = (state.mario_loc[0], state.mario_loc[1] - 1)
    if ideal_action == 'right':
        next_mario_loc = (state.mario_loc[0] + 1, state.mario_loc[1])
    if ideal_action == 'up':
        next_mario_loc = (state.mario_loc[0], state.mario_loc[1] + 1)

    # if the result of the chosen action is a BLOCK:
    if givenMap.get(next_mario_loc) == 'block':
        next_state.state_map[next_mario_loc] = 'block'

    # if the result of the chosen action is a MUSHROOM:
    elif state.state_map.get(next_mario_loc) == 'red' or state.state_map.get(next_mario_loc) == 'blue':

        remaining -= 1
        next_state.state_map[next_mario_loc] = 'mario'
        del next_state.state_map[state.mario_loc]
        next_state.mario_loc = next_mario_loc

        # if the mushroom is RED:
        if state.state_map.get(next_mario_loc) == 'red':
            redBool = True
            # global reds
            reds -= 1

        # if the mushroom is BLUE:
        else:
            blueBool = True
            # global blues
            blues -= 1

    # if the result of the chosen action is an EMPTY SPACE:
    else:
        next_state.state_map[next_mario_loc] = 'mario'
        del next_state.state_map[state.mario_loc]
        next_state.mario_loc = next_mario_loc

    # updates possible actions for this new state considering new map
    next_state.possible_actions_update()

    # print('\nminimum cost = %i  => ideal action = %s' % (minimum_cost, ideal_action))
    print('\nmario\'s loc: %s + "%s" => %s' % (state.mario_loc, ideal_action.upper(), next_state.mario_loc))
    # print('new map ', next_state.state_map)
    # print('new possible actions ', next_state.possible_actions)
    print('new amount of mushrooms:\nRED = %i , BLUE = %i' % (reds, blues))

    global current
    global last
    global last_is_None
    last = current
    current = next_state

    if heuristic_type == 1:
        current.h_update(remaining)
    elif heuristic_type == 2:
        current.h_update(minimum_distance_heuristic(current))
    elif heuristic_type == 3:
        current.h_update(maximum_distance_heuristic(current))

    last_is_None = False

    if not (redBool and blueBool):
        global stepNums
        stepNums += 1

    global action
    action = ideal_action


# start of program
# and it's in a loop in order to use the algorithm more than once and be able to use different possible heuristics
while True:

    # data input from file and defining parameters:
    f = open('/Users/apple/Desktop/Mario.txt')

    n = int(f.readline())
    m = int(f.readline())

    sc = list(f.readline().split())
    x, y = int(sc[0]), int(sc[1])

    k = int(f.readline())
    remaining = 2 * k
    reds = blues = k
    blueBool = redBool = False

    last_is_None = True
    last = State(None)

    step_cost = 1
    stepNums = 1
    action = ''

    result = dict()
    states = []

    givenMap = dict()
    givenMap[x, y] = 'mario'

    for i in range(k):
        sc = list(f.readline().split())
        givenMap[int(sc[0]), int(sc[1])] = 'red'
    for i in range(k):
        sc = list(f.readline().split())
        givenMap[int(sc[0]), int(sc[1])] = 'blue'

    for line in f:
        if line.strip() != '':
            sc = list(line.split())
            givenMap[int(sc[0]), int(sc[1])] = 'block'

    currentDict = dict()
    for key in givenMap.keys():
        if givenMap[key] == 'red' or givenMap[key] == 'blue' or givenMap[key] == 'mario':
            currentDict[key] = givenMap[key]

    current = State(currentDict.copy())

    print('\nGiven map: \n', givenMap)

    # selecting the heuristic for algorithm
    print('\n> Enter number of the heuristic you want to use:')
    print('  1 > NUMBER of REMAINING mushrooms')
    print('  2 > MINIMUM DISTANCE From remaining mushrooms')
    print('  3 > MAXIMUM DISTANCE Between remaining mushrooms')
    print('\n  >>> or print "end" in order to stop the program')

    while True:
        heuristic_type = input('\n> ')
        if heuristic_type == '1' or heuristic_type == '2' or heuristic_type == '3':
            heuristic_type = int(heuristic_type)
            break
        elif heuristic_type == 'end':
            exit()
        else:
            print('> choose from possible options please!')

    heuristic_str = ''
    if heuristic_type == 1:
        heuristic_str = 'REMAINING NUM'
    elif heuristic_type == 2:
        heuristic_str = 'MINIMUM  DIST'
    elif heuristic_type == 3:
        heuristic_str = 'MAXIMUM  DIST'
    print('\n------------------------------------------------------------------'
          '\n*** LRTA* algorithm using %s OF MUSHROOMS heuristic ***'
          '\n------------------------------------------------------------------' % heuristic_str)

    if heuristic_type == 1:
        current.h_update(remaining)
    elif heuristic_type == 2:
        current.h_update(minimum_distance_heuristic(current))
    elif heuristic_type == 3:
        current.h_update(maximum_distance_heuristic(current))

    # Run
    while True:

        if redBool and blueBool:
            final_print()
            time.sleep(1.7)
            break

        print('\n\nSTEP %i:\n------' % stepNums)

        # H(current state) update if current state is a NEW STATE:
        if not any(state.state_map == current.state_map for state in states):

            if heuristic_type == 1:
                current.big_h_update(remaining)
            elif heuristic_type == 2:
                current.big_h_update(minimum_distance_heuristic(current))
            elif heuristic_type == 3:
                current.big_h_update(maximum_distance_heuristic(current))

            print('H(current state) updated to: ', current.bigH)
            states.append(current)

        else:
            for state in states:
                if state.state_map == current.state_map:
                    current = state
                    print('H(current state) is: ', current.bigH)
                    break
            # print('H(current state) is: ', states[states.index(current)].bigH)

        # if last state is not null do 2 things:
        if not last_is_None:
            # 1) add the previous action( + its origin state and its destination state ) to results
            result[last, action] = current

            # 2) update H(last state) with minimum amount of relative states H (using LRTA*-Cost function)
            states[states.index(last)].big_h_update(lrta_star_cost(last))
            print('H(previous state) updated to: ', states[states.index(last)].bigH)
            print('number of states:', len(states))

        # take an action on current state:
        move(current)
