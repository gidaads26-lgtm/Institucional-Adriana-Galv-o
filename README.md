# Site institucional | Adriana Galvão

Site de uma página da Adriana Galvão, hipnoterapeuta clínica e neuropsicopedagoga em Guarulhos/SP.

## Arquivos

- `index.html`: o site pronto, com CSS, JavaScript e fotos embutidos. É só publicar este arquivo.
- `og-image.jpg`: imagem que aparece ao compartilhar o link no WhatsApp, Instagram, Facebook e LinkedIn (1200×630). Precisa ficar na mesma pasta do `index.html`.
- `apple-touch-icon.png` e `favicon-32.png`: ícones do site e da tela inicial do celular.
- `fonte/`: arquivos usados para gerar o `index.html`.
  - `template.html`: estrutura, estilos e scripts do site.
  - `build.py`: preenche o template com os dados, os ícones e as fotos (em base64).
  - `tinta.py`: gera a textura de aquarela com folhas de ouro (`fotos/tinta.jpg`).
  - `imagem_compartilhamento.py`: gera a `og-image.jpg` (precisa de Playwright com Chrome e das fontes Newsreader e Jost instaladas).
  - `fotos/`: `hero.jpg`, `sobre.jpg` e `tinta.jpg`. Adicione `consultorio.jpg` quando tiver a foto.

## Como atualizar

1. Edite os dados no topo de `fonte/build.py` (domínio, endereço, depoimentos) ou os textos em `fonte/template.html`.
2. Coloque as fotos novas em `fonte/fotos/` com os mesmos nomes.
3. Rode `python3 build.py` dentro da pasta `fonte` (precisa do Pillow). O `index.html` da raiz é gerado de novo.

O número do WhatsApp fica na constante `WHATSAPP` no script do `index.html` (e do `template.html`).

## Publicação

O site está em https://institucionaladrianagalvao.vercel.app/ e o `DOMINIO` do `build.py` já aponta para esse endereço. Se mudar para um domínio próprio, troque o `DOMINIO` e gere o site de novo, para que a imagem de compartilhamento e as tags de SEO apontem para o endereço certo.

O WhatsApp e o Facebook guardam a prévia do link por um tempo. Para conferir uma mudança na imagem, use o depurador do Facebook (https://developers.facebook.com/tools/debug/) e clique em "Extrair novamente". Quando a imagem mudar, troque o `?v=2` das tags `og:image` no `template.html`.

## Pendências

- Foto do consultório, endereço completo e CEP
- Depoimentos reais e autorizados
