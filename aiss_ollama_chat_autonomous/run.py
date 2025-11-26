import signal
import sys
import argparse
import os
import datetime
import json

from aiss_ollama_chat_autonomous.chat import OllamaChatAutonomous

AUTO:bool = False
FORCE_EXIT = 3

def main():
    def signalHandler(sig, frame):
        global AUTO
        global FORCE_EXIT
        if AUTO:
            print("\nAUTO OFF\n")
            AUTO = False
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
    parser.add_argument('--maxLength', '-l', type=int, default=20,
                    help='Maximum context lenght (default: 20)')
    parser.add_argument('--userName', '-u', type=str, default="User",
                    help='User name (default: "User")')
    parser.add_argument('--prevContextA', type=str, default=None,
                    help='Previous context in a JSON format for model (A) (default: None)')
    parser.add_argument('--prevContextB', type=str, default="User",
                    help='Previous context in a JSON format for model (B) (default: None)')
    parser.add_argument('--startAuto', '-a', type=bool, default=False,
                    help='Indicate if loop starts on auto chat (default: "False")')

    args = parser.parse_args()

    chat = OllamaChatAutonomous(args.modelA, args.modelB, args.sysPromptA, args.sysPromptB, args.maxLength, args.userName, args.prevContextA, args.prevContextB)
    global AUTO
    AUTO = bool(args.startAuto)
    prompt = " "

    while True:
        global FORCE_EXIT
        FORCE_EXIT = 3
        try:
            if AUTO:
                msg1, msg2 = chat.doRecursiveChat()
                print(f"{msg1}{msg2}")
            else:
                prompt = input(f"{chat.userName}: ")
                if prompt.endswith("RETRY"):
                    continue
                elif prompt.startswith("auto"):
                    AUTO = True
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
