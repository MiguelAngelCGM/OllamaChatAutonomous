import signal
import sys
import argparse
import os
import datetime
import json

from aiss_ollama_chat.chat import Chat
from aiss_ollama_chat_autonomous.chat import ChatAutonomous
from aiss_parameter_parser.parameter_parser import ParameterParser

AUTO:bool = False
AUTO_TURNS:int = 0
FORCE_EXIT = 3

def main():
    def signalHandler(sig, frame):
        global AUTO
        global AUTO_TURNS
        global FORCE_EXIT
        if AUTO:
            print("\nAUTO OFF\n")
            AUTO = None
            AUTO_TURNS = 0
        elif FORCE_EXIT == 0:
            print("\n--FORCE EXIT--")
            sys.exit(0)
        else:
            print(f"\n--FORCE EXIT IN {FORCE_EXIT}--")
            FORCE_EXIT -= 1
        return

    signal.signal(signal.SIGINT, signalHandler)
    
    parser = argparse.ArgumentParser(
        description='Ollama autonomous assistant-assistant chat app.',
        epilog='Example: ollama-chat-autonomous gemma3:12b-it-q8_0 gemma3:12b-it-q8_0 sysPromptA.txt sysPromptB.txt -u MyName -l 20 -t 20 -a False'
    )
    
    parser.add_argument('modelA', help='Model (A) to use')
    parser.add_argument('modelB', help='Model (B) to use')
    parser.add_argument('sysPromptA', help='Plain text file with the system prompt (A)')
    parser.add_argument('sysPromptB', help='Plain text file with the system prompt (B)')
    parser.add_argument('--lengthA', type=int, default=0,
                    help='Maximum context lenght (default: 0)')
    parser.add_argument('--lengthB', type=int, default=0,
                    help='Maximum context lenght (default: 0)')
    parser.add_argument('--userName', '-u', type=str, default="user",
                    help='User name (default: "user")')
    parser.add_argument('--assistantNameA', type=str, default="assistantA",
                    help='(default: "assistantA")')
    parser.add_argument('--assistantNameB', type=str, default="assistantB",
                    help='(default: "assistantB")')
    parser.add_argument('--prevContextA', type=str, default=None,
                    help='Previous context in a JSON format for model (A) (default: None)')
    parser.add_argument('--prevContextB', type=str, default=None,
                    help='Previous context in a JSON format for model (B) (default: None)')
    parser.add_argument('--startAuto', '-a', type=str, default="False",
                    help='(default: False)')
    parser.add_argument('--autoFirstMsg', type=str, default="",
                    help='(default: "")')
    parser.add_argument('--autoTurns', '-t', type=int, default=0,
                    help='(default: 0)')
    args = parser.parse_args()

    chatA = Chat(args.modelA, args.sysPromptA, args.lengthA, args.userName, args.assistantNameA, args.prevContextA)
    chatB = Chat(args.modelB, args.sysPromptB, args.lengthB, args.userName, args.assistantNameB, args.prevContextB)
        
    chat = ChatAutonomous(chatA, chatB, args.userName)

    autoFirstMsg = args.autoFirstMsg
    global AUTO
    global AUTO_TURNS
    AUTO = (args.startAuto == "True")
    AUTO_TURNS = args.autoTurns
    print(args.autoFirstMsg)
    prompt = " "

    while True:
        global FORCE_EXIT
        FORCE_EXIT = 3
        try:
            if AUTO:
                msg1, msg2 = chat.doRecursiveChat(autoFirstMsg)
                autoFirstMsg = None
                print(f"{msg1}{msg2}")
                if AUTO_TURNS > 0:
                    AUTO_TURNS -= 1
                    if AUTO_TURNS == 0:
                        AUTO = False
            else:
                prompt = input(f"{chat.userName}: ")
                if prompt.endswith("RETRY"):
                    continue
                elif prompt.startswith("auto"):
                    if prompt.startswith("auto:"):
                        AUTO = True
                        try:
                            parser = ParameterParser(prompt[len("auto:"):].strip(), [int, str])
                            turns = next()
                            msg = next()
                            AUTO_TURNS = turns
                            if msg != "":
                                chat.doRecursiveChat(msg)
                        except Exception as e:
                            print(f"\n\n{e}")
                    else:
                        AUTO_TURNS = 0
                    continue
                elif prompt.startswith("exit"):
                    print("Good bye!")
                    break
                else:
                    print(f"{chat.chat(prompt)}\n\n")
        except Exception as e:
            print(f"{e}\n\n")
    chat.makeBackup()


if __name__ == "__main__":

    main()
