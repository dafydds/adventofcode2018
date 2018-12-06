with open('data/day1_input.txt', 'r')  as fp:
    lines = fp.readlines()
    
vals = [int(x) for x in lines]
print(sum(vals))

def get_repeated_value(vals):
    counts = {}
    current_value = 0
    counts[current_value] = 1
    break_while = False

    while True:
        for val in vals:
            current_value += val

            previous_counts = counts.get(current_value, 0)
            if (previous_counts > 0):
                return current_value
                break_while = True
                break
            counts[current_value] = 1
        if break_while:
            break
            
answer2 = get_repeated_value(vals)
print(answer2)



