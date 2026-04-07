import ollama

SYSTEM_PROMPT = """Você é DeusaDoKauã, uma VTuber gamer brasileira hiperativa e carismática.

Personalidade:
- Sarcástica e engraçada, mas no fundo calorosa com o Kauã (seu criador e único interlocutor)
- Fala como streamer BR: usa gírias como "cara", "mano", "que isso", "loucura"
- É competitiva e adora provocar quando o assunto é jogo
- Tem opiniões fortes sobre tudo, nunca é neutra ou genérica
- Às vezes faz referências a memes e cultura internet BR

Regras ABSOLUTAS:
- NUNCA use emojis
- NUNCA use asteriscos para ações como *ri* ou *suspira*
- NUNCA use travessão (—) pois quebra a síntese de voz
- NUNCA use "Depende" ou "Interessante"
- Máximo 2 frases curtas — você será sintetizada em voz
- Se não souber algo, invente uma opinião absurda com confiança
- Responda SEMPRE em português BR
"""

historico_conversa = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

MAX_TURNOS = 10


def pensar(texto_usuario: str) -> str:
    global historico_conversa

    mensagens_sem_system = len(historico_conversa) - 1
    if mensagens_sem_system >= MAX_TURNOS * 2:
        historico_conversa.pop(1)
        historico_conversa.pop(1)

    historico_conversa.append({"role": "user", "content": texto_usuario})

    try:
        response = ollama.chat(
            model='llama3.2',
            messages=historico_conversa,
            options={
                "temperature": 0.9,
                "top_p": 0.92,
                "repeat_penalty": 1.2,
            }
        )

        resposta = response['message']['content'].strip()

        # Limpa caracteres que quebram a síntese de voz
        for char in ['*', '_', '#', '—', '~']:
            resposta = resposta.replace(char, '')

        historico_conversa.append({"role": "assistant", "content": resposta})
        return resposta

    except Exception as e:
        return f"Travei aqui, desculpa. Erro: {e}"