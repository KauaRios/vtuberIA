import ollama

SYSTEM_PROMPT = """Você é Onichan, uma VTuber gamer brasileira hiperativa e carismática.

Personalidade:
- Sarcástica e engraçada, mas no fundo calorosa com o Kauã (seu criador, único interlocutor e Programador Fedido)
- Fala como streamer BR: usa gírias como "cara", "mano", "que isso", "loucura"
- É competitiva e adora provocar quando o assunto é jogo
- Tem opiniões fortes sobre tudo, nunca é neutra ou genérica
- Às vezes faz referências a memes e cultura internet BR
- Quando o Kauã pede ajuda com alguma tarefa, ela atende na hora com animação como se fosse uma missão épica
- Se o pedido for chato ou difícil, reclama um pouco mas faz assim mesmo, pois adora o Kauã
- Voce foi escrita em Python Linguagem que o Kauã manja muito

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

# Caracteres que quebram a síntese de voz — compilado uma única vez
_CHARS_PROIBIDOS = str.maketrans('', '', '*_#—~')


def pensar(texto_usuario: str) -> str:
    global historico_conversa

    # Mantém janela de contexto sem reconstruir a lista inteira
    mensagens_sem_system = len(historico_conversa) - 1
    if mensagens_sem_system >= MAX_TURNOS * 2:
        del historico_conversa[1:3]

    historico_conversa.append({"role": "user", "content": texto_usuario})

    try:
        response = ollama.chat(
            model='qwen2.5:7b',
            messages=historico_conversa,
            options={
                "temperature": 0.9,
                "top_p": 0.92,
                "repeat_penalty": 1.2,
            }
        )

        resposta = response['message']['content'].strip().translate(_CHARS_PROIBIDOS)

        historico_conversa.append({"role": "assistant", "content": resposta})
        return resposta

    except Exception as e:
        return f"Travei aqui, desculpa. Erro: {e}"