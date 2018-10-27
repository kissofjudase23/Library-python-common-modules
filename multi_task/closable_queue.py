#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue


class ClosableQueue(Queue):

    SENTINEL = object()

    def close(self):
        self.put(ClosableQueue.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is ClosableQueue.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()


