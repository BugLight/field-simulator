from threading import Thread
import time

class Tracer(Thread):
    def __init__(self, trace, trace_args):
        Thread.__init__(self, target = self.idle)
        self.trace = trace
        self.targets = []
        self.trace_args = trace_args

    def idle(self):
        while True:
            if len(self.targets):
                target = self.targets.pop(0)
                self.trace(target, *self.trace_args)
            else:
                time.sleep(10)

    def put(self, target):
        self.targets.append(target)
