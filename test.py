from ipc import SharedRingBuffer
from multiprocessing import Process
import multiprocessing as mp
import time

def par_write(buffer: SharedRingBuffer, pnum: int):
    _, mview = buffer.get_write_buffer() 
    mview[:] = pnum.to_bytes(length=1, byteorder='big')
    buffer.write_done()

def par_read(buffer: SharedRingBuffer):
    buffer.data_available.wait()
    _, mview = buffer.get_read_buffer() 
    print(mview.tobytes(), flush=True)
    buffer.read_done()

if __name__ == '__main__':
    mp.set_start_method('spawn')

    buffer = SharedRingBuffer(num_element=10, element_byte_size=1)

    plist = []
    for i in range(15):
        proc = Process(target=par_write, args=(buffer, i))
        plist.append(proc)
        proc.start()

    for i in range(15):
        plist[i].join()

        # pretend all was read
        buffer.read_done()

    print(buffer.data[:])

    proc = Process(target=par_read, args=(buffer, ))
    proc.start()
    
    print(buffer.data_available.is_set())

    time.sleep(2)
    _, buf = buffer.get_write_buffer()
    buf[:] = B'\xaa'
    buffer.write_done()

    proc.join()
    print(buffer.data[:])

