import os
import string
from random import sample

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def gerar_senha_aleatoria(tamanho: int) -> str:
    senha = "".join(sample(string.ascii_letters + string.digits, tamanho))
    return senha


# Função para converter URLs relativos em caminhos absolutos do sistema (para gerar pdf)
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """

    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # make sure that file exists
    # if not os.path.isfile(path):
    #     raise Exception(
    #         f'media URI must start with {sUrl} or {mUrl}'
    #     )

    return path


def exportar_pdf(nome_exame, paciente, senha) -> HttpResponse:
    """
    Gera um arquivo PDF contendo o nome do exame, o nome paciente e a senha.
    """
    template_path = "pdf_senha_exame.html"
    context = {
        "exame": nome_exame,
        "paciente": paciente,
        "senha": senha,
    }
    response = HttpResponse(content="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Senha - {paciente.get_full_name()}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        src=html,
        dest=response,
        link_callback=link_callback,
    )
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response
