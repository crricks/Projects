import random
import string

class Roman:

    def roman_calculation(self, plebe):
        random.seed(0)
        self.plebe = str(plebe).lower()
        response = ''
        if string.digits in self.plebe:
            response = "Oh, you're very XXIst century.\n"
        full_name = self.plebe.split()
        self.roman_name = []
        for word in full_name:
            added = ''
            if word[-1] in 'aeiouy':
                added = random.choice(['v', 'm', 'n', 'l', 'ns', 'rp'])
            roman_word = word + added + self.rom_ending()
            self.roman_name.append(roman_word.capitalize())
        self.roman_name = response + ' '.join(self.roman_name)
        return self.roman_name


    def rom_ending(self):
        ending_list = []
        with open('test_latin_endings.txt') as roman_endings:
            for word in roman_endings:
                ending_list.append(word.strip())
            self.end = random.choice(ending_list)
            return self.end