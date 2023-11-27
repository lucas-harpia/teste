import httpx
import os
from tqdm import tqdm
from zipfile import ZipFile
from src.estabelecimento.formatar_arquivo import formatar_arquivo
from src.telegram import add_log, send_all_logs

httpx_client = httpx.Client()


def download_and_extract(url, dest_filename, max_attempts=3):
    add_log(f'Começando Download da Fonte de dados: {url}\n')

    for attempt in range(1, max_attempts + 1):
        try:
            with httpx_client.stream("GET", url, timeout=3600) as response:
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))

                with open(dest_filename, 'wb') as file, tqdm(
                        desc=dest_filename,
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                ) as bar:
                    for data in response.iter_bytes():
                        file.write(data)
                        bar.update(len(data))

                add_log('Download concluído com sucesso.\n')

                script_dir = os.path.dirname(os.path.abspath(__file__))
                extract_path = os.path.join(script_dir, '.zip', '')

                with ZipFile(dest_filename, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                add_log(f'Arquivo extraído.\n')

                # Obtém a lista de arquivos extraídos
                extracted_files = os.listdir(extract_path)

                for file in extracted_files:
                    original_path = os.path.join(extract_path, file)
                    new_name = os.path.join('arquivo_atualizacao.txt')
                    os.rename(original_path, new_name)
                    formatar_arquivo(new_name)

                os.remove(dest_filename)

                return extract_path
        except httpx.ReadTimeout:
            if attempt < max_attempts:
                add_log(f"Tentativa {attempt} de {max_attempts} falhou. Tentando novamente.\n")
                send_all_logs()
            else:
                add_log(f"Até {max_attempts} tentativas falharam. Abortando.\n")
                send_all_logs()
                raise
        except Exception as e:
            add_log(f"Erro desconhecido: {e}\n")
            send_all_logs()
            raise
