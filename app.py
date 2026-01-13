from flask import Flask, render_template, request, redirect, url_for
from db import get_connection
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# ------------------ Página inicial ------------------
@app.route("/")
def index():
    return render_template("index.html")

# ------------------ Cadastro único de EPI ou EPC ------------------
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        tipo = request.form["tipo"]  # 'epi' ou 'epc'
        nome = request.form["nome"]
        descricao = request.form["descricao"]
       
        

        conn = get_connection()
        cursor = conn.cursor()

        if tipo == "epi":
            quantidade = int(request.form["quantidade"])
            tamanho = request.form["tamanho"]
            cursor.execute(
                "INSERT INTO epi (nome, descricao, quantidade, tamanho) VALUES (%s, %s, %s,%s)",
                (nome, descricao, quantidade, tamanho)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("listar_epis"))

        else:  # EPC
            quantidade = int(request.form["quantidade"])
            local = request.form["local_instalacao"]
            status = request.form["status_epc"]
            

    
            cursor.execute(
                "INSERT INTO epc (nome, descricao, quantidade, local_instalacao, status_epc) VALUES (%s, %s, %s, %s,%s)",
                (nome, descricao, quantidade, local, status,)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("listar_epcs"))

    # GET: exibe o formulário
    return render_template("cadastrar.html")

# ------------------ Listagem de EPI ------------------
@app.route("/epis")
def listar_epis():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, descricao, tamanho, quantidade FROM epi")
    epis = cursor.fetchall()
    conn.close()
    return render_template("listar_epi.html", epis=epis)

# ------------------ Listagem de EPC ------------------
@app.route("/epcs")
def listar_epcs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, descricao, quantidade, local_instalacao, status_epc FROM epc")
    epcs = cursor.fetchall()
    conn.close()
    return render_template("listar_epc.html", epcs=epcs)


#------------------- Função PDF EPI-------------------
@app.route("/relatorio/epis")
def relatorio_epis():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nome, descricao, tamanho, quantidade FROM epi")
    epis = cursor.fetchall()
    conn.close()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    largura, altura = A4
    y = altura - 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Relatório de Estoque - EPIs")

    y -= 30
    pdf.setFont("Helvetica", 10)

    for epi in epis:
        texto = f"Nome: {epi['nome']} | descricao: {epi['descricao']} | tamanho: {epi['tamanho']} | Qtde: {epi['quantidade']}"
        pdf.drawString(40, y, texto)
        y -= 20

        if y < 40:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = altura - 40

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="relatorio_epis.pdf",
        mimetype="application/pdf"
    )

#------------------- Função PDF EPC-------------------

@app.route("/relatorio/epcs")
def relatorio_epcs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT nome, descricao, status_epc, quantidade 
        FROM epc
    """)
    epcs = cursor.fetchall()
    conn.close()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    largura, altura = A4
    y = altura - 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Relatório de EPCs")

    y -= 30
    pdf.setFont("Helvetica", 10)

    for epc in epcs:
        texto = (
        f"Nome: {epc['nome']} | "
         f"Descrição: {epc['descricao']} | "
         f"Status: {epc['status_epc']} | "
         f"Quantidade: {epc['quantidade']}"
        
        )
        pdf.drawString(40, y, texto)
        y -= 20

        if y < 40:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = altura - 40

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="relatorio_epcs.pdf",
        mimetype="application/pdf"
    )

# ------------------ Apagar intem ------------------
@app.route("/epc/excluir/<int:id>")
def excluir_epc(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM epc WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("listar_epcs"))

@app.route("/epi/excluir/<int:id>")
def excluir_epi(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM epi WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("listar_epis"))



# ------------------ Editar EPI ------------------
@app.route("/epi/editar/<int:id>", methods=["GET", "POST"])
def editar_epi(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        quantidade = int(request.form["quantidade"])

        cursor.execute(
            "UPDATE epi SET quantidade = %s WHERE id = %s",
            (quantidade, id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("listar_epis"))

    # GET → buscar dados do EPI
    cursor.execute("SELECT * FROM epi WHERE id = %s", (id,))
    epi = cursor.fetchone()
    conn.close()

    return render_template("editar_epi.html", epi=epi)
#-------------------Editar EPC-------------
@app.route("/epc/editar/<int:id>", methods=["GET", "POST"])
def editar_epc(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        quantidade = int(request.form["quantidade"])

        cursor.execute(
            "UPDATE epc SET quantidade = %s WHERE id = %s",
            (quantidade, id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("listar_epcs"))

    # GET → buscar EPC atual
    cursor.execute("SELECT * FROM epc WHERE id = %s", (id,))
    epc = cursor.fetchone()
    conn.close()

    return render_template("editar_epc.html", epc=epc)


# ------------------ Start Flask ------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
