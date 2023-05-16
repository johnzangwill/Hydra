class Ordinal:
    def __init__(self, *args):
        self.terms = []

        powers = sorted(args, reverse=True)
        for power in powers:
            if len(self.terms) > 0:
                lastcount, lastpower = self.terms[-1]
                if lastpower.is_equal(power):
                    self.terms[-1][0] += 1
                else:
                    self.terms.append([1, power])
            else:
                self.terms.append([1, power])

    def __str__(self):
        if self.terms:
            return '+'.join(Ordinal._to_string(count, power) for count, power in self.terms)
        else:
            return '0'

    def __lt__(self, ordinal):
        return self.compare(ordinal) < 0

    def is_zero(self):
        return len(self.terms) == 0

    def is_one(self):
        if len(self.terms) == 1:
            count, power = self.terms[0]
            if count == 1 and power.is_zero():
                return True
        return False

    def is_equal(self, ordinal):
        if len(self.terms) != len(ordinal.terms):
            return False
        
        for (count1, power1), (count2, power2) in zip(self.terms, ordinal.terms):
            if count1 != count2:
                return False
            
            if not power1.is_equal(power2):
                return False
        
        return True

    def compare(self, ordinal):
        if self.is_zero():
            if ordinal.is_zero():
                return 0
            else:
                return -1

        if ordinal.is_zero():
            return 1
    
        for index in range(min(len(self.terms), len(ordinal.terms))):
            count1, power1 = self.terms[index]
            count2, power2 = ordinal.terms[index]

            comparison = power1.compare(power2)

            if comparison == 0:
                if count1 < count2:
                    return -1
                
                if count1 > count2:
                    return 1

            else:
                 return comparison

        if len(self.terms) < len(ordinal.terms):
            return -1

        if len(self.terms) == len(ordinal.terms):
            return 0

        return 1

    def to_brackets(self):
        string = ''
        for count, power in self.terms:
            for _ in range(count):
                string += f'({power.to_brackets()})'
        return string

    def to_real(self):
        brackets = self.to_brackets()
        decimal = brackets.replace('(', '9').replace(')', '1')
        return f'0.{decimal or "0"}'

    @staticmethod
    def _to_string(count, power):
        if power.is_zero():
            expression = '1'
        elif power.is_one():
            expression = 'ω'
        else:
            expression = f'ω↑({power})'

        if count ==1:
            return expression
        elif expression == '1':
            return f'{count}'
        else:
            return f'{expression}×{count}'
