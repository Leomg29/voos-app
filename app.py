from flask import Flask, request, render_template_string
from datetime import datetime, date

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Passagens e Milhas</title>
    <style>
        * { box-sizing: border-box; }

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
            max-width: 1120px;
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

        .faixa {
            margin-top: 16px;
            padding: 14px;
            border-radius: 12px;
            background: #eaf2ff;
            color: #16306d;
            font-weight: bold;
        }

        .cards-voos {
            margin-top: 24px;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 16px;
        }

        .voo {
            background: white;
            border: 1px solid #dbeafe;
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05);
            position: relative;
        }

        .voo h3 {
            margin-top: 0;
            color: #1e3a8a;
            font-size: 22px;
        }

        .linha {
            margin: 8px 0;
            font-size: 15px;
        }

        .preco {
            margin-top: 14px;
            padding: 10px 12px;
            border-radius: 12px;
            background: #eff6ff;
            font-weight: bold;
            color: #16306d;
        }

        .milhas {
            margin-top: 10px;
            padding: 10px 12px;
            border-radius: 12px;
            background: #ecfdf5;
            font-weight: bold;
            color: #065f46;
        }

        .tag {
            display: inline-block;
            margin-top: 10px;
            background: #dbeafe;
            color: #1d4ed8;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: bold;
        }

        .selo {
            position: absolute;
            top: 14px;
            right: 14px;
            background: #16a34a;
            color: white;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: bold;
        }

        .rodape {
            text-align: center;
            font-size: 13px;
            color: #64748b;
            margin-top: 18px;
        }

        @media (max-width: 900px) {
            .cards-voos {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 700px) {
            .grid, .grid-3, .resumo {
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
        <p>Pesquise e compare opções da sua próxima viagem</p>
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

                <div class="campo" style="margin-top:16px;">
                    <label>Priorizar</label>
                    <select name="prioridade">
                        <option value="menor_preco">Menor preço em dinheiro</option>
                        <option value="menor_milhas">Menor valor em milhas</option>
                        <option value="custo_beneficio">Melhor custo-benefício</option>
                        <option value="mais_rapido">Mais rápido</option>
                    </select>
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
                        <strong>Prioridade</strong>
                        {{ resultado.prioridade_label }}
                    </div>
                </div>

                <div class="faixa">
                    Melhor opção escolhida com base em: {{ resultado.prioridade_label }}.
                </div>

                <div class="cards-voos">
                    {% for voo in voos %}
                    <div class="voo">
                        {% if voo.melhor %}
                        <div class="selo">Melhor opção</div>
                        {% endif %}

                        <h3>{{ voo.companhia }}</h3>
                        <div class="linha"><strong>Rota:</strong> {{ resultado.origem }} → {{ resultado.destino }}</div>
                        <div class="linha"><strong>Saída:</strong> {{ resultado.data_ida }}</div>
                        <div class="linha"><strong>Cabine:</strong> {{ resultado.cabine }}</div>
                        <div class="linha"><strong>Bagagem:</strong> {{ voo.bagagem }}</div>
                        <div class="linha"><strong>Escalas:</strong> {{ voo.escalas }}</div>
                        <div class="linha"><strong>Duração:</strong> {{ voo.duracao }}</div>

                        <div class="preco">Preço em dinheiro: {{ voo.preco }}</div>
                        <div class="milhas">Preço em milhas: {{ voo.milhas }}</div>
                        <div class="tag">{{ voo.tag }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <div class="rodape">
                Versão online no Render • filtro inteligente ativo
            </div>
        </div>
    </div>
</body>
</html>
"""

def calcular_fator_antecedencia(dias):
    if dias >= 180:
        return 0.78
    if dias >= 120:
        return 0.88
    if dias >= 90:
        return 0.96
    if dias >= 60:
        return 1.05
    if dias >= 30:
        return 1.18
    if dias >= 15:
        return 1.35
    return 1.60

def calcular_fator_cabine(cabine):
    fatores = {
        "Econômica": 1.0,
        "Premium Economy": 1.45,
        "Executiva": 2.4,
        "Primeira Classe": 4.0
    }
    return fatores.get(cabine, 1.0)

def formatar_reais(valor):
    texto = f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"

def formatar_milhas(valor):
    texto = f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{texto} milhas + taxas"

def duracao_para_minutos(texto):
    horas = 0
    minutos = 0
    if "h" in texto:
        partes = texto.split("h")
        horas = int(partes[0].strip())
        resto = partes[1].replace("min", "").strip()
        if resto:
            minutos = int(resto)
    return horas * 60 + minutos

def prioridade_label(valor):
    labels = {
        "menor_preco": "Menor preço em dinheiro",
        "menor_milhas": "Menor valor em milhas",
        "custo_beneficio": "Melhor custo-benefício",
        "mais_rapido": "Mais rápido"
    }
    return labels.get(valor, "Menor preço em dinheiro")

@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None
    voos = []

    if request.method == "POST":
        origem = request.form.get("origem")
        destino = request.form.get("destino")
        data_ida = request.form.get("data_ida")
        data_volta = request.form.get("data_volta")
        adultos = int(request.form.get("adultos"))
        criancas = int(request.form.get("criancas"))
        cabine = request.form.get("cabine")
        prioridade = request.form.get("prioridade")

        try:
            ida_date = datetime.strptime(data_ida, "%Y-%m-%d").date()
            hoje = date.today()
            antecedencia = (ida_date - hoje).days
            if antecedencia < 0:
                antecedencia = 0
        except:
            antecedencia = 0

        fator_antecedencia = calcular_fator_antecedencia(antecedencia)
        fator_cabine = calcular_fator_cabine(cabine)
        passageiros_equivalentes = adultos + (criancas * 0.75)

        base_latam = 920
        base_gol = 870
        base_azul = 980

        milhas_latam = 28000
        milhas_gol = 25500
        milhas_azul = 30000

        preco_latam = base_latam * fator_antecedencia * fator_cabine * passageiros_equivalentes
        preco_gol = base_gol * fator_antecedencia * fator_cabine * passageiros_equivalentes
        preco_azul = base_azul * fator_antecedencia * fator_cabine * passageiros_equivalentes

        fator_milhas = 1 + ((fator_cabine - 1) * 0.9)

        milhas_total_latam = milhas_latam * fator_antecedencia * fator_milhas * passageiros_equivalentes
        milhas_total_gol = milhas_gol * fator_antecedencia * fator_milhas * passageiros_equivalentes
        milhas_total_azul = milhas_azul * fator_antecedencia * fator_milhas * passageiros_equivalentes

        dados_voos = [
            {
                "companhia": "LATAM",
                "bagagem": "1 bagagem de mão",
                "escalas": "Sem escalas",
                "duracao": "2h 15min",
                "preco_num": preco_latam,
                "milhas_num": milhas_total_latam,
                "tag": "Melhor tempo"
            },
            {
                "companhia": "GOL",
                "bagagem": "1 bagagem de mão",
                "escalas": "1 escala",
                "duracao": "3h 05min",
                "preco_num": preco_gol,
                "milhas_num": milhas_total_gol,
                "tag": "Melhor custo"
            },
            {
                "companhia": "Azul",
                "bagagem": "Bagagem de mão + item pessoal",
                "escalas": "Sem escalas",
                "duracao": "2h 35min",
                "preco_num": preco_azul,
                "milhas_num": milhas_total_azul,
                "tag": "Mais confortável"
            }
        ]

        for voo in dados_voos:
            voo["duracao_min"] = duracao_para_minutos(voo["duracao"])
            voo["score_cb"] = (voo["preco_num"] / 100) + (voo["milhas_num"] / 10000) + (voo["duracao_min"] / 100)

        if prioridade == "menor_preco":
            melhor_valor = min(voo["preco_num"] for voo in dados_voos)
            for voo in dados_voos:
                voo["melhor"] = voo["preco_num"] == melhor_valor

        elif prioridade == "menor_milhas":
            melhor_valor = min(voo["milhas_num"] for voo in dados_voos)
            for voo in dados_voos:
                voo["melhor"] = voo["milhas_num"] == melhor_valor

        elif prioridade == "mais_rapido":
            melhor_valor = min(voo["duracao_min"] for voo in dados_voos)
            for voo in dados_voos:
                voo["melhor"] = voo["duracao_min"] == melhor_valor

        else:
            melhor_valor = min(voo["score_cb"] for voo in dados_voos)
            for voo in dados_voos:
                voo["melhor"] = voo["score_cb"] == melhor_valor

        for voo in dados_voos:
            voo["preco"] = formatar_reais(voo["preco_num"])
            voo["milhas"] = formatar_milhas(voo["milhas_num"])

        voos = dados_voos

        resultado = {
            "origem": origem,
            "destino": destino,
            "data_ida": data_ida,
            "data_volta": data_volta,
            "adultos": adultos,
            "criancas": criancas,
            "cabine": cabine,
            "prioridade_label": prioridade_label(prioridade)
        }

    return render_template_string(HTML, resultado=resultado, voos=voos)

if __name__ == "__main__":
    app.run(debug=True)
