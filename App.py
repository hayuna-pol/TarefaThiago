from shiny import App, ui, reactive, render

# Dados dos desenhos: nome e preço
# Usamos reactive.Value para que as alterações nesta lista sejam reativas e atualizem a UI
desenhos_data = reactive.Value([
    {"name": "Gato Espacial", "price": 10.00},
    {"name": "Dragão Azul", "price": 12.50},
    {"name": "Unicórnio Pixelado", "price": 8.00},
    {"name": "Robô Retro", "price": 15.00},
    {"name": "Floresta Mágica", "price": 9.99}
])

# Definição da interface do usuário (UI) do aplicativo
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel(
            "Loja",
            # O estilo 'padding' foi movido para um ui.div que envolve o conteúdo da aba
            ui.div(
                ui.h3("Loja de Desenhos"),
                # Agora, a renderização dos cards da loja será feita por uma função de saída reativa
                ui.output_ui("shop_cards"),
                ui.input_action_button("comprar", "Comprar Selecionados", class_="btn-primary"),
                ui.hr(),
                ui.output_text("compra_status"),
                style="padding: 20px;" # Estilo aplicado ao conteúdo dentro do painel
            )
        )
        # A aba "Contador" foi removida daqui
    ),
    fillable=True
)

# Definição da lógica do servidor
def server(input, output, session):
    # Variável reativa para armazenar os itens comprados
    compras = reactive.Value([])

    # As variáveis reativas e efeitos relacionados ao contador foram removidos

    @output
    @render.ui
    def shop_cards():
        """
        Renderiza os cards dos desenhos disponíveis na loja.
        Esta função é um output reativo, permitindo que acesse desenhos_data.get()
        dentro de um contexto reativo.
        """
        current_desenhos = desenhos_data.get() # Acessa os dados dos desenhos dentro do contexto reativo
        cards = []
        # Para cada desenho na lista atual, cria um card
        for desenho in current_desenhos: # Iterar diretamente sobre o objeto, não o índice
            cards.append(
                ui.card(
                    # Imagem de placeholder para o desenho
                    ui.tags.img(
                        src=f"https://placehold.co/200x150/ADD8E6/000000?text={desenho['name'].replace(' ', '+')}",
                        style="width: 100%; height: auto; border-radius: 8px; margin-bottom: 10px;"
                    ),
                    ui.h4(desenho['name']), # Nome do desenho
                    ui.p(f"Preço: R${desenho['price']:.2f}"), # Preço do desenho
                    # O ID do checkbox agora usa o nome do desenho para ser único e persistente
                    ui.input_checkbox(f"check_{desenho['name'].replace(' ', '_')}", label="Selecionar"),
                    ui.p("Um incrível desenho para colorir!"), # Descrição do desenho
                    style="margin-bottom: 15px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" # Estilo do card
                )
            )
        # Retorna o layout de colunas com os cards
        return ui.layout_column_wrap(width="300px", *cards)


    @output
    @render.text
    @reactive.event(input.comprar) # Dispara quando o botão 'comprar' é clicado
    def compra_status():
        selecionados_nomes = []
        valor_total_compra = 0.0
        current_desenhos = desenhos_data.get() # Obter a lista atual de desenhos
        desenhos_restantes = [] # Lista para armazenar os desenhos que não foram comprados

        # Itera sobre os desenhos atuais para verificar quais foram selecionados
        for desenho in current_desenhos:
            # O ID do checkbox agora usa o nome do desenho
            checkbox_id = f"check_{desenho['name'].replace(' ', '_')}"
            # Verifica se o checkbox existe e se foi marcado
            if checkbox_id in input and input[checkbox_id]():
                selecionados_nomes.append(desenho['name'])
                valor_total_compra += desenho['price']
            else:
                desenhos_restantes.append(desenho) # Adiciona à lista de restantes se não foi comprado

        if selecionados_nomes:
            # Atualiza a lista de desenhos disponíveis na loja
            desenhos_data.set(desenhos_restantes)

            # Adiciona os nomes dos desenhos comprados à lista de compras (se necessário para outra funcionalidade)
            lista_compras_atual = compras.get()
            nova_lista_compras = lista_compras_atual + selecionados_nomes
            compras.set(nova_lista_compras)

            return f"Você comprou: {', '.join(selecionados_nomes)} por R${valor_total_compra:.2f} 🎨"
        else:
            return "Nenhum desenho selecionado."

# Cria a instância do aplicativo Shiny
app = App(app_ui, server)
