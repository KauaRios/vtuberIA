import voz
import cerebro
import voz_saida


def executar_ia():
    print("=" * 40)
    print("  Onichan — Online")
    print("=" * 40)

    while True:
        fala_usuario = voz.capturar_voz_ia()

        if not fala_usuario:
            continue

        print(f"\n[Você]: {fala_usuario}")
        print("[Onichan está pensando...]")

        resposta = cerebro.pensar(fala_usuario)
        print(f"[Onichan]: {resposta}\n")

        voz_saida.falar(resposta)


if __name__ == "__main__":
    executar_ia()