"""Base didática autoral de regência verbal e nominal.

O objetivo desta base é ensinar a relação entre termo regente, complemento e
preposição. Ela não reproduz verbetes de dicionários comerciais. Os exemplos
são próprios e priorizam usos frequentes da norma-padrão brasileira.
"""

from __future__ import annotations

import unicodedata


VOLP_URL = "https://www.academia.org.br/nossa-lingua/busca-no-vocabulario"


def _sense(sentido, estrutura, classificacao, preposicao, exemplo, observacao=""):
    return {
        "sentido": sentido,
        "estrutura": estrutura,
        "classificacao": classificacao,
        "preposicao": preposicao,
        "exemplo": exemplo,
        "observacao": observacao,
    }


VERBAL_REGENCY = {
    "agradar": {
        "classe": "verbo",
        "tipo_motor": "VTI ou VTD",
        "preposicoes_motor": ["a"],
        "regencias": [
            _sense("satisfazer, ser agradável", "agradar a alguém", "VTI", "a", "A proposta agradou aos alunos."),
            _sense("acariciar, fazer agrado", "agradar alguém", "VTD", "—", "A mãe agradou a criança."),
        ],
    },
    "aludir": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("fazer referência", "aludir a algo/alguém", "VTI", "a", "O professor aludiu ao capítulo anterior.")],
    },
    "antipatizar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["com"],
        "regencias": [_sense("sentir antipatia", "antipatizar com alguém", "VTI", "com", "Ele antipatizou com o novo colega.", "Na norma-padrão, usa-se sem o pronome se.")],
    },
    "aspirar": {
        "classe": "verbo",
        "tipo_motor": "VTD ou VTI",
        "preposicoes_motor": ["a"],
        "regencias": [
            _sense("sorver, inalar", "aspirar algo", "VTD", "—", "O técnico aspirou a poeira do equipamento."),
            _sense("desejar, almejar", "aspirar a algo", "VTI", "a", "Ela aspira ao cargo de direção."),
        ],
    },
    "assistir": {
        "classe": "verbo",
        "tipo_motor": "VTI ou VTD",
        "preposicoes_motor": ["a"],
        "regencias": [
            _sense("ver, presenciar", "assistir a algo", "VTI", "a", "Assistimos ao documentário."),
            _sense("prestar assistência", "assistir alguém", "VTD", "—", "A médica assistiu o paciente."),
        ],
    },
    "atender": {
        "classe": "verbo",
        "tipo_motor": "VTD ou VTI",
        "preposicoes_motor": ["a"],
        "regencias": [
            _sense("receber, dar atendimento", "atender alguém", "VTD", "—", "A recepcionista atendeu o visitante."),
            _sense("dar atenção ou cumprimento", "atender a algo", "VTI", "a", "O relatório atende às exigências."),
        ],
    },
    "avisar": {
        "classe": "verbo",
        "tipo_motor": "VTDI",
        "preposicoes_motor": ["a", "de", "sobre"],
        "regencias": [
            _sense("informar uma coisa a alguém", "avisar algo a alguém", "VTDI", "a", "Avisei a mudança aos funcionários."),
            _sense("informar alguém acerca de algo", "avisar alguém de/sobre algo", "VTDI", "de / sobre", "Avisei os funcionários sobre a mudança."),
        ],
    },
    "carecer": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["de"],
        "regencias": [_sense("necessitar", "carecer de algo", "VTI", "de", "O texto carece de revisão.")],
    },
    "chegar": {
        "classe": "verbo",
        "tipo_motor": "VI",
        "preposicoes_motor": ["a", "de"],
        "regencias": [
            _sense("alcançar um destino", "chegar a um lugar", "VI + adjunto", "a", "Chegamos à escola cedo.", "Em registro formal, a preposição a é a construção tradicional para destino."),
            _sense("vir de uma origem", "chegar de um lugar", "VI + adjunto", "de", "Eles chegaram de Brasília ontem."),
        ],
    },
    "comunicar": {
        "classe": "verbo",
        "tipo_motor": "VTDI",
        "preposicoes_motor": ["a", "de"],
        "regencias": [
            _sense("transmitir uma informação", "comunicar algo a alguém", "VTDI", "a", "Comunicamos a decisão aos candidatos."),
            _sense("informar alguém", "comunicar alguém de algo", "VTDI", "de", "Comunicamos os candidatos da decisão."),
        ],
    },
    "concordar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["com"],
        "regencias": [_sense("estar de acordo", "concordar com algo/alguém", "VTI", "com", "Concordo com a sua análise.")],
    },
    "confiar": {
        "classe": "verbo",
        "tipo_motor": "VTI ou VTDI",
        "preposicoes_motor": ["em", "a"],
        "regencias": [
            _sense("ter confiança", "confiar em alguém/algo", "VTI", "em", "Confio em sua experiência."),
            _sense("entregar algo aos cuidados de alguém", "confiar algo a alguém", "VTDI", "a", "Confiei o documento ao responsável."),
        ],
    },
    "consistir": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["em"],
        "regencias": [_sense("ser constituído, resumir-se", "consistir em algo", "VTI", "em", "A atividade consiste em analisar frases.")],
    },
    "depender": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["de"],
        "regencias": [_sense("estar condicionado", "depender de algo/alguém", "VTI", "de", "O resultado depende do contexto.")],
    },
    "discordar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["de"],
        "regencias": [_sense("não estar de acordo", "discordar de algo/alguém", "VTI", "de", "Discordo dessa interpretação.")],
    },
    "dispor": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["de"],
        "regencias": [_sense("ter à disposição", "dispor de algo", "VTI", "de", "A biblioteca dispõe de bons materiais.")],
    },
    "esquecer": {
        "classe": "verbo",
        "tipo_motor": "VTD ou VTI",
        "preposicoes_motor": ["de"],
        "regencias": [
            _sense("não se lembrar", "esquecer algo", "VTD", "—", "Esqueci o caderno em casa."),
            _sense("forma pronominal", "esquecer-se de algo", "VTI pronominal", "de", "Esqueci-me do compromisso."),
        ],
    },
    "gostar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["de"],
        "regencias": [_sense("ter apreço ou preferência", "gostar de algo/alguém", "VTI", "de", "Gosto de estudar gramática.")],
    },
    "implicar": {
        "classe": "verbo",
        "tipo_motor": "VTD ou VTI",
        "preposicoes_motor": ["com", "em"],
        "regencias": [
            _sense("acarretar, produzir como consequência", "implicar algo", "VTD", "—", "A decisão implica novos custos."),
            _sense("demonstrar antipatia", "implicar com alguém", "VTI", "com", "Ele implica com o colega."),
            _sense("envolver-se", "implicar-se em algo", "VTI pronominal", "em", "Ele se implicou na discussão."),
        ],
    },
    "informar": {
        "classe": "verbo",
        "tipo_motor": "VTDI",
        "preposicoes_motor": ["a", "de", "sobre"],
        "regencias": [
            _sense("transmitir informação", "informar algo a alguém", "VTDI", "a", "Informei o horário aos alunos."),
            _sense("dar ciência a alguém", "informar alguém de/sobre algo", "VTDI", "de / sobre", "Informei os alunos sobre o horário."),
        ],
    },
    "ir": {
        "classe": "verbo",
        "tipo_motor": "VI",
        "preposicoes_motor": ["a", "para"],
        "regencias": [
            _sense("deslocar-se a destino com ideia de ida", "ir a um lugar", "VI + adjunto", "a", "Fui à biblioteca."),
            _sense("deslocar-se com ideia de destino/permanência", "ir para um lugar", "VI + adjunto", "para", "Ele foi para São Paulo.")
        ],
    },
    "lembrar": {
        "classe": "verbo",
        "tipo_motor": "VTD ou VTI",
        "preposicoes_motor": ["de"],
        "regencias": [
            _sense("recordar", "lembrar algo", "VTD", "—", "Lembro aquela conversa."),
            _sense("forma pronominal", "lembrar-se de algo", "VTI pronominal", "de", "Lembro-me daquela conversa."),
        ],
    },
    "morar": {
        "classe": "verbo",
        "tipo_motor": "VI",
        "preposicoes_motor": ["em"],
        "regencias": [_sense("residir", "morar em um lugar", "VI + adjunto", "em", "Moro em Pouso Alegre.")],
    },
    "namorar": {
        "classe": "verbo",
        "tipo_motor": "VTD",
        "preposicoes_motor": [],
        "regencias": [_sense("manter namoro", "namorar alguém", "VTD", "—", "Ela namora um colega.", "Na norma-padrão tradicional, o complemento não é introduzido por com.")],
    },
    "necessitar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["de"],
        "regencias": [_sense("ter necessidade", "necessitar de algo", "VTI", "de", "O projeto necessita de ajustes.")],
    },
    "obedecer": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("cumprir, submeter-se", "obedecer a algo/alguém", "VTI", "a", "Obedecemos às regras.")],
    },
    "optar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["por"],
        "regencias": [_sense("escolher entre alternativas", "optar por algo", "VTI", "por", "Optei pelo estudo diário.")],
    },
    "pagar": {
        "classe": "verbo",
        "tipo_motor": "VTDI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("dar pagamento", "pagar algo a alguém", "VTDI", "a", "Paguei a conta ao atendente.", "A coisa paga funciona como objeto direto; a pessoa, como objeto indireto." )],
    },
    "perdoar": {
        "classe": "verbo",
        "tipo_motor": "VTDI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("conceder perdão", "perdoar algo a alguém", "VTDI", "a", "Perdoei o erro ao colega.", "A coisa perdoada é objeto direto; a pessoa, objeto indireto." )],
    },
    "pertencer": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("ser propriedade ou parte de", "pertencer a algo/alguém", "VTI", "a", "O livro pertence à biblioteca.")],
    },
    "preferir": {
        "classe": "verbo",
        "tipo_motor": "VTDI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("escolher uma coisa em relação a outra", "preferir X a Y", "VTDI", "a", "Prefiro leitura a televisão.", "Na construção formal tradicional, evita-se reforçar com mais e usar do que no segundo termo." )],
    },
    "precisar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["de"],
        "regencias": [_sense("ter necessidade", "precisar de algo", "VTI", "de", "Preciso de ajuda.", "Esta é a construção tradicional mais útil para o estudo da norma-padrão." )],
    },
    "proceder": {
        "classe": "verbo",
        "tipo_motor": "VI ou VTI",
        "preposicoes_motor": ["a", "de"],
        "regencias": [
            _sense("ter origem", "proceder de algum lugar", "VTI", "de", "A informação procede de fonte confiável."),
            _sense("realizar, dar início", "proceder a algo", "VTI", "a", "A equipe procedeu à conferência."),
            _sense("ter fundamento", "proceder", "VI", "—", "A reclamação não procede."),
        ],
    },
    "recorrer": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("buscar auxílio ou recurso", "recorrer a algo/alguém", "VTI", "a", "Recorremos ao manual para conferir a regra.")],
    },
    "referir-se": {
        "classe": "verbo pronominal",
        "tipo_motor": "VTI pronominal",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("fazer referência", "referir-se a algo/alguém", "VTI pronominal", "a", "O texto se refere à norma-padrão.")],
        "lema_motor": "referir",
    },
    "renunciar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["a"],
        "regencias": [_sense("abrir mão", "renunciar a algo", "VTI", "a", "Ele renunciou ao cargo.")],
    },
    "responder": {
        "classe": "verbo",
        "tipo_motor": "VTD ou VTI ou VTDI",
        "preposicoes_motor": ["a"],
        "regencias": [
            _sense("dar uma resposta", "responder algo", "VTD", "—", "Ela respondeu a pergunta com clareza."),
            _sense("dar resposta a alguém ou a algo", "responder a alguém/algo", "VTI", "a", "Ela respondeu ao professor."),
            _sense("dizer algo a alguém em resposta", "responder algo a alguém", "VTDI", "a", "Ela respondeu a verdade ao professor."),
        ],
    },
    "simpatizar": {
        "classe": "verbo",
        "tipo_motor": "VTI",
        "preposicoes_motor": ["com"],
        "regencias": [_sense("sentir simpatia", "simpatizar com alguém/algo", "VTI", "com", "Simpatizei com a proposta.", "Na norma-padrão, usa-se sem o pronome se." )],
    },
    "visar": {
        "classe": "verbo",
        "tipo_motor": "VTD ou VTI",
        "preposicoes_motor": ["a"],
        "regencias": [
            _sense("mirar ou pôr visto", "visar algo", "VTD", "—", "O arqueiro visou o alvo."),
            _sense("ter como objetivo", "visar a algo", "VTI", "a", "O curso visa ao domínio consciente da língua.", "A construção com a é a forma tradicional da norma-padrão para este sentido."),
        ],
    },
}


NOMINAL_REGENCY = {
    "acessível": {"classe": "adjetivo", "regencias": [_sense("que permite acesso", "acessível a alguém", "regência nominal", "a", "O conteúdo é acessível aos iniciantes.")]},
    "alheio": {"classe": "adjetivo", "regencias": [_sense("estranho, não relacionado", "alheio a algo", "regência nominal", "a", "Ele permaneceu alheio à discussão.")]},
    "amor": {"classe": "substantivo", "regencias": [_sense("afeição", "amor a/por alguém ou algo", "regência nominal", "a / por", "O amor à leitura cresce com a prática.")]},
    "apto": {"classe": "adjetivo", "regencias": [_sense("capaz, habilitado", "apto a/para algo", "regência nominal", "a / para", "Ela está apta ao trabalho.")]},
    "aversão": {"classe": "substantivo", "regencias": [_sense("repulsa", "aversão a/por algo", "regência nominal", "a / por", "Ele tem aversão ao desperdício.")]},
    "capaz": {"classe": "adjetivo", "regencias": [_sense("que tem capacidade", "capaz de algo", "regência nominal", "de", "Ela é capaz de resolver o problema.")]},
    "capacidade": {"classe": "substantivo", "regencias": [_sense("aptidão", "capacidade de/para algo", "regência nominal", "de / para", "Ele demonstrou capacidade de análise.")]},
    "certeza": {"classe": "substantivo", "regencias": [_sense("convicção", "certeza de algo", "regência nominal", "de", "Tenho certeza da resposta.")]},
    "compatível": {"classe": "adjetivo", "regencias": [_sense("que pode coexistir", "compatível com algo", "regência nominal", "com", "A solução é compatível com o sistema.")]},
    "contrário": {"classe": "adjetivo", "regencias": [_sense("oposto", "contrário a algo", "regência nominal", "a", "Sou contrário à mudança proposta.")]},
    "favorável": {"classe": "adjetivo", "regencias": [_sense("que favorece", "favorável a algo", "regência nominal", "a", "O parecer foi favorável ao projeto.")]},
    "fidelidade": {"classe": "substantivo", "regencias": [_sense("lealdade", "fidelidade a algo/alguém", "regência nominal", "a", "A pesquisa exige fidelidade aos dados.")]},
    "grato": {"classe": "adjetivo", "regencias": [_sense("agradecido", "grato a alguém por algo", "regência nominal", "a / por", "Sou grato ao professor pela ajuda.")]},
    "hábito": {"classe": "substantivo", "regencias": [_sense("costume", "hábito de algo", "regência nominal", "de", "Criei o hábito de estudar diariamente.")]},
    "indiferente": {"classe": "adjetivo", "regencias": [_sense("sem interesse", "indiferente a algo", "regência nominal", "a", "Ele ficou indiferente ao comentário.")]},
    "inerente": {"classe": "adjetivo", "regencias": [_sense("inseparável, próprio", "inerente a algo", "regência nominal", "a", "A variação é inerente à língua.")]},
    "medo": {"classe": "substantivo", "regencias": [_sense("temor", "medo de algo", "regência nominal", "de", "Ele perdeu o medo de errar.")]},
    "necessidade": {"classe": "substantivo", "regencias": [_sense("aquilo que é necessário", "necessidade de algo", "regência nominal", "de", "Há necessidade de revisão.")]},
    "obediência": {"classe": "substantivo", "regencias": [_sense("ato de obedecer", "obediência a algo/alguém", "regência nominal", "a", "A norma exige obediência às regras do edital.")]},
    "orgulho": {"classe": "substantivo", "regencias": [_sense("sentimento de satisfação", "orgulho de algo/alguém", "regência nominal", "de", "Ela sente orgulho do próprio progresso.")]},
    "paralelo": {"classe": "adjetivo", "regencias": [_sense("correspondente ou semelhante", "paralelo a algo", "regência nominal", "a", "O estudo corre paralelo à prática.")]},
    "referência": {"classe": "substantivo", "regencias": [_sense("menção", "referência a algo/alguém", "regência nominal", "a", "O texto faz referência ao capítulo anterior.")]},
    "relativo": {"classe": "adjetivo", "regencias": [_sense("referente", "relativo a algo", "regência nominal", "a", "O aviso é relativo à prova.")]},
    "respeito": {"classe": "substantivo", "regencias": [_sense("consideração", "respeito a/por algo ou alguém", "regência nominal", "a / por", "O respeito às regras facilita a convivência.")]},
    "útil": {"classe": "adjetivo", "regencias": [_sense("que tem utilidade", "útil a/para alguém ou algo", "regência nominal", "a / para", "O guia é útil aos estudantes.")]},
}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", str(text).casefold())
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def all_regency_entries() -> list[dict]:
    entries = []
    for term, data in VERBAL_REGENCY.items():
        entries.append({"termo": term, "categoria": "verbal", **data})
    for term, data in NOMINAL_REGENCY.items():
        entries.append({"termo": term, "categoria": "nominal", **data})
    return sorted(entries, key=lambda item: _normalize(item["termo"]))


def search_regency(query: str = "", category: str = "todos") -> list[dict]:
    query = _normalize(query.strip())
    words = [part for part in query.split() if part]
    results = []
    for entry in all_regency_entries():
        if category in {"verbal", "nominal"} and entry["categoria"] != category:
            continue
        searchable = _normalize(
            " ".join(
                [entry["termo"], entry["classe"]]
                + [
                    " ".join(
                        [
                            sense["sentido"],
                            sense["estrutura"],
                            sense["classificacao"],
                            sense["preposicao"],
                            f"preposição {sense['preposicao']}",
                            sense["exemplo"],
                        ]
                    )
                    for sense in entry["regencias"]
                ]
            )
        )
        if not words or all(word in searchable for word in words):
            results.append(entry)
    return results


def get_regency_entry(term: str) -> dict | None:
    target = _normalize(term).removesuffix("-se")
    for entry in all_regency_entries():
        candidate = _normalize(entry.get("lema_motor", entry["termo"])).removesuffix("-se")
        if candidate == target:
            return entry
    return None


def engine_frames() -> dict[str, dict]:
    frames = {}
    for term, data in VERBAL_REGENCY.items():
        lemma = data.get("lema_motor", term).removesuffix("-se")
        frames[lemma] = {
            "tipo": data["tipo_motor"],
            "preps": set(data["preposicoes_motor"]),
        }
    return frames
