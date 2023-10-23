from random import Random

random = Random()


def generate_random_code(code_length):
    code = ''
    for i in range(code_length):
        code += str(random.randint(0, 9))
    return code