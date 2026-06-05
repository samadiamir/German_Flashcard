# 🇩🇪 German Flashcards App

A desktop flashcard application built with **Python** and **PySide6** to help learners memorize German vocabulary efficiently.

## Features

* 📚 Study German words with flashcards
* 🔄 Automatic card flipping after a few seconds
* ✅ Mark words as known and remove them from the learning queue
* 💾 Progress is automatically saved
* 🎲 Random card selection
* ⌨️ Keyboard shortcuts for faster learning
* 🖥️ Clean and user-friendly desktop interface

## Project Structure

```text
Flashcard/
│
├── data/
│   ├── german_words.csv
│   └── words_to_learn.csv
│
│
├── main.py
├── requirements.txt
└── README.md
```

## Data Format

The CSV file should contain two columns:

| German | English |
| ------ | ------- |
| Haus   | House   |
| Hund   | Dog     |
| Wasser | Water   |

Example:

```csv
German,English
Haus,House
Hund,Dog
Wasser,Water
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/german-flashcards.git
cd german-flashcards
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Keyboard Shortcuts

| Key         | Action        |
| ----------- | ------------- |
| Space       | Flip Card     |
| Left Arrow  | Next Card     |
| Right Arrow | Mark as Known |

## Technologies

* Python 3
* PySide6 (Qt for Python)
* Pandas

## Future Improvements

* Progress statistics
* Vocabulary categories (A1, A2, B1...)
* German pronunciation (Text-to-Speech)
* Flashcard animations
* Dark/Light theme support

## License

This project is open source and available under the MIT License.
