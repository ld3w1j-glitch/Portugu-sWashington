"""Motor didático de análise morfológica e sintática.

O objetivo não é substituir um gramático ou um analisador estatístico. O motor
combina vocabulário, padrões de flexão e contexto para produzir uma hipótese
explicada. Casos ambíguos são sinalizados para que façam parte do aprendizado.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass, field
from typing import Iterable


TOKEN_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*|\d+(?:[.,]\d+)?|[^\w\s]",
    re.UNICODE,
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def normalized_set(words: str) -> set[str]:
    return {normalize(word) for word in words.split()}


ARTICLES = {
    "o": ("definido", "masculino", "singular"),
    "a": ("definido", "feminino", "singular"),
    "os": ("definido", "masculino", "plural"),
    "as": ("definido", "feminino", "plural"),
    "um": ("indefinido", "masculino", "singular"),
    "uma": ("indefinido", "feminino", "singular"),
    "uns": ("indefinido", "masculino", "plural"),
    "umas": ("indefinido", "feminino", "plural"),
}

PREPOSITIONS = normalized_set(
    "a ante após até com contra de desde em entre para perante por sem sob sobre trás"
)
PREPOSITION_CONTRACTIONS = {
    "ao": "a + o",
    "aos": "a + os",
    "do": "de + o",
    "da": "de + a",
    "dos": "de + os",
    "das": "de + as",
    "no": "em + o",
    "na": "em + a",
    "nos": "em + os",
    "nas": "em + as",
    "pelo": "por + o",
    "pela": "por + a",
    "pelos": "por + os",
    "pelas": "por + as",
    "num": "em + um",
    "numa": "em + uma",
    "nuns": "em + uns",
    "numas": "em + umas",
    "à": "a + a",
    "às": "a + as",
    "deste": "de + este",
    "desta": "de + esta",
    "daquele": "de + aquele",
    "naquele": "em + aquele",
}
PREPOSITION_CONTRACTIONS = {
    normalize(key): value for key, value in PREPOSITION_CONTRACTIONS.items()
}

CONJUNCTIONS = {
    "e": "coordenativa aditiva",
    "nem": "coordenativa aditiva",
    "mas": "coordenativa adversativa",
    "porem": "coordenativa adversativa",
    "contudo": "coordenativa adversativa",
    "todavia": "coordenativa adversativa",
    "entretanto": "coordenativa adversativa",
    "ou": "coordenativa alternativa",
    "logo": "coordenativa conclusiva",
    "portanto": "coordenativa conclusiva",
    "pois": "conclusiva ou explicativa, conforme a posição",
    "porque": "causal ou explicativa, conforme o contexto",
    "porquanto": "causal ou explicativa",
    "que": "integrante, explicativa ou consecutiva, conforme o contexto",
    "se": "integrante ou condicional, conforme o contexto",
    "quando": "subordinativa temporal",
    "enquanto": "subordinativa temporal",
    "embora": "subordinativa concessiva",
    "conquanto": "subordinativa concessiva",
    "caso": "subordinativa condicional",
    "conforme": "subordinativa conformativa",
    "consoante": "subordinativa conformativa",
    "como": "comparativa, conformativa ou causal, conforme o contexto",
}

PRONOUNS = {
    # pessoais
    "eu": "pessoal do caso reto",
    "tu": "pessoal do caso reto",
    "ele": "pessoal do caso reto",
    "ela": "pessoal do caso reto",
    "nos": "pessoal do caso reto ou oblíquo",
    "vos": "pessoal do caso reto ou oblíquo",
    "eles": "pessoal do caso reto",
    "elas": "pessoal do caso reto",
    "me": "pessoal oblíquo átono",
    "te": "pessoal oblíquo átono",
    "se": "pessoal oblíquo ou partícula",
    "o": "pessoal oblíquo átono",
    "a": "pessoal oblíquo átono",
    "lhe": "pessoal oblíquo átono",
    "nos": "pessoal oblíquo átono",
    "vos": "pessoal oblíquo átono",
    "os": "pessoal oblíquo átono",
    "as": "pessoal oblíquo átono",
    "lhes": "pessoal oblíquo átono",
    "mim": "pessoal oblíquo tônico",
    "ti": "pessoal oblíquo tônico",
    "si": "pessoal oblíquo tônico",
    "comigo": "pessoal oblíquo tônico",
    "contigo": "pessoal oblíquo tônico",
    "consigo": "pessoal oblíquo tônico",
    # possessivos
    "meu": "possessivo",
    "minha": "possessivo",
    "meus": "possessivo",
    "minhas": "possessivo",
    "teu": "possessivo",
    "tua": "possessivo",
    "teus": "possessivo",
    "tuas": "possessivo",
    "seu": "possessivo",
    "sua": "possessivo",
    "seus": "possessivo",
    "suas": "possessivo",
    "nosso": "possessivo",
    "nossa": "possessivo",
    "nossos": "possessivo",
    "nossas": "possessivo",
    # demonstrativos
    "este": "demonstrativo",
    "esta": "demonstrativo",
    "estes": "demonstrativo",
    "estas": "demonstrativo",
    "isto": "demonstrativo",
    "esse": "demonstrativo",
    "essa": "demonstrativo",
    "esses": "demonstrativo",
    "essas": "demonstrativo",
    "isso": "demonstrativo",
    "aquele": "demonstrativo",
    "aquela": "demonstrativo",
    "aqueles": "demonstrativo",
    "aquelas": "demonstrativo",
    "aquilo": "demonstrativo",
    # indefinidos/interrogativos/relativos
    "alguem": "indefinido",
    "ninguem": "indefinido",
    "algo": "indefinido",
    "nada": "indefinido",
    "tudo": "indefinido",
    "cada": "indefinido",
    "outro": "indefinido",
    "outra": "indefinido",
    "qualquer": "indefinido",
    "quem": "interrogativo ou relativo",
    "qual": "interrogativo ou relativo",
    "quais": "interrogativo ou relativo",
    "quanto": "interrogativo, relativo ou indefinido",
    "cujo": "relativo possessivo",
    "cuja": "relativo possessivo",
    "cujos": "relativo possessivo",
    "cujas": "relativo possessivo",
    "onde": "relativo, quando retoma lugar",
}

NUMERALS = {
    **{str(n): "cardinal" for n in range(0, 101)},
    **{
        normalize(word): "cardinal"
        for word in (
            "zero um uma dois duas três quatro cinco seis sete oito nove dez onze "
            "doze treze catorze quatorze quinze dezesseis dezassete dezessete "
            "dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta "
            "oitenta noventa cem cento mil milhão milhões bilhão bilhões"
        ).split()
    },
    **{
        normalize(word): "ordinal"
        for word in (
            "primeiro primeira segundo segunda terceiro terceira quarto quarta "
            "quinto quinta sexto sexta sétimo sétima oitavo oitava nono nona "
            "décimo décima centésimo centésima milésimo milésima"
        ).split()
    },
    "meio": "fracionário ou multiplicativo, conforme o contexto",
    "metade": "fracionário",
    "dobro": "multiplicativo",
    "triplo": "multiplicativo",
}

ADVERBS = {
    **{
        normalize(word): "tempo"
        for word in "hoje ontem amanhã agora ainda cedo tarde nunca jamais sempre outrora logo".split()
    },
    **{
        normalize(word): "lugar"
        for word in "aqui ali lá acolá acima abaixo dentro fora perto longe onde adiante atrás".split()
    },
    **{
        normalize(word): "modo"
        for word in "bem mal assim depressa devagar melhor pior".split()
    },
    **{
        normalize(word): "intensidade"
        for word in "muito pouco bastante demais mais menos tão quão quase tanto".split()
    },
    **{
        normalize(word): "afirmação"
        for word in "sim certamente realmente efetivamente decerto".split()
    },
    **{
        normalize(word): "negação"
        for word in "não nunca jamais tampouco".split()
    },
    **{
        normalize(word): "dúvida"
        for word in "talvez acaso provavelmente possivelmente quiçá".split()
    },
}

INTERJECTIONS = {
    normalize(word): meaning
    for word, meaning in {
        "ah": "espanto, alegria, dor ou lembrança",
        "oh": "admiração, alegria ou tristeza",
        "ó": "chamamento",
        "ai": "dor ou lamento",
        "ufa": "alívio",
        "oba": "alegria",
        "viva": "comemoração",
        "socorro": "pedido de ajuda",
        "bravo": "aprovação",
        "ei": "chamamento",
        "olá": "saudação",
        "tchau": "despedida",
        "arre": "irritação",
        "puxa": "surpresa",
    }.items()
}

COMMON_ADJECTIVES = normalized_set(
    "alto baixo bonito feio feliz triste alegre rápido lenta lento grande pequeno "
    "nova novo velho velha inteligente forte fraco claro escuro difícil fácil "
    "brasileiro brasileira bom boa mau má importante possível impossível "
    "vermelho azul verde amarelo cansado cansada ansioso ansiosa aberto aberta "
    "fechado fechada correto correta simples composto comum próprio concreto abstrato "
    "belo bela atento atenta vazio vazia silencioso silenciosa longo longa"
)

COMMON_NOUNS = normalized_set(
    "menino menina homem mulher criança aluno aluna professor professora livro casa "
    "carro escola cidade trabalho tempo dia noite manhã tarde frase palavra língua "
    "gramática análise sintaxe morfologia sujeito predicado objeto cachorro gato "
    "mesa cadeira comida água café mercado amigo amiga família prova questão resposta "
    "pessoa pessoas mundo vida ideia pensamento coração"
)

PROPER_NOUNS = normalized_set(
    "Brasil Portugal Maria João Washington Ana Pedro Carlos Juliana Minas Gerais"
)

AMBIGUITIES = {
    "a": ["artigo definido", "preposição", "pronome oblíquo"],
    "o": ["artigo definido", "pronome oblíquo", "pronome demonstrativo"],
    "um": ["artigo indefinido", "numeral cardinal"],
    "uma": ["artigo indefinido", "numeral cardinal"],
    "como": ["conjunção", "advérbio interrogativo", "verbo comer"],
    "que": ["conjunção", "pronome relativo", "pronome interrogativo"],
    "se": ["conjunção", "pronome", "partícula apassivadora", "índice de indeterminação"],
    "meio": ["numeral", "advérbio", "substantivo"],
    "muito": ["advérbio", "pronome indefinido"],
    "pouco": ["advérbio", "pronome indefinido"],
    "canto": ["substantivo", "verbo cantar"],
    "jovem": ["substantivo", "adjetivo"],
}

REGULAR_VERBS = (
    "amar cantar comprar estudar falar trabalhar brincar olhar morar chegar analisar "
    "explicar caminhar ensinar perguntar usar ajudar chamar encontrar precisar gostar "
    "comer beber correr aprender vender viver escrever receber partir abrir assistir "
    "decidir permitir subir resolver responder retornar terminar continuar transformar "
    "emocionar ecoar confiar entregar aceitar organizar comparar classificar identificar "
    "completar modificar concordar relacionar"
).split()

IRREGULAR_FORMS = {
    "sou": "ser",
    "es": "ser",
    "e": "ser",
    "somos": "ser",
    "sao": "ser",
    "era": "ser",
    "eram": "ser",
    "fui": "ser/ir",
    "foi": "ser/ir",
    "foram": "ser/ir",
    "serei": "ser",
    "estou": "estar",
    "esta": "estar",
    "estamos": "estar",
    "estao": "estar",
    "estava": "estar",
    "estavam": "estar",
    "esteve": "estar",
    "tenho": "ter",
    "tem": "ter",
    "temos": "ter",
    "tinha": "ter",
    "teve": "ter",
    "ha": "haver",
    "havia": "haver",
    "houve": "haver",
    "havera": "haver",
    "faco": "fazer",
    "faz": "fazer",
    "fazem": "fazer",
    "fez": "fazer",
    "vou": "ir",
    "vai": "ir",
    "vamos": "ir",
    "vao": "ir",
    "ia": "ir",
    "posso": "poder",
    "pode": "poder",
    "podem": "poder",
    "podia": "poder",
    "quero": "querer",
    "quer": "querer",
    "querem": "querer",
    "disse": "dizer",
    "diz": "dizer",
    "dizem": "dizer",
    "vejo": "ver",
    "ve": "ver",
    "vi": "ver",
    "veio": "vir",
    "vem": "vir",
    "vieram": "vir",
    "leio": "ler",
    "le": "ler",
    "li": "ler",
    "deu": "dar",
    "dou": "dar",
    "da": "dar",
    "pareco": "parecer",
    "parece": "parecer",
    "parecem": "parecer",
    "parecia": "parecer",
    "pareciam": "parecer",
    "permanece": "permanecer",
    "permanecem": "permanecer",
    "permaneceu": "permanecer",
    "ficou": "ficar",
    "ficaram": "ficar",
    "acontece": "acontecer",
    "aconteceu": "acontecer",
    "aconteceram": "acontecer",
    "ocorre": "ocorrer",
    "ocorreu": "ocorrer",
    "ocorreram": "ocorrer",
    "existe": "existir",
    "existem": "existir",
    "existiu": "existir",
    "chove": "chover",
    "choveu": "chover",
    "nasceu": "nascer",
    "nasceram": "nascer",
    "morreu": "morrer",
    "morreram": "morrer",
}

LINKING_VERBS = normalized_set(
    "ser estar ficar permanecer continuar parecer andar tornar virar"
)
INTRANSITIVE_VERBS = normalized_set(
    "chegar sair voltar nascer morrer acontecer ocorrer existir caminhar correr"
)
LOCATIVE_VERBS = normalized_set("morar viver ficar permanecer chegar ir voltar")
ACTION_WITH_SUBJECT_PREDICATIVE = normalized_set(
    "chegar sair voltar caminhar correr"
)

# O acento diferencia formas verbais de homônimos muito frequentes:
# "é/e", "está/esta" e "dá/da".
ACCENTED_VERB_FORMS = {
    "é": "ser",
    "és": "ser",
    "está": "estar",
    "estão": "estar",
    "dá": "dar",
    "vê": "ver",
    "têm": "ter",
    "vêm": "vir",
}


def build_regular_forms(lemma: str) -> set[str]:
    stem, ending = lemma[:-2], lemma[-2:]
    forms = {lemma}
    if ending == "ar":
        tails = (
            "o as a am amos ava avas avam avamos ei aste ou aram aria arias "
            "ariam ariamos ando ado"
        ).split()
    elif ending == "er":
        tails = (
            "o es e em emos ia ias iam iamos i este eu eram eria erias eriam "
            "eriamos endo ido"
        ).split()
    else:
        tails = (
            "o es e em imos ia ias iam iamos i iste iu iram iria irias iriam "
            "iriamos indo ido"
        ).split()
    forms.update(stem + tail for tail in tails)
    return {normalize(form) for form in forms}


VERB_FORMS: dict[str, str] = {}
for _lemma in REGULAR_VERBS:
    for _form in build_regular_forms(_lemma):
        VERB_FORMS[_form] = _lemma
VERB_FORMS.update(IRREGULAR_FORMS)


CLASS_DESCRIPTIONS = {
    "artigo": "acompanha o substantivo, determinando-o ou generalizando-o",
    "substantivo": "nomeia seres, lugares, sentimentos, ações, qualidades ou conceitos",
    "adjetivo": "caracteriza ou delimita um substantivo",
    "pronome": "retoma, substitui ou acompanha um nome",
    "numeral": "indica quantidade, ordem, multiplicação ou fração",
    "verbo": "exprime ação, estado, mudança de estado ou fenômeno",
    "advérbio": "modifica verbo, adjetivo, outro advérbio ou toda a oração",
    "preposição": "liga termos e estabelece uma relação de sentido entre eles",
    "conjunção": "liga termos semelhantes ou orações",
    "interjeição": "expressa emoção, reação, chamamento ou estado de espírito",
    "pontuação": "organiza a escrita e ajuda a construir o sentido",
}


@dataclass
class WordAnalysis:
    index: int
    token: str
    normalized: str
    classe: str
    subclasse: str = ""
    morfologia: list[str] = field(default_factory=list)
    funcao: str = "função dependente do contexto"
    explicacao: str = ""
    confianca: int = 70
    alternativas: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _gender_number(word: str) -> list[str]:
    result = ["plural" if word.endswith("s") and len(word) > 2 else "singular"]
    singular = word[:-1] if result[0] == "plural" else word
    if singular.endswith("a"):
        result.insert(0, "provável feminino")
    elif singular.endswith("o"):
        result.insert(0, "provável masculino")
    return result


def _classify_word(
    token: str,
    index: int,
    raw_tokens: list[str],
    provisional: list[WordAnalysis],
) -> WordAnalysis:
    word = normalize(token)
    previous = normalize(raw_tokens[index - 1]) if index > 0 else ""
    following = normalize(raw_tokens[index + 1]) if index + 1 < len(raw_tokens) else ""

    if re.fullmatch(r"[^\w\s]", token, re.UNICODE):
        return WordAnalysis(
            index,
            token,
            word,
            "pontuação",
            explicacao="Este sinal delimita ou organiza partes do enunciado.",
            confianca=100,
        )

    if re.fullmatch(r"\d+(?:[.,]\d+)?", token):
        return WordAnalysis(
            index,
            token,
            word,
            "numeral",
            "cardinal em algarismos",
            ["invariável na forma apresentada"],
            explicacao="Representa uma quantidade por meio de algarismos.",
            confianca=99,
        )

    raw_lower = token.lower()
    if raw_lower in ACCENTED_VERB_FORMS:
        lemma = ACCENTED_VERB_FORMS[raw_lower]
        return WordAnalysis(
            index,
            token,
            word,
            "verbo",
            f"verbo {lemma}",
            [f"forma do verbo {lemma}", "forma finita"],
            explicacao=f"O acento ajuda a distinguir esta forma do verbo “{lemma}” de palavras homônimas.",
            confianca=98,
        )

    # Artigos precisam ser avaliados antes dos pronomes homônimos.
    if word in ARTICLES:
        subtype, gender, number = ARTICLES[word]
        confidence = 94 if following and following not in VERB_FORMS else 68
        alternatives = AMBIGUITIES.get(word, [])[1:] if word in AMBIGUITIES else []
        return WordAnalysis(
            index,
            token,
            word,
            "artigo",
            subtype,
            [gender, number, "classe variável"],
            explicacao=f"Apresenta ou determina o nome que vem depois. É um artigo {subtype}.",
            confianca=confidence,
            alternativas=alternatives,
        )

    if word in PREPOSITION_CONTRACTIONS:
        return WordAnalysis(
            index,
            token,
            word,
            "preposição",
            "contração",
            ["classe invariável", f"formação: {PREPOSITION_CONTRACTIONS[word]}"],
            explicacao="Resulta da união de uma preposição com artigo ou pronome.",
            confianca=96,
        )

    if word in PREPOSITIONS:
        return WordAnalysis(
            index,
            token,
            word,
            "preposição",
            "essencial",
            ["classe invariável"],
            explicacao="Liga dois termos e introduz uma relação entre eles.",
            confianca=96,
            alternativas=AMBIGUITIES.get(word, [])[1:],
        )

    if word in INTERJECTIONS:
        return WordAnalysis(
            index,
            token,
            word,
            "interjeição",
            INTERJECTIONS[word],
            ["classe invariável"],
            explicacao=f"Expressa {INTERJECTIONS[word]}.",
            confianca=92,
        )

    # "que", "se" e "como" recebem confiança menor por sua grande ambiguidade.
    if word in CONJUNCTIONS:
        confidence = 62 if word in {"que", "se", "como", "pois"} else 91
        return WordAnalysis(
            index,
            token,
            word,
            "conjunção",
            CONJUNCTIONS[word],
            ["classe invariável"],
            explicacao="Conecta termos ou introduz uma nova oração.",
            confianca=confidence,
            alternativas=AMBIGUITIES.get(word, [])[1:],
        )

    if word in PRONOUNS:
        return WordAnalysis(
            index,
            token,
            word,
            "pronome",
            PRONOUNS[word],
            ["classe variável em muitos de seus tipos"],
            explicacao=f"Funciona como pronome {PRONOUNS[word]}.",
            confianca=88 if word not in AMBIGUITIES else 66,
            alternativas=AMBIGUITIES.get(word, [])[1:],
        )

    if word in NUMERALS:
        # Após artigo, "meio" e semelhantes podem estar substantivados.
        confidence = 88 if previous not in ARTICLES else 70
        return WordAnalysis(
            index,
            token,
            word,
            "numeral",
            NUMERALS[word],
            ["classe variável em gênero e/ou número em certos casos"],
            explicacao=f"Indica valor numérico do tipo {NUMERALS[word]}.",
            confianca=confidence,
            alternativas=AMBIGUITIES.get(word, [])[1:],
        )

    if word in ADVERBS or word.endswith("mente"):
        subtype = ADVERBS.get(word, "modo (formado com o sufixo -mente)")
        return WordAnalysis(
            index,
            token,
            word,
            "advérbio",
            subtype,
            ["classe invariável"],
            explicacao=f"Acrescenta uma circunstância de {subtype}.",
            confianca=94 if word in ADVERBS else 90,
            alternativas=AMBIGUITIES.get(word, [])[1:],
        )

    if word in {"canto"} and previous in ARTICLES:
        return WordAnalysis(
            index,
            token,
            word,
            "substantivo",
            "comum (leitura contextual)",
            _gender_number(word) + ["classe variável"],
            explicacao="O artigo anterior indica que “canto” está nomeando algo, e não exprimindo a ação de cantar.",
            confianca=90,
            alternativas=["verbo cantar em outro contexto"],
        )

    if word in VERB_FORMS:
        lemma = VERB_FORMS[word]
        morphology = [f"forma do verbo {lemma}"]
        if word.endswith(("ando", "endo", "indo")):
            morphology.append("gerúndio")
        elif word.endswith(("ado", "ido")):
            morphology.append("particípio")
        elif word.endswith(("ar", "er", "ir")):
            morphology.append("infinitivo")
        else:
            morphology.append("forma finita")
        return WordAnalysis(
            index,
            token,
            word,
            "verbo",
            f"verbo {lemma}",
            morphology,
            explicacao=f"É uma forma verbal associada ao infinitivo “{lemma}”.",
            confianca=93,
            alternativas=AMBIGUITIES.get(word, [])[1:],
        )

    if word.endswith(("ar", "er", "ir")) and len(word) > 3:
        return WordAnalysis(
            index,
            token,
            word,
            "verbo",
            "infinitivo",
            ["forma nominal", "infinitivo"],
            explicacao="A terminação sugere uma forma verbal no infinitivo.",
            confianca=82,
            alternativas=["substantivo, em contextos de substantivação"],
        )

    adjective_suffixes = (
        "oso",
        "osa",
        "avel",
        "ivel",
        "al",
        "ico",
        "ica",
        "ario",
        "aria",
        "ento",
        "enta",
        "ivo",
        "iva",
        "ês",
        "esa",
    )
    if word in COMMON_ADJECTIVES or (
        word.endswith(adjective_suffixes) and word not in COMMON_NOUNS
    ):
        return WordAnalysis(
            index,
            token,
            word,
            "adjetivo",
            "qualificativo ou relacional",
            _gender_number(word) + ["classe variável"],
            explicacao="Atribui característica, estado ou relação a um nome.",
            confianca=88 if word in COMMON_ADJECTIVES else 72,
            alternativas=AMBIGUITIES.get(word, []),
        )

    if word in COMMON_NOUNS:
        return WordAnalysis(
            index,
            token,
            word,
            "substantivo",
            "comum",
            _gender_number(word) + ["classe variável"],
            explicacao="Nomeia um ser, lugar, sentimento, ação ou conceito.",
            confianca=91,
            alternativas=AMBIGUITIES.get(word, [])[1:],
        )

    if word in PROPER_NOUNS:
        return WordAnalysis(
            index,
            token,
            word,
            "substantivo",
            "próprio",
            ["classe variável"],
            explicacao="Nomeia um ser ou lugar individualizado.",
            confianca=94,
        )

    if word == "jovem" and provisional and provisional[-1].classe == "substantivo":
        return WordAnalysis(
            index,
            token,
            word,
            "adjetivo",
            "qualificativo (leitura contextual)",
            ["singular", "uniforme em gênero"],
            explicacao="Depois do nome, “jovem” atribui a ele uma característica.",
            confianca=82,
            alternativas=["substantivo em outro contexto"],
        )

    if token[:1].isupper() and index > 0:
        return WordAnalysis(
            index,
            token,
            word,
            "substantivo",
            "próprio (hipótese)",
            ["provavelmente próprio", "classe variável"],
            explicacao="A inicial maiúscula dentro da frase sugere um nome próprio.",
            confianca=79,
            alternativas=["substantivo comum em uso especial"],
        )

    if previous in ARTICLES or previous in PRONOUNS or previous in NUMERALS:
        return WordAnalysis(
            index,
            token,
            word,
            "substantivo",
            "comum (hipótese contextual)",
            _gender_number(word) + ["classe variável"],
            explicacao="O determinante anterior sugere que esta palavra funciona como nome.",
            confianca=72,
            alternativas=["adjetivo substantivado", "outra classe substantivada"],
        )

    # Padrão seguro para palavras lexicais desconhecidas: hipótese de nome,
    # acompanhada de alerta. É melhor ensinar a dúvida do que ocultá-la.
    return WordAnalysis(
        index,
        token,
        word,
        "substantivo",
        "hipótese inicial",
        _gender_number(word),
        explicacao="Sem um dicionário completo, o motor considera inicialmente esta palavra um nome.",
        confianca=52,
        alternativas=AMBIGUITIES.get(word, ["adjetivo", "verbo, conforme o contexto"]),
    )


def _join_tokens(tokens: Iterable[str]) -> str:
    text = " ".join(tokens)
    text = re.sub(r"\s+([,.;:!?…])", r"\1", text)
    text = re.sub(r"([¿¡(])\s+", r"\1", text)
    return text.strip()


def _content_indices(words: list[WordAnalysis], start: int, end: int) -> list[int]:
    return [
        index
        for index in range(start, end)
        if words[index].classe not in {"pontuação", "conjunção"}
    ]


def _mark_nominal_group(words: list[WordAnalysis], indices: list[int], head_function: str) -> None:
    noun_candidates = [
        index
        for index in indices
        if words[index].classe in {"substantivo", "pronome", "numeral"}
    ]
    if not noun_candidates:
        noun_candidates = [index for index in indices if words[index].classe == "adjetivo"]
    if not noun_candidates:
        return
    head = noun_candidates[-1]
    words[head].funcao = head_function
    for index in indices:
        if index == head:
            continue
        if words[index].classe in {"artigo", "adjetivo", "pronome", "numeral"}:
            words[index].funcao = "adjunto adnominal"
        elif words[index].classe == "preposição":
            words[index].funcao = "elemento de ligação do grupo nominal"


def _syntactic_analysis(words: list[WordAnalysis]) -> dict:
    phrases: list[dict] = []
    warnings: list[str] = []
    lexical_indices = [i for i, word in enumerate(words) if word.classe != "pontuação"]
    verb_indices = [i for i in lexical_indices if words[i].classe == "verbo"]

    for word in words:
        if word.classe == "pontuação":
            word.funcao = "sinal de pontuação"
        elif word.classe == "conjunção":
            word.funcao = "conector"
        elif word.classe == "interjeição":
            word.funcao = "enunciado interjetivo"

    if not verb_indices:
        text = _join_tokens(word.token for word in words)
        phrases.append({"tipo": "frase nominal", "texto": text})
        warnings.append(
            "Não foi identificado verbo; portanto, há uma frase nominal ou uma forma verbal não reconhecida."
        )
        return {
            "sujeito": "não se aplica sem oração reconhecida",
            "tipo_sujeito": "não identificado",
            "predicado": "não identificado",
            "tipo_predicado": "não identificado",
            "oracoes": 0,
            "termos": phrases,
            "avisos": warnings,
        }

    main_verb = verb_indices[0]
    lemma = words[main_verb].subclasse.replace("verbo ", "").split("/")[0]
    # Se houver advérbio deslocado e vírgula antes do verbo, ele não integra o sujeito.
    subject_start = 0
    comma_before = [i for i in range(main_verb) if words[i].token == ","]
    if comma_before:
        subject_start = comma_before[-1] + 1

    subject_indices = _content_indices(words, subject_start, main_verb)
    subject_nominals = [
        i
        for i in subject_indices
        if words[i].classe in {"substantivo", "pronome", "numeral"}
    ]
    if not subject_nominals:
        subject_nominals = [i for i in subject_indices if words[i].classe == "adjetivo"]

    impersonal_lemmas = {"haver"} if words[main_verb].subclasse == "verbo haver" else set()
    postposed_subject_indices: set[int] = set()
    if impersonal_lemmas:
        subject_text = "oração sem sujeito (hipótese)"
        subject_type = "inexistente"
    elif subject_nominals:
        subject_text = _join_tokens(words[i].token for i in subject_indices)
        nuclei = [
            i
            for i in subject_nominals
            if words[i].normalized not in PREPOSITION_CONTRACTIONS
        ]
        subject_type = "composto" if len(nuclei) > 1 and any(
            words[i].normalized == "e" for i in range(subject_start, main_verb)
        ) else "simples"
        _mark_nominal_group(words, subject_indices, "núcleo do sujeito")
        phrases.append({"tipo": f"sujeito {subject_type}", "texto": subject_text})
    else:
        possible_after = [
            i
            for i in range(main_verb + 1, len(words))
            if words[i].classe != "pontuação"
        ]
        group: list[int] = []
        if normalize(lemma) in INTRANSITIVE_VERBS and possible_after:
            for idx in possible_after:
                if words[idx].classe in {"advérbio", "conjunção", "preposição"} and not group:
                    continue
                if words[idx].classe in {"advérbio", "conjunção", "preposição"} and group:
                    break
                group.append(idx)
            if any(
                words[i].classe in {"substantivo", "pronome", "numeral"}
                for i in group
            ):
                postposed_subject_indices = set(group)
                subject_text = _join_tokens(words[i].token for i in group)
                subject_type = "simples posposto"
                _mark_nominal_group(words, group, "núcleo do sujeito")
                phrases.append({"tipo": "sujeito simples posposto", "texto": subject_text})
            else:
                group = []
        if not group:
            subject_text = "oculto, indeterminado ou posposto"
            subject_type = "não expresso antes do verbo"
            warnings.append(
                "O sujeito não aparece claramente antes do verbo. Ele pode estar oculto, indeterminado ou depois do verbo."
            )

    end = len(words)
    while end > 0 and words[end - 1].classe == "pontuação":
        end -= 1
    predicate_indices = list(range(main_verb, end))
    predicate_text = _join_tokens(words[i].token for i in predicate_indices)

    words[main_verb].funcao = "núcleo do predicado"
    for idx in verb_indices[1:]:
        words[idx].funcao = "verbo de outra oração ou parte de locução verbal"

    is_linking = normalize(lemma) in LINKING_VERBS
    has_predicative = False
    objects: list[dict] = []

    after = [
        i
        for i in range(main_verb + 1, end)
        if words[i].classe not in {"pontuação", "conjunção"}
    ]

    # Circunstâncias adverbiais são marcadas independentemente dos complementos.
    for idx in after:
        if words[idx].classe == "advérbio":
            subtype = words[idx].subclasse.split(" ")[0]
            words[idx].funcao = f"adjunto adverbial de {subtype}"
            phrases.append(
                {
                    "tipo": words[idx].funcao,
                    "texto": words[idx].token,
                }
            )

    if is_linking:
        candidates = [
            i
            for i in after
            if words[i].classe in {"adjetivo", "substantivo", "pronome", "numeral"}
        ]
        if candidates:
            pred_idx = candidates[0]
            words[pred_idx].funcao = "núcleo do predicativo do sujeito"
            group = [
                i
                for i in after
                if i <= pred_idx or (
                    i > pred_idx
                    and words[i].classe in {"adjetivo", "advérbio"}
                )
            ]
            pred_text = _join_tokens(words[i].token for i in group)
            phrases.append({"tipo": "predicativo do sujeito", "texto": pred_text})
            has_predicative = True
    else:
        predicative_candidates = [
            i
            for i in after
            if words[i].classe == "adjetivo"
            and i not in postposed_subject_indices
            and (i == main_verb + 1 or words[i - 1].classe != "artigo")
        ]
        if normalize(lemma) in ACTION_WITH_SUBJECT_PREDICATIVE and predicative_candidates:
            pred_idx = predicative_candidates[0]
            words[pred_idx].funcao = "núcleo do predicativo do sujeito"
            phrases.append(
                {"tipo": "predicativo do sujeito", "texto": words[pred_idx].token}
            )
            has_predicative = True

        # Divide a parte pós-verbal em grupos simples, respeitando preposições e advérbios.
        cursor = main_verb + 1
        while cursor < end:
            if (
                words[cursor].classe in {"pontuação", "conjunção", "advérbio"}
                or cursor in postposed_subject_indices
                or words[cursor].funcao == "núcleo do predicativo do sujeito"
            ):
                cursor += 1
                continue
            group_start = cursor
            introduced = words[cursor].classe == "preposição"
            cursor += 1
            while cursor < end:
                current = words[cursor]
                if current.classe in {"pontuação", "conjunção", "advérbio"}:
                    break
                if current.classe == "preposição" and cursor > group_start:
                    break
                cursor += 1
            group_indices = list(range(group_start, cursor))
            group_indices = [
                i
                for i in group_indices
                if i not in postposed_subject_indices
                and words[i].funcao != "núcleo do predicativo do sujeito"
            ]
            if not group_indices:
                continue
            if not any(
                words[i].classe in {"substantivo", "pronome", "numeral"}
                for i in group_indices
            ) and not any(words[i].classe == "adjetivo" for i in group_indices):
                continue
            preposition = words[group_indices[0]].normalized if introduced else ""
            is_locative = (
                introduced
                and normalize(lemma) in LOCATIVE_VERBS
                and preposition in normalized_set("a de em para até")
            )
            object_type = (
                "adjunto adverbial de lugar"
                if is_locative
                else ("objeto indireto" if introduced else "objeto direto")
            )
            _mark_nominal_group(words, group_indices, f"núcleo do {object_type}")
            if introduced:
                words[group_start].funcao = (
                    "preposição introdutora do adjunto adverbial"
                    if is_locative
                    else "preposição introdutora do objeto indireto"
                )
            object_text = _join_tokens(words[i].token for i in group_indices)
            item = {"tipo": object_type, "texto": object_text}
            phrases.append(item)
            if not is_locative:
                objects.append(item)

    if has_predicative and not is_linking:
        predicate_type = "verbo-nominal (hipótese)"
    elif has_predicative:
        predicate_type = "nominal"
    else:
        predicate_type = "verbal"

    phrases.insert(1 if phrases else 0, {"tipo": f"predicado {predicate_type}", "texto": predicate_text})

    # Uma aproximação transparente da quantidade de orações.
    finite_verbs = [
        i
        for i in verb_indices
        if not any(
            form in words[i].morfologia for form in ("infinitivo", "gerúndio", "particípio")
        )
    ]
    clause_count = max(1, len(finite_verbs))
    if clause_count > 1:
        warnings.append(
            "Há mais de uma forma verbal finita. A divisão e a classificação das orações exigem observar os conectores."
        )

    return {
        "sujeito": subject_text,
        "tipo_sujeito": subject_type,
        "predicado": predicate_text,
        "tipo_predicado": predicate_type,
        "verbo_principal": words[main_verb].token,
        "complementos": objects,
        "oracoes": clause_count,
        "termos": phrases,
        "avisos": warnings,
    }


def analyze_sentence(sentence: str) -> dict:
    sentence = re.sub(r"\s+", " ", sentence.strip())
    if not sentence:
        raise ValueError("Digite uma frase para analisar.")
    if len(sentence) > 500:
        raise ValueError("Use uma frase de até 500 caracteres por análise.")

    tokens = TOKEN_RE.findall(sentence)
    if not tokens:
        raise ValueError("Não foi possível identificar palavras nessa entrada.")

    words: list[WordAnalysis] = []
    for index, token in enumerate(tokens):
        words.append(_classify_word(token, index, tokens, words))

    syntax = _syntactic_analysis(words)
    low_confidence = [word.token for word in words if word.confianca < 65]
    ambiguous = [word.token for word in words if word.alternativas]

    return {
        "frase": sentence,
        "palavras": [word.to_dict() for word in words],
        "sintaxe": syntax,
        "qualidade": {
            "confianca_media": round(
                sum(word.confianca for word in words) / len(words)
            ),
            "baixa_confianca": low_confidence,
            "ambiguidades": ambiguous,
            "nota": (
                "Esta é uma hipótese didática baseada no contexto. Confira especialmente "
                "as palavras marcadas como ambíguas."
            ),
        },
        "legenda": CLASS_DESCRIPTIONS,
    }


if __name__ == "__main__":
    import json
    import sys

    sample = " ".join(sys.argv[1:]) or "O menino comprou um livro ontem."
    print(json.dumps(analyze_sentence(sample), ensure_ascii=False, indent=2))
