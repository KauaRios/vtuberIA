import asyncio
import subprocess
import io
import edge_tts

# ThalitaMultilingualNeural: a voz pt-BR mais nova e natural disponível no edge-tts
# Treinada com dados multilíngues — soa bem mais realista que FranciscaNeural
# Formato longo obrigatório para evitar NoAudioReceived
VOZ = "Microsoft Server Speech Text to Speech Voice (pt-BR, ThalitaMultilingualNeural)"

VELOCIDADE = "+12%"  # Um pouco acima do normal — energia de VTuber sem atropelar
TOM = "+10Hz"        # Levemente mais agudo — mais expressivo e jovem

# Caracteres que quebram o TTS — maketrans é mais rápido que replace em loop
_CHARS_PROIBIDOS = str.maketrans('', '', '*_#—~[]')


async def _sintetizar_e_falar(texto: str):
    try:
        comunicar = edge_tts.Communicate(texto, VOZ, rate=VELOCIDADE, pitch=TOM)
        buffer = io.BytesIO()

        async for chunk in comunicar.stream():
            if chunk["type"] == "audio":
                buffer.write(chunk["data"])

        audio = buffer.getvalue()

        if not audio:
            print("[voz_saida] Nenhum audio recebido.")
            return

        subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "-i", "pipe:0"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).communicate(input=audio)

    except Exception as e:
        print(f"[voz_saida] Erro na sintese: {e}")


def falar(texto: str):
    if not texto:
        return

    texto = texto.translate(_CHARS_PROIBIDOS).strip()

    if not texto:
        return

    asyncio.run(_sintetizar_e_falar(texto))