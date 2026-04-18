from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Passagens e Milhas</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(180deg, #eef3ff 0%, #f7f9fc 100%);
            color: #1f2937;
        }

        .topo {
            background: #1e3a8a;
            color: white;
            padding: 22px 16px;
            text-align: center;
        }

        .topo h1 {
            margin: 0;
            font-size: 32px;
        }

        .topo p {
            margin: 8px 0 0;
            font-size: 16px;
            opacity: 0.95;
        }

        .container {
            max-width: 950px;
            margin: 30px auto;
            padding: 16px;
        }

        .card {
            background: white;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
            padding: 22px;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 16px;
        }

        .campo {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 14px;
            margin-bottom: 6px;
            font-weight: bold;
            color: #334155;
        }

        input, select, button {
            padding: 13px 14px;
            border-radius: 12px;
            border: 1px solid #cbd5e1;
            font-size: 16px;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #1e40af;
        }

        .btn {
            background: #1e40af;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
            margin-top: 18px;
        }

        .btn:hover {
            background: #1b378f;
        }

        .resultado {
            margin-top: 24px;
            background: #f8fbff;
            border: 1px solid #dbeafe;
            border-radius: 18px;
            padding: 20px;
        }

        .resultado h2 {
            margin-top: 0;
            color: #1e3a8a;
        }

        .resumo {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 12px;
        }

        .item {
            background: white;
            border-radius: 12px;
            padding: 14px;
            border: 1px solid #e5e7eb;
        }

        .item strong {
            display: block;
            color: #0f172a;
            margin-bottom: 6px;
        }

        .destaque {
            margin-top: 16px;
            background: #e0edff;
            color: #16306d;
            border-radius: 12px;
            padding: 14px;
            font-weight: bold;
        }

        .rodape {
            text-align: center;
            font-size: 13px;
            color: #64748b;
            margin-top: 18px;
        }

        @media (max-width: 700px) {
            .grid,
            .grid-3,
            .resumo {
                grid-template-columns: 1fr;
            }

            .topo h1 {
                font-size: 26px;
            }

            .card {
                padding: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="topo">
        <h1>Passagens e Milhas</h1>
        <p>Pesquise e organize sua próxima viagem</p>
    </div>

    <div class="container">
        <div class="card">
            <form method="POST">
                <div class="grid">
                    <div class="campo">
                        <label>Origem</label>
                        <input type="text" name="origem" placeholder="Ex: Belo Horizonte" required>
                    </div>
                    <div class="campo">
                        <label>Destino</label>
                        <input type="text" name="destino" placeholder="Ex: Salvador" required>
                    </div>
                </div>

                <div class="grid">
                    <div class="campo">
                        <label>Data de ida</label>
                        <input type="date" name="data_ida" required>
                    </div>
                    <div class="campo">
                        <label>Data de volta</label>
                        <input type="date" name="data_volta">
                    </div>
                </div>

                <div class="grid-3">
                    <div class="campo">
                        <label>Adultos</label>
                        <select name="adultos">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </div>

                    <div class="campo">
                        <label>Crianças</label>
                        <select name="criancas">
                            <option value="0">0</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                        </select>
                    </div>

                    <div class="campo">
                        <label>Cabine</label>
                        <select name="cabine">
                            <option value="Econômica">Econômica</option>
                            <option value="Premium Economy">Premium Economy</option>
                            <option value="Executiva">Executiva</option>
                            <option value="Primeira Classe">Primeira Classe</option>
                        </select>
                    </div>
                </div>

                <button class="btn" type="submit">Pesquisar viagem</button>
            </form>

            {% if resultado %}
            <div class="resultado">
                <h2>Resumo da pesquisa</h2>

                <div class="resumo">
                    <div class="item">
                        <strong>Trecho</strong>
                        {{ resultado.origem }} → {{ resultado.destino }}
                    </div>

                    <div class="item">
                        <strong>Cabine</strong>
                        {{ resultado.cabine }}
                    </div>

                    <div class="item">
                        <strong>Ida</strong>
                        {{ resultado.data_ida }}
                    </div>

                    <div class="item">
                        <strong>Volta</strong>
                        {{ resultado.data_volta if resultado.data_volta else "Somente ida" }}
                    </div>

                    <div class="item">
                        <strong>Passageiros</strong>
                        {{ resultado.adultos }} adulto(s) e {{ resultado.criancas }} criança(s)
                    </div>

                    <div class="item">
                        <strong>Status</strong>
                        Pesquisa registrada com sucesso
                    </div>
                </div>

                <div class="destaque">
                    Próxima etapa: conectar preços e milhas reais, comparar opções e exibir resultados em cards.
                </div>
            </div>
            {% endif %}

            <div class="rodape">
                Versão inicial online no Render
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None

    if request.method == "POST":
        resultado = {
            "origem": request.form.get("origem"),
            "destino": request.form.get("destino"),
            "data_ida": request.form.get("data_ida"),
            "data_volta": request.form.get("data_volta"),
            "adultos": request.form.get("adultos"),
            "criancas": request.form.get("criancas"),
            "cabine": request.form.get("cabine")
        }

    return render_template_string(HTML, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
