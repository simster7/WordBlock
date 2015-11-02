# import queue
# import threading
# import urllib

# worker_data = ['http://google.com', 'http://yahoo.com', 'http://bing.com']

# #load up a queue with your data, this will handle locking
# q = queue.Queue()
# for url in worker_data:
#     q.put(url)

# #define a worker function
# def worker(queue):
#     queue_full = True
#     while queue_full:
#         try:
#             #get your data off the queue, and do some work
#             url= queue.get(False)
#             opener = urllib.request.build_opener()
#             html = opener.open(url).read(100000).\
#                 decode(encoding='utf-8', errors='replace')
#             print(len(data))
#         except:
#             queue_full = False

# #create as many threads as you want
# thread_count = 5
# thread_list = []
# for i in range(thread_count):
#     t = threading.Thread(target=worker, args = (q,))
#     thread_list.append(t)
#     t.start()
# for thread in thread_list:
#     t.join()
import wikipedia
import threading

querylist = wikipedia.search("Federer")[0:5]
output = []

def worker(query):
    text = wikipedia.page(query).content
    print(text)
    output.append(text.split()[0:3])

thread_list = []
for i in range(5):
    t = threading.Thread(target=worker, args=(querylist[i],))
    t.start()
    thread_list.append(t)
for thread in thread_list:
    thread.join()
print(output)