#
#
# def censor(description, str):
#     s = ['редиска']
#     for i in s:
#         n = ' ' + i[0] + '*' * (len(i) - 1) + ' '
#         value = description.replace(i, n)
#     return description
#
# print(censor('редиска нехороший человек', str))

def censor(value):
    """
    The function replaces bad words specified in the list a[].
    Example: 'хрен' ->> 'x***'
    """
    if isinstance(value, str):
        a = ['хрен', 'редиска', 'тыква']
        for i in a:
            b = ' '+i[0]+'*' * (len(i)-1)+' '
            value = value.replace(i, b)
    return value