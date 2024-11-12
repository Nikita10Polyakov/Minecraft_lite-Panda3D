import pickle


class Mapmanager():
    """ Керування мапою """

    def __init__(self):
        self.model = 'block'  # модель кубика лежить у файлі block.egg
        # # використовуються такі текстури:
        self.texture = 'block.png'
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ]  # rgba
        # створюємо основний вузол мапи:
        self.startNew()
        # self.addBlock((0,10, 0))

    def startNew(self):
        """створює основу нової мапи"""
        self.land = render.attachNewNode("Land")  # вузол, до якого прив'язані усі блоки мапи

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
        # створюємо будівельні блоки
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)

        self.block.setTag("at", str(position))

        self.block.reparentTo(self.land)

    def clear(self):
        """обнулює мапу"""
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        """створює мапу землі з текстового файлу, повертає її розміри"""
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z) + 1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        """Ставимо блок з урахуванням гравітації:"""
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, position):
        """видаляє блоки у зазначеній позиції """
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        """зберігає всі блоки, включаючи споруди, у бінарний файл"""

        """повертає колекцію NodePath для всіх існуючих у карті світу блоків"""
        blocks = self.land.getChildren()
        # відкриваємо бінарний файл на запис
        with open('my_map.dat', 'wb') as fout:
            # зберігаємо на початок файлу кількість блоків
            pickle.dump(len(blocks), fout)

            # обходимо всі блоки
            for block in blocks:
                # зберігаємо позицію
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        # видаляємо всі блоки
        self.clear()

        # відкриваємо бінарний файл на читання
        with open('my_map.dat', 'rb') as fin:
            # зчитуємо кількість блоків
            length = pickle.load(fin)

            for i in range(length):
                # зчитуємо позицію
                pos = pickle.load(fin)

                # створюємо новий блок
                self.addBlock(pos)
