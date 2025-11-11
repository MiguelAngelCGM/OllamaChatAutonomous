from aiss_ollama_chat.chat import Chat as OllamaChat


class OllamaChatAutonomous:
    def __init__(self, model1:str, model2:str, sysPrompt1:str, sysPrompt2:str, turns:int=10, maxChatLength:int=10):
        self.turns:int = turns
        self.c1:OllamaChat = OllamaChat(model1, sysPrompt1, maxChatLength)
        self.c2:OllamaChat = OllamaChat(model2, sysPrompt2, maxChatLength)

    def doChat(self, prompt) -> bool:
        msg = self.c1.doChat(prompt)
        msg = self.c2.doChat(msg)
        return msg
    
    def printToFile(self) -> None:
        self.c1.printToFile("Chat-A")
        self.c2.printToFile("Chat-B")
