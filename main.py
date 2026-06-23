import customtkinter as ctk
import screen_adm  # Sua tela de administração limpa
import screen_page  # Sua tela de atendimento corrigida


def iniciar_sistema():
    ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.geometry("500x400")
    root.title("CineGestão - Inicializador Principal")
    root.resizable(False, False)

    # Centraliza o conteúdo
    frame_central = ctk.CTkFrame(root, fg_color="transparent")
    frame_central.pack(expand=True)

    ctk.CTkLabel(frame_central, text="🎬 CINEGESTÃO", font=("Helvetica", 28, "bold"), text_color="#FFFFFF").pack(
        pady=(0, 10))
    ctk.CTkLabel(frame_central, text="Selecione o módulo de trabalho para iniciar:", font=("Helvetica", 14),
                 text_color="#A0A0A0").pack(pady=(0, 30))

    def ir_para_adm():
        root.destroy()  # Fecha o menu de escolha
        screen_adm.abrir_dashboard()  # Abre a área administrativa

    def ir_para_caixa():
        root.destroy()  # Fecha o menu de escolha
        screen_page.abrir_atendimento()  # Abre a frente de caixa

    btn_adm = ctk.CTkButton(frame_central, text="Acessar Painel ADM", width=300, height=50,
                            font=("Helvetica", 16, "bold"), fg_color="#810000", hover_color="#630000",
                            command=ir_para_adm)
    btn_adm.pack(pady=10)

    btn_caixa = ctk.CTkButton(frame_central, text="Acessar Frente de Caixa", width=300, height=50,
                              font=("Helvetica", 16, "bold"), fg_color="#810000", hover_color="#630000",
                              command=ir_para_caixa)
    btn_caixa.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    iniciar_sistema()