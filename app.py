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
        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 700px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        }
        h1 {
            text-align: center;
            color: #1f3c88;
        }
        p {
            text-align: center;
            color: #555;
        }
        form {
            display: grid;
            gap: 15px;
            margin-top: 25px;
        }
        input, button {
            padding: 12px;
            font-size: 16px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        button {
            background: #1f3c88;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: #16306d;
        }
        .resultado {
            margin-top: 25px;
            padding: 15px;
            background: #eef4ff;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Busca de Passagens e Milhas</h1>
        <p>Pesquise trechos e organize sua viagem</p>

        <form method="POST">
            <input type="text" name="origem" placeholder="Cidade de origem" required>
            <input type="text" name="destino" placeholder="Cidade de destino" required>
            <input type="date" name="data_ida" required>
            <button type="submit">Pesquisar</button>
        </form>

        {% if resultado %}
        <div class="resultado">
            <h3>Pesquisa realizada:</h3>
            <p><strong>Origem:</strong> {{ resultado.origem }}</p>
            <p><strong>Destino:</strong> {{ resultado.destino }}</p>
            <p><strong>Data:</strong> {{ resultado.data_ida }}</p>
            <p>Em breve vamos conectar preços e milhas reais aqui.</p>
        </div>
        {% endif %}
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
            "data_ida": request.form.get("data_ida")
        }
    return render_template_string(HTML, resultado=resultado)
