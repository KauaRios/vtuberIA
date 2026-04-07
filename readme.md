# 🎙️ DeusaDoKauã — IA VTuber Autônoma

Um sistema de inteligência artificial em tempo real projetado para atuar como uma VTuber autônoma, gamer e interativa. Construído com arquitetura modular em Python, rodando 100% localmente para garantir baixa latência e otimizado para ecossistemas Linux (Pipewire/ALSA).

## 🚀 Arquitetura e Tecnologias

O pipeline do sistema segue o fluxo contínuo de **Escuta Ativa ➔ Processamento ➔ Síntese de Voz**.

* **Cérebro (LLM):** [Ollama](https://ollama.com/) rodando o modelo `Llama 3.2` localmente.
* **Percepção (VAD & STT):** `SpeechRecognition` acoplado ao `WebRTC VAD` para capturar fala dinamicamente.
* **Voz (TTS):** `edge-tts` gerando áudio neural em tempo real, reproduzido via `ffplay`.
* **Sistema:** Tratamento de baixo nível com `ctypes` para supressão de logs de áudio no Linux.

## 🗺️ Mapa do Projeto (Módulos)

* **`main.py`**: O Maestro. Controla o loop infinito e a injeção de dependências.
* **`cerebro.py`**: Gerencia a personalidade (System Prompt), o histórico de contexto e a comunicação com o Ollama.
* **`voz.py`**: O motor de entrada (VAD + Transcrição).
* **`voz_saida.py`**: O motor de saída (Síntese e reprodução).

## ⚙️ Pré-requisitos (Linux)

```bash
# Instalação de dependências de sistema (Arch/CachyOS)
sudo pacman -S ffmpeg

# Certifique-se de ter o Ollama rodando
ollama run llama3.2
```

```bash
# Instalação e Execução

# 1. Clone o repositório
git clone https://github.com/KauaRios/deusadokaua.git
cd deusadokaua

# 2. Configure o ambiente virtual
python -m venv venv
source venv/bin/activate.fish

# 3. Instale as dependências e rode
pip install -r requirements.txt
python main.py
```
