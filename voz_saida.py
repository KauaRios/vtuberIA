import asyncio
import subprocess
import io
import edge_tts

# ThalitaNeural: voz feminina mais jovem e expressiva disponível em pt-BR no edge-tts

VOZ = "Microsoft Server Speech Text to Speech Voice (pt-BR, ThalitaNeural)"

# Velocidade da fala: +15% deixa mais agitada e com energia de streamer
VELOCIDADE = "+15%"
# Tom: +15Hz deixa a voz mais aguda, aproximando do estilo anime/VTuber
TOM = "+15Hz"


async def _sintetizar_e_falar(texto: str):
    comunicar = edge_tts.Communicate(texto, VOZ, rate=VELOCIDADE, pitch=TOM)
    buffer = io.BytesIO()

    async for chunk in comunicar.stream():
        if chunk["type"] == "audio":
            buffer.write(chunk["data"])

    buffer.seek(0)
    audio = buffer.read()

    if not audio:
        return

    subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "-i", "pipe:0"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).communicate(input=audio)


def falar(texto: str):
    if not texto or not texto.strip():
        return
    asyncio.run(_sintetizar_e_falar(texto))
