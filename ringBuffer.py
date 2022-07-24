import numpy as np
import numbers

class RingBuffer:
    
    def __init__(self, maxNumItems, itemSize=1):
        
        self.maxNumItems = maxNumItems
        self.itemSize = itemSize
        self.totalSize = maxNumItems*itemSize
        self.data = np.zeros(self.totalSize)
        self.write_cursor = 0
        self.read_cursor = 0

    def full(self):
        return self.write_cursor==((self.read_cursor-self.itemSize)%self.totalSize)

    def empty(self):
        return self.write_cursor==self.read_cursor

    def check_item(self, item):
        ''' Check item type '''

        if not isinstance(item,(numbers.Number, list, np.ndarray)):
            raise TypeError("Accepted types: scalar, list, numpy array")
        
        if isinstance(item,numbers.Number) and self.itemSize>1:
            raise TypeError(
                "Expecting {0} items, got scalar".format(
                    self.itemSize
                    )
                )
        
        if isinstance(item,list) and len(item) != self.itemSize:
            raise TypeError(
                "Expecting {0} items, got {1}".format(
                    self.itemSize,
                    len(item)
                    )
                )
        
        if isinstance(item,np.ndarray) and len(item.shape)>1:
            raise TypeError(
                "Expecting 1D array, got {0}D".format(
                    len(item.shape)
                    )
                )
        
        if isinstance(item,np.ndarray) and item.shape[0] != self.itemSize:
            raise TypeError(
                "Expecting {0} items, got {1}".format(
                    self.itemSize,
                    item.shape[0]
                    )
                )

    def push(self, item):
        ''' Add item at the back '''

        self.check_item(item)
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
        reprstr = ("Ring Buffer " + "="*20 
            + "\nRead: {0}\nWrite: {1}\nSize: {2}\nData: {3}".format(
            self.read_cursor,
            self.write_cursor,
            self.size(),
            self.data)
        )
        return reprstr


if __name__ == '__main__':

    r = RingBuffer(5)
    r.push(0)
    r.push(1)
    r.push(2)
    r.push(3)
    ok, it = r.pop()
    r.push(4)
    ok, it = r.pop()
    r.push(5)
    print(r)

    r = RingBuffer(5,2)
    r.push([1,2])
    r.push([3,4])
    r.push([5,6])
    r.push([7,8])
    ok, it = r.pop()
    r.push([9,10])
    ok, it = r.pop()
    r.push([11,12])
    print(r)
