from aiss_ollama_chat.chat import Chat
from aiss_parameter_parser_parameter_parser import ParameterParser

class ChatAutonomous:
    def __init__(self, chatA:Chat, chatB:Chat, userName:str="user"):
        self.userName = userName
        self.c1:chatA = chatA
        self.c2:chatB = chatB
        self.chatAutonomousOperations = {
            "_A": self._handleChatA,
            "_B": self._handleChatB,
            "_AB": self._handleChatAB
        }

    def autoChat(self, turns):
        if turns < 0: raise Exception(f"Invalid num. turns. Param: {turns}")
        while turns != 0:
            self.doRecursiveChat()
            turns -= 1
    
    def doRecursiveChat(self, prompt:str=None):
        if not prompt or prompt == "":
            prompt = self.c2.getLastContextMsg()
        msg = self.c1.chat(prompt)
        msg2 = self.c2.chat(msg)
        return msg, msg2

    def doChatA(self, prompt):
        return self.c1.chat(prompt)
    
    def doChatB(self, prompt):
        return self.c2.chat(prompt)
    
    def chat(self, prompt):
        try:
            parser = ParameterParser(prompt, [str,str])
            op = parser.next()
            params = parser.next()
            return self.chatAutonomousOperations[op](params)
        except (ValueError, KeyError):
            return self._handleDefault(prompt)

    def _handleSave(self, prompt: str) -> str:
        self.c1.chat("save:context1.json")
        self.c2.chat("save:context2.json")
        return "-- serialized to ./context1.json and ./context2.json --\n\n"

    def _handleRestore(self, prompt: str) -> str:
        self.c1.chat("restore:context1.json")
        self.c2.chat("restore:context2.json")
        return "-- restored from ./context1.json and ./context2.json --\n\n"

    def _handleRewind(self, prompt: str) -> str:
        if prompt.startswith("rewind:"):
            amount = int(prompt[len("rewind:"):].strip())
            self.c1.rewind(amount)
            self.c2.rewind(amount)
            return f"-- rewind AB: {amount} --\n\n"
        else:
            self.c1.rewind(1)
            self.c2.rewind(1)
            return "-- rewind AB: 1 --\n\n"
        
    def _handleChatA(self, prompt):
        return f"{self.doChatA(prompt[len('A:'):].strip())}"

    def _handleChatB(self, prompt):
        return f"{self.doChatB(prompt[len('B:'):].strip())}"

    def _handleChatAB(self, prompt):
        msg1 = f"{self.doChatA(prompt[len('A:'):].strip())}"
        msg2 = f"{self.doChatB(prompt[len('B:'):].strip())}"
        return f"{msg1}{msg2}"
    
    def _handleDefault(self, prompt):
        msg1, msg2 = self.doRecursiveChat(prompt)
        return f"{msg1}{msg2}"

    def makeBackup(self) -> None:
        self.c1.makeBackup("Chat-A")
        self.c2.makeBackup("Chat-B")
