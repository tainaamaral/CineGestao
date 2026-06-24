# 🎬 CineGestão - Sistema de Gerenciamento de Cinema

O **CineGestão** é uma aplicação desktop desenvolvida em Python para o gerenciamento completo de um cinema. O sistema é dividido em duas frentes principais: um **Painel Administrativo** para o cadastro do catálogo e uma **Frente de Caixa (PDV)** interativa para a venda de ingressos com emissão de bilhete virtual.

## 🚀 Funcionalidades

### 🛡️ Painel Administrativo (`screen_adm.py`)
* **Gestão de Filmes:** Cadastro completo com título, gênero, duração, classificação indicativa e sinopse.
* **Gestão de Salas:** Definição de layout (padrão de 10x8), capacidade total calculada automaticamente e tipo de exibição (IMAX, 3D, VIP, etc).
* **Gestão de Sessões:** Agendamento de horários integrando os filmes às salas reais disponíveis, com definição de preço base.
* **Listagem Dinâmica:** Visualização em tempo real de todos os dados cadastrados no banco.

### 🎟️ Frente de Caixa (`screen_page.py`)
* **Mapa de Assentos Interativo:** Grade gerada dinamicamente baseada na sala escolhida. As poltronas já vendidas são bloqueadas e destacadas em vermelho.
* **Cálculo Automático:** Atualização do valor total em tempo real, suportando descontos (como meia-entrada para estudantes).
* **Emissão de Bilhete:** Geração de um recibo digital na tela estilizado como papel térmico impresso, contendo as informações da sessão, assentos escolhidos e código de barras simulado.

---

## 🏗️ Arquitetura do Sistema (Modularidade)

O projeto foi estruturado seguindo boas práticas de Engenharia de Software, dividido em módulos de alta coesão e baixo acoplamento:

* **`modulo1.py` (Módulo de Catálogo):** Responsável estritamente por manipular entidades estáticas: cadastros de **Filmes** e **Salas**.
* **`modulo2.py` (Módulo de Programação):** Lida com as restrições de tempo e espaço, coordenando o agendamento de **Sessões**.
* **`modulo3.py` (Módulo de Vendas):** Cadastro interno de clientes para programas de
**fidelidade** e no gerenciamento de regras de negócio para aplicação de
**descontos**.
* **`main.py` (Módulo Integrador):** Atua como o orquestrador principal, inicializando o sistema e permitindo a navegação entre as interfaces gráficas sem misturar regras de negócio.

---

## 💻 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica (GUI):** CustomTkinter (biblioteca moderna baseada em Tkinter)
* **Banco de Dados:** SQLite3 (banco relacional embutido para persistência de dados e garantia de integridade com *Foreign Keys*)

---

## 🛠️ Como Executar o Projeto

1. **Clone o repositório:**
   ```
   git clone https://github.com/tainaamaral/CineGestao.git
   
2.  Acesse a pasta do projeto: 
     ```
      cd CineGestão
     ```
3. Instale as dependências necessárias:
O projeto utiliza a biblioteca CustomTkinter para a interface moderna. Instale-a via pip:

   ```
   pip install customtkinter
   ```

4. Inicie o sistema:
Rode o arquivo integrador principal. O banco de dados (banco.db) será criado e configurado automaticamente na primeira execução.

    ```
   python main.py
   ```

## 📸 Telas do Sistema


Menu Principal:

<img width="496" height="430" alt="Screenshot 2026-06-24 at 00 00 49" src="https://github.com/user-attachments/assets/304fdefc-240a-4ce3-83c2-6d2953e26273" />

                   
                   
Painel Administrativo: 

<img width="1249" height="756" alt="Screenshot 2026-06-23 at 21 08 13" src="https://github.com/user-attachments/assets/65b8be68-f1eb-463a-adf2-dd679c25fe63" />


Frente de Caixa (Mapa de Assentos): 

<img width="1246" height="748" alt="Screenshot 2026-06-23 at 21 08 42" src="https://github.com/user-attachments/assets/1e92980a-696c-48be-996d-41b9ee2f4199" />

Bilhete Emitido: 



<img width="453" height="690" alt="Screenshot 2026-06-23 at 21 09 07" src="https://github.com/user-attachments/assets/709581fe-e9d8-4b4e-b1d2-f3b89c3ba434" />

## ✒️ Desenvolvido por Tainá, Lívia e Natália.

