"""Pooling Process To Handle Event
"""
import multiprocessing as mp
import queue

class EventPoolRecord:
    def __init__(self, handler, bot, event):
        self.id = 0  #このオブジェクトだけEventPool内で変更される
        self.handler = handler
        self.bot = bot
        self.event = event
class EventPool:
    def __init__(self):
        self.processes = [] # id付きのプロセス
        self.ctx = mp.get_context('spawn')
        self.queue = self.ctx.Queue()
        self.run_count = 0
    @staticmethod
    def do_handler(record, queue):
        """生成したプロセス上で実行するハンドリング処理
        """
        exec_id = record.id
        try:
            #self.queue.put(record)
            record.handler.on_event(record.bot, record.event)
        finally:
            queue.put(exec_id)
    def check_queue(self):
        """終了したプロセスがあったらJoinする
        """
        while 1:
            try:
                exec_id = self.queue.get_nowait()
            except queue.Empty:
                break
            for item in filter(lambda item: item[0] == exec_id, self.processes):
                item[1].join()
                self.processes.remove(item)
    def kill(self):
        """全プロセスを正常終了,あるいは強制終了させる
        """
        for item in self.processes:
            if item[1].join(0.5) is not None:
                self.processes.remove(item)
        for item in self.processes:
            item[1].terminate()
            self.processes.remove(item)
    def register(self, record: EventPoolRecord):
        """実行プロセスを登録
        """
        record.id = self.run_count
        self.run_count += 1
        process = mp.Process(target=EventPool.do_handler, args=(record, self.queue))
        self.processes.append((record.id, process))
        process.start()