import numpy as np
import zmq
from ipc import SharedRingBuffer
from multiprocessing import Process, Event
import multiprocessing as mp
import time

BIG_ARRAY = np.random.randint(0,255,(4096,4096), dtype='B')
NLOOP = 100

def process_0(buffer: SharedRingBuffer, nloop):
    # start timing
    start_time = time.time_ns()

    # loop
    for i in range(nloop):
        buffer.data_available.wait()
        _, buf = buffer.get_read_buffer()
        array = np.frombuffer(buf, dtype='B')
        print(np.mean(array))
        buffer.read_done()

    # stop timing
    stop_time = time.time_ns() - start_time
    print(f'{1e-9*stop_time}')

def process_1(data_available: Event, nloop):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://localhost:5555")

    # start timing
    start_time = time.time_ns()

    # loop
    for i in range(nloop):
        data_available.wait()
        data = socket.recv()
        array = np.frombuffer(data, dtype='B')
        print(np.mean(array))

    # stop timing
    stop_time = time.time_ns() - start_time
    print(f'{1e-9*stop_time}')

if __name__ == '__main__':
    mp.set_start_method('spawn')

    # shared ring buffer 
    buffer = SharedRingBuffer(num_element=10, element_byte_size=BIG_ARRAY.nbytes)

    proc1 = Process(target=process_0, args=(buffer, NLOOP))
    proc1.start()

    # loop
    for i in range(NLOOP):
        _ , buf = buffer.get_write_buffer()
        buf[:] = BIG_ARRAY.reshape((BIG_ARRAY.nbytes,))
        buffer.write_done()

    # done
    proc1.join()

    # zmq
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5555")
    data_available = Event()

    proc2 = Process(target=process_1, args=(data_available, NLOOP))
    proc2.start()

    # loop
    for i in range(NLOOP):
        socket.send(BIG_ARRAY.reshape((BIG_ARRAY.nbytes,)))
        data_available.set()

    # done
    proc2.join()

