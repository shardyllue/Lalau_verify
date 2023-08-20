from loguru import logger
from os.path import exists
from json import loads, dumps


class MuteStorage:


    def __init__(self, path : str):

        self.path = path

        if not exists(path):

            with open(self.path, "w") as file:
                file.write(dumps([]))

        self.words = loads(self.read())
        


    def read(self):

        with open(self.path, "r") as file:
            return file.read()

    def write(self, data : str):

        with open(self.path, "w") as file:
            return file.write(data)


    def add(self, word : str):
        
        self.words.append(word)

        self.save()


    def remove(self, word : str):
        
        try:
            self.words.remove(word)


            self.save()
        except Exception as err:
            logger.error(err)


    def save(self):

        data = dumps(self.words)
        self.write(data)

        


    