class SessionMemory:
    def __init__(self):
        self._messages = []

    def add(self, role, content):
        if not content:
            return
        self._messages.append({"role": role, "content": str(content)})

    def as_list(self):
        return list(self._messages)

    def reset(self):
        self._messages = []
