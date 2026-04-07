# 🎙️ DeusaDoKauã - IA VTuber Autônoma

Um sistema de inteligência artificial em tempo real projetado para atuar como uma VTuber autônoma, gamer e interativa. Construído com arquitetura modular em Python, rodando 100% localmente para garantir baixa latência e otimizado para ecossistemas Linux (Pipewire/ALSA).

## 🚀 Arquitetura e Tecnologias

O pipeline do sistema segue o fluxo contínuo de **Escuta Ativa ➔ Processamento ➔ Síntese de Voz**.

* **Cérebro (LLM):** Ollama rodando o modelo `Llama 3.2` localmente.
* **Percepção (VAD & STT):** `SpeechRecognition` acoplado ao `WebRTC VAD` (motor de detecção de voz em C++) para capturar fala dinamicamente.
* **Voz (TTS):** `edge-tts` gerando áudio neural em tempo real, reproduzido nativamente via `ffplay`.
* **Sistema:** Tratamento de baixo nível com `ctypes` para supressão de logs de áudio C/C++ no Linux.

## 🗺️ Mapa do Projeto (Módulos)

A base de código foi dividida por responsabilidades estritas:

* `main.py`: O Maestro. Controla o loop infinito e a injeção de dependências.
* `cerebro.py`: Gerencia a personalidade, o histórico de contexto e a comunicação com a API do Ollama.
* `voz.py`: O motor de entrada (VAD + Transcrição).
* `voz_saida.py`: O motor de saída (Síntese e reprodução).

## ⚙️ Pré-requisitos (Linux)

```bash
sudo pacman -S ffmpeg
ollama run llama3.2



```bash
git clone [https://github.com/KauaRios/deusadokaua.git](https://github.com/KauaRios/deusadokaua.git)
cd deusadokaua
python -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt
python main.py
---

### 3. Salve as dependências no terminal
Para gerar o arquivo com as bibliotecas, rode apenas este comando simples no seu terminal (com o venv ativado):

```bash
pip freeze > requirements.txt