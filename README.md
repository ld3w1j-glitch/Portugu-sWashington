# Gramática em Análise

Sistema didático para estudar classes gramaticais, funções sintáticas e
morfossintaxe. Funciona no navegador, mas o processamento e os dados ficam no
próprio computador.

## O que já está incluído

- analisador palavra por palavra;
- dez classes gramaticais com cores e explicações;
- identificação didática de sujeito, predicado, complementos e adjuntos;
- indicação de confiança e de classificações alternativas;
- curso progressivo com 26 aulas;
- 42 exercícios iniciantes, intermediários e avançados;
- filtros por assunto e revisão das questões erradas;
- folha A4 econômica e opção de imprimir com gabarito;
- histórico pesquisável, exclusão individual e backup em JSON;
- regência, voz verbal, locuções e classificação detalhada das orações;
- layout responsivo para computador e celular;
- funcionamento offline depois da instalação inicial;
- configuração pronta para Railway.

## Iniciar no Windows

1. Extraia todo o ZIP para uma pasta.
2. Dê dois cliques em `iniciar.bat`.
3. Na primeira execução, aguarde a instalação dos componentes.
4. O navegador abrirá em `http://127.0.0.1:5000`.

É necessário ter Python 3.10 ou superior. Durante a instalação do Python,
marque a opção **Add Python to PATH**.

Depois que Flask e Waitress forem instalados, o sistema poderá ser iniciado
sem internet.

## Iniciar manualmente

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python server.py
```

Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server.py
```

## Como estudar

1. Faça primeiro a aula "Gramática, morfologia e sintaxe".
2. Estude uma classe gramatical de cada vez.
3. Use frases curtas no analisador.
4. Antes de clicar nas palavras, tente classificá-las sozinho.
5. Compare classe e função sintática.
6. Revise as palavras marcadas com `?`.
7. Imprima exercícios quando quiser praticar sem consultar a tela.

## Limite importante

O português permite ambiguidades que dependem de contexto, intenção e
conhecimento de mundo. Este motor usa regras e vocabulário local; portanto,
apresenta hipóteses didáticas, não uma verdade automática. Uma confiança baixa
ou um ponto de interrogação significa que você deve comparar as interpretações.

Exemplo:

- `Eu canto todos os dias.` - **canto** é verbo.
- `O canto ecoou na sala.` - **canto** é substantivo.

Essa limitação é usada como parte do aprendizado: o sistema explica a evidência
que motivou a classificação.

## Dados

O banco é criado automaticamente em `data/gramatica.db`. Para fazer uma cópia
de segurança, use **Histórico → Exportar backup** ou feche o sistema e copie
esse arquivo.

O horário é registrado com deslocamento UTC-03 sem depender do pacote
`tzdata`, evitando erros de `ZoneInfo` em instalações Windows.

## Estrutura

- `app.py`: rotas e páginas Flask;
- `grammar_engine.py`: motor de análise;
- `course_data.py`: aulas e exercícios;
- `database.py`: histórico e progresso SQLite;
- `templates/`: páginas;
- `static/`: visual e interações;
- `server.py`: inicialização local ou em nuvem.

Consulte `REFERENCIAS.md` para entender como o material de apoio compartilhado
durante a criação orientou a abrangência do curso.

## Railway

O projeto inclui `railway.json` e `Procfile`. Em hospedagens efêmeras, o banco
SQLite deve ficar em um volume persistente para não perder o progresso durante
novos deploys. Para uso individual, a versão local é a opção mais simples.
No Railway, defina `DATABASE_PATH` com o caminho do banco dentro do volume.
