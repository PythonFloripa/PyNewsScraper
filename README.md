# PyNewsScraper

Este projeto é um scraper (raspador de dados) para verificar as bibliotecas Python que tiveram atualização no último mês e listá-las, facilitando a identificação de bibliotecas com lançamentos de versão major.

Este Scraper utiliza IA para que não seja necessário a sua atualização constante

# Como utilizar

## Instalação do Docker e Docker Compose

### Ubuntu

1. **Instale o Docker:**

    https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

2. **Instale o Docker Compose:**

    https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04


### Windows

1. **Instale o Docker:**

    https://docs.docker.com/desktop/setup/install/windows-install/

2. **Instale o Docker Compose:**

    https://docs.docker.com/compose/install/


### Crie uma chave GEMINI API junto a Google

- https://aistudio.google.com/
<p>

Atualize o valor em jeannie.py
```
...
GOOGLE_API_KEY = "<YOUR-API-KEY>"
...
```

## Construa o container
```sh
docker compose build
```

## Para procurar por releases, execute o comando abaixo e aguarde as instruções
```
docker compose run --rm --remove-orphans pynews python3 /app/app/getNews.py releases
```

## Para criar os resumos, execute
```
docker compose run --rm --remove-orphans pynews python3 /app/app/getNews.py slides
```
<p>
<p>
<p>

## Esse é um script que depende da COHERE AI, essa IA assim como todas as outras, ainda não apresentam comportamento estável, portanto esse script deve ser usado sob supervisão

## DeepSeek "This model's maximum context length is 65536 tokens"
