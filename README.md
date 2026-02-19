# Teletext IA

This API is hosted on Streamlit Community Cloud and is accessible at the following address:
- [teletext.streamlit.app](https://teletext.streamlit.app)

## Description

Teletext IA is an experimental project for improving video/audio accessibility with AI.
It combines research notebooks (transcription, subtitles, descriptive captions) and a Streamlit prototype dashboard.

![Capture](/docs/images/Capture.png)

## Table of Contents

- [Teletext IA](#teletext-ia)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [🎯 Project objective](#-project-objective)
  - [👥 Target audience](#-target-audience)
  - [⚙️ Current project content](#️-current-project-content)
  - [🗂️ Repository structure](#️-repository-structure)
  - [🚀 Quick start](#-quick-start)
  - [🐳 Installation \& deployment](#-installation--deployment)
  - [🥽 Security](#-security)
  - [📰 Changelog](#-changelog)
  - [🩷 Acknowledgements](#-acknowledgements)
    - [Environment](#environment)
  - [🧪 Project Status](#-project-status)
  - [🔒 License](#-license)
  - [🤝 Contributing](#-contributing)
  - [👤 Author](#-author)

## 🎯 Project objective

Build practical tools to generate accessibility outputs from media files:
- subtitles (SRT)
- text transcription
- scene-level descriptive captions
- multimodal combinations (audio + visual context)

## 👥 Target audience 

- Developers working on media accessibility tools
- Students or practitioners exploring Whisper and vision-language pipelines
- Teams prototyping inclusive video/audio workflows

## ⚙️ Current project content

- `dashboard/`: Streamlit prototype interface
  - upload audio/video
  - select one or more target outputs
  - current pipeline is a placeholder (simulated processing + ZIP output)
- `notebooks/`: research and experimentation notebooks
  - Whisper-based transcription and subtitle generation
  - folder transcription workflow
  - descriptive caption generation with scene detection + image captioning model
- project governance files: contribution, security, license, changelog, acknowledgements

## 🗂️ Repository structure

```text
teletext-ia/
├── dashboard/
│   ├── src/
│   ├── requirements.txt
│   └── streamlit_app.py
├── docs/
│   └── images/
├── notebooks/
│   ├── drafts/
│   ├── src/
│   ├── descriptive_captions.ipynb
│   ├── folder_transcription.ipynb
│   ├── subtitle.ipynb
│   └── transcription.ipynb
├── .gitignore
├── ACKNOWLEDGEMENTS.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE.md
├── README.md
└── SECURITY.md
```

## 🚀 Quick start

1. Clone the repository.
2. Install dashboard dependencies.
3. Run the Streamlit app.
4. Open notebooks for experimentation and iteration on AI pipelines.

## 🐳 Installation & deployment

The project is planned to be deployed:

- Via Docker for simple and reproducible containerisation
```shell
$ docker build -t streamlit-dashboard .
$ docker run -p 8501:8501 streamlit-dashboard
```
- Directly on the server by running the Streamlit application

```shell
$ streamlit run streamlit_app.py 
```
## 🥽 Security

- See [SECURITY.md](/SECURITY.md) for vulnerability reporting guidelines.

## 📰 Changelog

Track all notable project changes in [CHANGELOG.md](/CHANGELOG.md).

Recommended:
- Follow a consistent format such as Keep a Changelog
- Create an entry for each release
- Include Added, Changed, Fixed, and Removed sections when relevant

## 🩷 Acknowledgements

- See [ACKNOWLEDGEMENTS.md](/ACKNOWLEDGEMENTS.md) for people, tools, libraries, and communities that support this project.

### Environment

- **Python ≥ 3.13.5**
- Dependencies listed in [requirements.txt](/dashboard/requirements.txt)
- Additional notebook dependencies installed according to experiment needs

## 🧪 Project Status

- 🔬 **Status**: experimental prototype
- ✅ **Working today**: Streamlit upload flow and ZIP export, notebook experiments
- 🚧 **In progress**: implementation of real production pipeline in `dashboard/src/`

## 🔒 License

- See [LICENSE.md](/LICENSE.md).

## 🤝 Contributing

Contributions are welcome.
- See [CONTRIBUTING.md](/CONTRIBUTING.md)
- Code of conduct available in [CODE_OF_CONDUCT.md](/CODE_OF_CONDUCT.md).

## 👤 Author

Gauthier Rammault
