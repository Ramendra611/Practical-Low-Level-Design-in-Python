from models.card import Card


class Screen:
    def show(self, message):
        print(message)


class Keyboard:
    def read(self, prompt):
        return input(prompt)


class CardReader:
    def read(self, card: Card):
        return card

    def capture(self, card: Card):
        pass

    def eject(self):
        pass


class Printer:
    pass
