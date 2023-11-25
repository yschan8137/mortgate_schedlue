my_dict = {
    '1': 'one',
    '2': 'two',
}

# py -m unittest test.dict_test
if __name__ == '__main__':
    print(
        [my_dict[key] for key in ['1', '2']]
    )