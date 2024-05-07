import os


def add_path_comment(root_path):
    # Caminhar pelos diretórios a partir do diretório raiz
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            # Checa se o arquivo é Python e não é __init__.py
            if filename.endswith('.py') and filename != '__init__.py':
                filepath = os.path.join(dirpath, filename)
                # Calcula o caminho relativo para uso no comentário
                relative_path = os.path.relpath(filepath, start=root_path)
                comment = f'# {relative_path}\n'

                # Ler o conteúdo original do arquivo
                with open(filepath, 'r') as file:
                    lines = file.readlines()

                # Remove o comentário da primeira linha se existir
                if lines and lines[0].startswith('#'):
                    lines = lines[1:]

                # Adiciona o comentário no início e escreve de volta no arquivo
                with open(filepath, 'w') as file:
                    file.write(comment + ''.join(lines))


# Chame a função com o diretório raiz onde os arquivos Python estão localizados
add_path_comment('./')
