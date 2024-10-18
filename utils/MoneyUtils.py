import re

class MoneyUtils(object):

    @staticmethod
    def text_has_money(test_string: str):
        format_pattern = r'^\$([0-9]{1,3}(?:,[0-9]{3})*)?(?:\.[0-9]{1,2})?$|^\d+\s(dollars|USD)$'
        has_money = False
        for string in test_string:
            if re.match(format_pattern, string):
                has_money = True
                break

        return has_money