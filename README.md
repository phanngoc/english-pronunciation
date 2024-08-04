# English Pronunciation Assessment using OpenAI Whisel

This repository provides a solution for assessing English pronunciation using OpenAI Whisel. 

## Introduction

Assessing pronunciation is an important aspect of language learning. This project aims to leverage the power of OpenAI Whisel, a state-of-the-art speech recognition model, to provide accurate and automated pronunciation assessment for English learners.

## Features

- **Automated Pronunciation Assessment**: OpenAI Whisel allows for automated assessment of English pronunciation, providing learners with instant feedback on their pronunciation accuracy.

- **Scoring System**: The assessment system provides a scoring mechanism to evaluate the learner's pronunciation proficiency, helping them track their progress over time.

- **Interactive Interface**: The repository includes an interactive interface that allows users to input their spoken English and receive immediate feedback on their pronunciation.

## Getting Started

To get started with this project, follow these steps:

- Clone the repository: `git clone https://github.com/phanngoc/english-pronunciation.git`

- Setup virtual environment
```
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

- Set up OpenAI Whisel API credentials.
Setup .env
```
OPENAI_API_KEY=
```

- Running worker
```
./myenv/bin/celery -A tasks worker -l INFO --concurrency=1
```

- Running web server
```
./myenv/bin/python app.py
```

- Running dashboard flower (tracking task)
```
./myenv/bin/celery -A tasks flower
```

1. Access the application in your web browser at `http://localhost:5000`.

![alt text](<images/Screen Shot 2024-07-20 at 11.36.11.png>)

## Contributing

Phân đang research:
- Sử dụng link audio trả về từ tts model để đánh giá pronunciation.
- Sử dụng link audio trả về từ tts model đưa ra cho người học nghe.
    => cái ni hơi khoai, cần load stream về bằng ajax sau khi load page.
## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

We would like to express our gratitude to OpenAI for providing the Whisel API, which powers the pronunciation assessment in this project.

## Acknowledgements

We would like to express our gratitude to OpenAI for providing the Whisel API, which powers the pronunciation assessment in this project.

We would also like to thank gTTS (Google Text-to-Speech) for their contribution. gTTS is used to generate audio links for pronunciation evaluation and listening exercises.

## Development

```bash
pip freeze > requirements.txt
```
