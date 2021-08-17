import os
from flask import Flask

from kenzie.upload import upload
from kenzie.files import list_files, download, download_dir_as_zip

app = Flask(__name__)
app.config['FILE_DIRECTORY'] = os.environ.get('FILE_DIRECTORY')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


@app.route('/upload', methods=["POST"])
def upload_file():

    """
    Endpoint responsável por fazer upload de imagens.

    :return: Response
    """

    return upload(app)


@app.route('/files')
@app.route('/files/<type>')
def files(type=None):
    """
    Endpoint responsável por retornar todos os arquivos ou arquivos em especifico no diretório upload.

    :param type: Tipo do arquivo
    :return: Response
    """

    return list_files(app, type)


@app.route('/download/<filename>')
def download_file(filename):

    """
    Endpoint responsável por fazer download lado do cliente de algum arquivo específico.

    :param filename: Nome do arquivo
    :return: Response
    """

    return download(app, filename)


@app.route("/download-zip")
def download_zip():

    """
    Endpoint responsável por fazer download de arquivos em especifico comprimidos.

    :return: Response
    """

    return download_dir_as_zip(app)


if __name__ == '__main__':
    app.run()
