def assert_is_dict_contain_dict(dict1: dict, dict2: dict):
    for key, value in dict2.items():
        if key not in dict1:
            raise RuntimeError(f"Key {key} not in dict1")
        elif type(dict1[key]) == dict:
            if assert_is_dict_contain_dict(dict1[key], dict2[key]) == False:
                raise RuntimeError(f"Key {key} does not contain dict1")
        elif type(dict1[key]) == list:
            if assert_is_list_contain_list(dict1[key], dict2[key]) == False:
                raise RuntimeError(f"Key {key} does not contain dict1")
        elif dict1[key] != value:
            raise RuntimeError(
                f"Key {key}: dict1[key] != dict2[key], {dict1[key]} != {value}"
            )

    return True


def assert_is_list_contain_list(list1: list, list2: list):
    if len(list2) > len(list1):
        raise RuntimeError(f"list2 {list2} has more elements than list1 {list1}")
    for i in range(len(list2)):
        if type(list1[i]) == dict:
            if assert_is_dict_contain_dict(list1[i], list2[i]) == False:
                raise RuntimeError(f"List {list2} not in list1")
        elif type(list1[i]) == list:
            if assert_is_list_contain_list(list1[i], list2[i]) == False:
                raise RuntimeError(f"List {list2} not in list1")
        elif list1[i] != list2[i]:
            raise RuntimeError(f"List {list2} not in list1")
    return True
