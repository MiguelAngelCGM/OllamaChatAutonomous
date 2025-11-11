# Ollama Chat Autonomous - Autonomous Ollama Chatbot

This project implements an autonomous chat system using Ollama, where two artificial intelligence models interact with each other in a continuous conversation.

## 📋 Description

The project allows creating an autonomous chat where two language models communicate with each other, generating a continuous conversation. Each model acts as a different participant in the conversation, responding to messages from the other model.

## 🚀 Features

The system creates two chatbots that communicate with each other: 
- The first model (c1) receives an initial message and responds
- The second model (c2) receives the first model's response and responds
- This process repeats for the specified number of turns
- Results are saved to text files
     
## 🛠 Requirements

- Python 3.7+
- Ollama installed and running
- Required packages:
  - `ollama`
  - `aiss_ollama_chat`

## 📦 Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Clone the repository:
   ```bash
   git clone <your-repository>
   cd ollamaChat
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install package using:
   ```bash
   pip install .
   ```

## ▶️ Usage

Run the program with:
```bash
ollama-chat-autonomous <model1> <model2> <prompt1> <prompt2> <numTurns> <maxLength>
```

Example:
```bash
ollama-chat-autonomous gemma3:12b-it-q8_0 gemma3:12b-it-q8_0 ./sysPrompt1.txt ./sysPrompt2.txt 10 10
```

## 📁 Project Structure

```
.
├── aiss_ollama_chat_autonomous/
│   ├── __init__.py
│   ├── chat.py
│   └── run.py
├── run.sh
├── setup.py
├── sysPrompt1.txt
├── sysPrompt2.txt
├── LICENSE
└── README.md
```

## 📄 Output

Conversation history is saved in a timestamped folder:
```
Chat-A_2025-11-09_21-00-00/
├── log.sh
└── params.py
Chat-B_2025-11-09_21-00-00/
├── log.sh
└── params.py
```

## 🤝 Contributions

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.
