from flask import Flask, render_template, request, redirect, url_for
from db import get_connection
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from sqlalchemy import text





app = Flask(__name__)

# ------------------ Página inicial ------------------
@app.route("/")
def index():
    return render_template("index.html")

# ------------------ Cadastro único de EPI ou EPC ------------------

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        tipo = request.form["tipo"]
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        conn = get_connection()

        try:
            if tipo == "epi":
                quantidade = int(request.form["quantidade"])
                tamanho = request.form["tamanho"]

                conn.execute(
                    text("""
                        INSERT INTO epi (nome, descricao, quantidade, tamanho)
                        VALUES (:nome, :descricao, :quantidade, :tamanho)
                    """),
                    {
                        "nome": nome,
                        "descricao": descricao,
                        "quantidade": quantidade,
                        "tamanho": tamanho
                    }
                )

                conn.commit()
                return redirect(url_for("listar_epis"))

            else:  # EPC
                quantidade = int(request.form["quantidade"])
                local = request.form["local_instalacao"]
                status = request.form["status_epc"]

                conn.execute(
                    text("""
                        INSERT INTO epc (nome, descricao, quantidade, local_instalacao, status_epc)
                        VALUES (:nome, :descricao, :quantidade, :local, :status)
                    """),
                    {
                        "nome": nome,
                        "descricao": descricao,
                        "quantidade": quantidade,
                        "local": local,
                        "status": status
                    }
                )

                conn.commit()
                return redirect(url_for("listar_epcs"))

        finally:
            conn.close()

    return render_template("cadastrar.html")

# ------------------ Listagem de EPI ------------------
@app.route("/epis")
def listar_epis():
    conn = get_connection()
    result = conn.execute(text("SELECT id, nome, descricao, tamanho, quantidade FROM epi"))
    epis = [dict(row._mapping) for row in result]
    conn.close()

    return render_template("listar_epi.html", epis=epis)

# ------------------ Listagem de EPC ------------------
@app.route("/epcs")
def listar_epcs():
    conn = get_connection()
    result = conn.execute(text("SELECT id, nome, descricao, quantidade, local_instalacao, status_epc FROM epc"))
    epcs = [dict(row._mapping) for row in result]
    conn.close()
    return render_template("listar_epc.html", epcs=epcs)


#------------------- Função PDF EPI-------------------
@app.route("/relatorio/epis")
def relatorio_epis():
    conn = get_connection()

    try:
        result = conn.execute(
            text("SELECT nome, descricao, tamanho, quantidade FROM epi")
        )
        epis = result.mappings().all()
    finally:
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

    return send_file(buffer, as_attachment=True,
                     download_name="relatorio_epis.pdf",
                     mimetype="application/pdf")

#------------------- Função PDF EPC-------------------

@app.route("/relatorio/epcs")
def relatorio_epcs():
    conn = get_connection()

    try:
        result = conn.execute(
            text("SELECT nome, descricao, status_epc, quantidade FROM epc")
        )
        epcs = result.mappings().all()
    finally:
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
    try:
        conn.execute(
            text("DELETE FROM epc WHERE id = :id"),
            {"id": id}
        )
        conn.commit()
        return redirect(url_for("listar_epcs"))
    finally:
        conn.close()


# ------------------ Editar EPI ------------------
@app.route("/epi/editar/<int:id>", methods=["GET", "POST"])
def editar_epi(id):
    conn = get_connection()

    try:
        if request.method == "POST":
            quantidade = int(request.form["quantidade"])

            conn.execute(
                text("UPDATE epi SET quantidade = :q WHERE id = :id"),
                {"q": quantidade, "id": id}
            )
            conn.commit()
            return redirect(url_for("listar_epis"))

        result = conn.execute(
            text("SELECT * FROM epi WHERE id = :id"),
            {"id": id}
        )

        epi = result.mappings().first()
        return render_template("editar_epi.html", epi=epi)

    finally:
        conn.close()
#-------------------Editar EPC-------------
@app.route("/epc/editar/<int:id>", methods=["GET", "POST"])
def editar_epc(id):
    conn = get_connection()

    try:
        if request.method == "POST":
            quantidade = int(request.form["quantidade"])

            conn.execute(
                text("UPDATE epc SET quantidade = :q WHERE id = :id"),
                {"q": quantidade, "id": id}
            )
            conn.commit()
            return redirect(url_for("listar_epcs"))

        result = conn.execute(
            text("SELECT * FROM epc WHERE id = :id"),
            {"id": id}
        )

        epc = result.mappings().first()
        return render_template("editar_epc.html", epc=epc)

    finally:
        conn.close()


# ------------------ Start Flask ------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


