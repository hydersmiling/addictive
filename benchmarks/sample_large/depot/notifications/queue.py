"""Outgoing message queue (stored, not sent)."""


class MessageQueue:
    def __init__(self):
        self.pending = []

    def enqueue(self, to, text):
        self.pending.append({"to": to, "text": text})

    def drain(self):
        items, self.pending = self.pending, []
        return items
