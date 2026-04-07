import os
import ctypes
import ctypes.util
import speech_recognition as sr




def _silenciar_alsa():
    """
    Instala um error handler nulo direto na libasound via ctypes.
    Isso impede que qualquer mensagem de erro C chegue ao stderr.
    É mais robusto que redirecionar fd 2 pois age antes do write().
    """
    try:
        asound = ctypes.cdll.LoadLibrary('libasound.so.2')
       
        asound.snd_lib_error_set_handler(None)
    except OSError:
        pass  # libasound não encontrada — ignora silenciosamente


class _SuppressStderr:
    """
    Segundo nível de defesa: redireciona fd 2 (stderr do processo inteiro,
    incluindo C/C++) para /dev/null durante a inicialização do PyAudio.
    Cobre JACK e outros backends que não usam libasound.
    """
    def __enter__(self):
        self._fd = os.dup(2)
        self._devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(self._devnull, 2)
        return self

    def __exit__(self, *_):
        os.dup2(self._fd, 2)
        os.close(self._fd)
        os.close(self._devnull)


# Executa uma única vez no import do módulo
_silenciar_alsa()


# ==========================================
# PARÂMETROS DO RECOGNIZER — LÓGICA E MATEMÁTICA
# ==========================================
#
# energy_threshold = 450
#   O SpeechRecognition mede energia de áudio em RMS (Root Mean Square).
#   Valor padrão (300) é baixo demais para ambientes com ventoinha/PC.
#   450 é empiricamente bom para home office com ruído de fundo moderado.
#   Se ainda cortar fala: suba para 500-600. Se não detectar voz: desça para 350.
#
# dynamic_energy_threshold = False
#   Quando True, o SR ajusta o threshold automaticamente a cada chunk.
#   Problema: em ambientes com ruído constante (ventoinha), ele "aprende"
#   o ruído como linha de base e passa a ignorar a voz também. Desativamos.
#
# pause_threshold = 1.8  (segundos)
#   Tempo de silêncio contínuo para considerar que a frase terminou.
#   Padrão é 0.8s — muito curto para fala de VTuber que faz pausas dramáticas.
#   1.8s = tempo confortável para respirar, pensar e continuar a frase.
#   Para frases ainda mais longas/reflexivas, use 2.2s.
#
# phrase_threshold = 0.2  (segundos)
#   Tempo mínimo de áudio para considerar que é uma frase real (não ruído).
#   0.2s filtra cliques de teclado e batidas curtas sem cortar sílabas.
#
# non_speaking_duration = 0.4  (segundos)
#   Quantos segundos de silêncio são incluídos no início e fim do áudio gravado.
#   Garante que a primeira e última sílaba da frase não sejam cortadas.
#   Deve ser ≤ pause_threshold / 2 para não conflitar com a detecção de pausa.
# ==========================================

def _criar_recognizer() -> sr.Recognizer:
    r = sr.Recognizer()
    r.energy_threshold = 450
    r.dynamic_energy_threshold = False
    r.pause_threshold = 1.8
    r.phrase_threshold = 0.2
    r.non_speaking_duration = 0.4
    return r


def _criar_microfone() -> sr.Microphone:
    """
    Inicializa o microfone suprimindo stderr no momento exato
    em que o PyAudio abre o ALSA/JACK — que é quando o spam acontece.
    """
    with _SuppressStderr():
        mic = sr.Microphone(sample_rate=16000)
    return mic


# Instâncias únicas reutilizadas entre chamadas (evita overhead de reinicialização)
_recognizer = _criar_recognizer()
_microfone = _criar_microfone()


def capturar_voz_ia() -> str | None:
    print("  Aguardando você começar a falar...")

    with _SuppressStderr():
        with _microfone as source:
            audio = _recognizer.listen(source)

    print("⏸  Processando...")

    try:
        texto = _recognizer.recognize_google(audio, language='pt-BR')
        print(f" Reconhecido: {texto}")
        return texto
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"❌ Erro na API do Google: {e}")
        return None