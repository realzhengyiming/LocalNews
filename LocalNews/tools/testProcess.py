import multiprocessing
import time

def worker_1(interval):
    print ("worker_1")
    time.sleep(interval)
    print ("end worker_1")

def worker_2(interval):
    print ("worker_2")
    time.sleep(interval)
    print ("end worker_2")

def worker_3(interval):
    print ("worker_3")
    time.sleep(interval)
    print ("end worker_3")

def worker_4(interval):
    print ("worker_4")
    time.sleep(interval)
    print ("end worker_4")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target = worker_1, args = (2,))
    p2 = multiprocessing.Process(target = worker_2, args = (2,))
    p3 = multiprocessing.Process(target = worker_3, args = (2,))
    p4 = multiprocessing.Process(target=worker_4, args=(2,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

    print ("END!!!!!!!!!!!!!!!!!")