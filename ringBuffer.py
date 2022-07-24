import numpy as np

class RingBuffer:
    
    def __init__(self, maxNumItems, itemSize=1):
        
        self.maxNumItems = maxNumItems
        self.itemSize = itemSize
        self.totalSize = maxNumItems*itemSize
        self.data = np.zeros(self.totalSize)
        self.write_cursor = 0
        self.read_cursor = 0

    def full(self):
        return self.write_cursor == ((self.read_cursor - self.itemSize) % self.totalSize)

    def empty(self):
        return self.write_cursor == self.read_cursor

    def push(self, item):
        ''' Add item at the back '''

        #TODO check that item is the right size/type other throw ValueError

        if not self.full():
            self.data[self.write_cursor:self.write_cursor+self.itemSize] = item
            self.write_cursor = (self.write_cursor+self.itemSize)%self.totalSize
            return True
        else:
            return False

    def pop(self):
        ''' Return item from the front '''
        
        if not self.empty():
            item = self.data[self.read_cursor:self.read_cursor+self.itemSize]
            self.read_cursor = (self.read_cursor+self.itemSize)%self.totalSize
            return True, item
        else:
            return False, []

    def size(self):
        ''' Return number of items currently stored in the buffer '''
        return (self.write_cursor-self.read_cursor)%self.totalSize

    def __repr__(self):
        reprstr = "Ring Buffer\nRead: {0}\nWrite: {1}\nSize: {2}\nData: {3}".format(
            self.read_cursor,
            self.write_cursor,
            self.size(),
            self.data)
        return reprstr


if __name__ == '__main__':

    r = RingBuffer(5)
    r.push(0)
    r.push(1)
    r.push(2)
    r.push(3)
    r.pop()
    r.push(4)
    print(r)
