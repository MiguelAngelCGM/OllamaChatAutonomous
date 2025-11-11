import sys
import os
import datetime
import json

from aiss_ollama_chat_autonomous.chat import OllamaChatAutonomous

MODEL1 = sys.argv[1]
MODEL2 = sys.argv[2]
SYS_PROMPT1 = sys.argv[3]
SYS_PROMPT2 = sys.argv[4]
NUM_TURNS = int(sys.argv[5])
MAX_LENGTH = int(sys.argv[6])

def main():
    chat = OllamaChatAutonomous(MODEL1, MODEL2, SYS_PROMPT1, SYS_PROMPT2, NUM_TURNS, MAX_LENGTH)
    msg = ""
    while chat.turns!=0:
        msg = chat.doChat(msg)
        chat.turns -= 1
        print(f"AI 1:\n{msg}\n\n")
        print(f"AI 2:\n{msg}\n\n")
        continue
    chat.printToFile()
    return

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Run: ollama-chat-autonomous <model1> <model2> <prompt1> <prompt2> <numTurns> <maxLength>")
        print("Example: ollama-chat-autonomous gemma3:12b-it-q8_0 gemma3:12b-it-q8_0 ./sysPrompt1.txt ./sysPrompt2.txt 10 10")
        sys.exit(1)
    main()
