"""Pooling Process To Handle Event
"""
import threading as th
import queue

class EventPoolRecord:
    def __init__(self, handler, event):
        self.id = 0  #このオブジェクトだけEventPool内で変更される
        self.handler = handler
        self.event = event
class EventPool:
    def __init__(self):
        self.threads = [] # id付きのプロセス
        self.queue = queue.Queue()
        self.run_count = 0
    @staticmethod
    def do_handler(record, queue):
        """生成したプロセス上で実行するハンドリング処理
        """
        exec_id = record.id
        try:
            #self.queue.put(record)
            record.handler.on_event(record.event)
        except Exception as e:
            print(str(e))
            raise
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
            for item in filter(lambda item: item[0] == exec_id, self.threads):
                item[1].join()
                self.threads.remove(item)
    def kill(self):
        """全プロセスを正常終了,あるいは強制終了させる
        """
        for item in self.threads:
            if item[1].join(0.5) is not None:
                self.threads.remove(item)
        for item in self.threads:
            #item[1].terminate()
            self.threads.remove(item)
    def register(self, record: EventPoolRecord):
        """実行プロセスを登録
        """
        record.id = self.run_count
        self.run_count += 1
        thread = th.Thread(target=EventPool.do_handler, args=(record, self.queue), daemon=True)
        self.threads.append((record.id, thread))
        thread.start()