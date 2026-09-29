positive_lookbehind_open_parenthesis = r'(?<=\()'
positive_lookahead_closing_parenthesis = r'(?=\))'

# В шаблоне используется {{}}, чтобы оставить место для подстановки параметра.
parentheses_lookarounds = '{}{{}}{}'.format(positive_lookbehind_open_parenthesis,
                                            positive_lookahead_closing_parenthesis)
