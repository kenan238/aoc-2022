chrs = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}


def parse_input(input_str):
    return tuple(map(list, input_str.splitlines()))

def decimal(snafu: list[str]):
    if not snafu: return 0
    tail = snafu.pop()
    return 5 * decimal(snafu) + chrs[tail]

def snafu(dec: int):
    if not dec: return ''
    q, r = divmod(dec + 2, 5)
    return snafu(q) + '=-012'[r]



if __name__ == '__main__':
    snafus = parse_input(open("input.txt", "r").read())
    print(snafu(sum(map(decimal, snafus))))
