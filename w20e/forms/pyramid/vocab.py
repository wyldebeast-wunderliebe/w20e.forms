def vocab(f):

    def new_vocab(self):
        return f(self)

    new_vocab.__vocab__ = True

    return new_vocab
