import asyncio
import subprocess
import io
import edge_tts

VOZ = "Microsoft Server Speech Text to Speech Voice (pt-BR, FranciscaNeural)"

VELOCIDADE = "+10%"
TOM = "+5Hz"


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