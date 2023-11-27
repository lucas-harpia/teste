import requests


logs = []


def add_log(messages):
    """Adiciona uma mensagem à lista de logs."""
    logs.append(messages)


def send_telegram_message(text: object) -> object:
    token = "6432441599:AAFIc2mDZCCKvOQ9NCcruFtq1jcHocwaZa0"
    chat_id = "-4063647216"
    base_url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(base_url, data=data)
    if response.status_code == 200:
        return "Mensagem enviada com sucesso!"
    else:
        return f"Erro ao enviar mensagem: {response.text}"


def send_all_logs():
    """Envia todos os logs acumulados para o Telegram."""
    formatted_message = "\n".join(logs)
    send_telegram_message(formatted_message)

send_all_logs()