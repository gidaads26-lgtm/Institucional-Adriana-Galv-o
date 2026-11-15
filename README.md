# Site institucional | Adriana Galvão

Site de uma página da Adriana Galvão, hipnoterapeuta clínica e neuropsicopedagoga em Guarulhos/SP.

## Arquivos

- `index.html`: o site pronto, com CSS, JavaScript e fotos embutidos. É só publicar este arquivo.
- `og-image.jpg`: imagem de compartilhamento (1200×630). Precisa ficar na mesma pasta do `index.html` no servidor.
- `fonte/`: arquivos usados para gerar o `index.html`.
  - `template.html`: estrutura, estilos e scripts do site.
  - `build.py`: preenche o template com os dados, os ícones e as fotos (em base64).
  - `tinta.py`: gera a textura de aquarela com folhas de ouro (`fotos/tinta.jpg`).
  - `fotos/`: `hero.jpg`, `sobre.jpg` e `tinta.jpg`. Adicione `consultorio.jpg` quando tiver a foto.

## Como atualizar

1. Edite os dados no topo de `fonte/build.py` (domínio, endereço, depoimentos) ou os textos em `fonte/template.html`.
2. Coloque as fotos novas em `fonte/fotos/` com os mesmos nomes.
3. Rode `python3 build.py` dentro da pasta `fonte` (precisa do Pillow). O `index.html` da raiz é gerado de novo.

O número do WhatsApp fica na constante `WHATSAPP` no script do `index.html` (e do `template.html`).

## Publicar no GitHub Pages

Em Settings > Pages, escolha a branch `main` e a pasta raiz. Depois de definir o domínio, atualize `DOMINIO` no `build.py` e gere o site de novo, para que a imagem de compartilhamento e as tags de SEO apontem para o endereço certo.

## Pendências

- Foto do consultório, endereço completo e CEP
- Domínio definitivo
- Depoimentos reais e autorizados
