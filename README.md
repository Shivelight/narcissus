# Narcissus

COMP6065 (Artificial Intelligence) Group Project
Class: LN01
Group: snake_case

## Installation

### Dependency

- [MagicMirror](https://github.com/MichMich/MagicMirror)
- [Snowboy](https://github.com/Kitt-AI/snowboy)
- PortAudio (for PyAudio to compile and works)
- Wit.ai key (training data is in `narcissus/models/wit`)

### Installing

The best way to install Narcissus is using virtual environtment

```
pip install .
```

### Running

Make sure MagicMirror is running before running Narcissus

```
export WIT_AI_TOKEN=wit_ai_token
python -m narcissus
```

## Commands

- Bot Appearance

	- Who are you?
    - What do you look like

- Bot Personal Status

	- How are you
	- How are you doing

- Joke

	- Tell me a joke
	- Can you tell me a joke?

- Appreciation

	- Thank you

- Greeting

	- Good morning
	- Good evening
	- Hello

- Insult

	- You stinky

- Maps

    - Show me a map of San Francisco
    - Show me a roadmap of Jakarta
    - Can you find me a satellite map of Bekasi?
    - Find me the hybrid map of Tangerang

- Snow White

	- Who is the fairest of them all?

- User

	- Who am I
	- What's my name?