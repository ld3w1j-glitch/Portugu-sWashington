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
            "ariam ariamos arei aras ara aremos areis arao ando ado "
            "e es emos em asse asses assemos assem ares armos aredes"
        ).split()
    elif ending == "er":
        tails = (
            "o es e em emos ia ias iam iamos i este eu eram eria erias eriam "
            "eriamos erei eras era eremos ereis erao endo ido "
            "a as am amos esse esses essemos essem eres ermos erdes"
        ).split()
    else:
        tails = (
            "o es e em imos ia ias iam iamos i iste iu iram iria irias iriam "
            "iriamos irei iras ira iremos ireis irao indo ido "
            "a as am amos isse isses issemos issem ires irmos irdes"
        ).split()
    forms.update(stem + tail for tail in tails)
    return {normalize(form) for form in forms}


VERB_FORMS: dict[str, str] = {}
for _lemma in REGULAR_VERBS:
    for _form in build_regular_forms(_lemma):
        VERB_FORMS[_form] = _lemma
VERB_FORMS.update(IRREGULAR_FORMS)

# ---------------------------------------------------------------------------
# Camada ampliada do motor 2.0
# ---------------------------------------------------------------------------

ENGINE_VERSION = "2.0"

EXTRA_REGULAR_VERBS = normalized_set(
    """
    abandonar aceitar acompanhar acontecer acordar adicionar admitir agradecer alugar
    alcançar andar anunciar aparecer aplicar apresentar aproveitar aprovar avisar
    beber buscar calcular causar começar comentar compreender concordar conhecer consultar
    continuar conversar corrigir criar cuidar deixar depender desejar descobrir
    considerar discutir ensinar entender entrar enviar esperar esquecer evitar fechar formar ganhar gerar
    identificar informar iniciar instalar lembrar levar ligar machucar mudar necessitar
    mostrar obedecer observar oferecer organizar pagar passar perceber permanecer pesquisar
    planejar praticar preparar produzir publicar reconhecer registrar retornar salvar
    significar solicitar terminar tentar utilizar vender viajar visitar
    """
)

for _lemma in EXTRA_REGULAR_VERBS:
    if _lemma.endswith(("ar", "er", "ir")):
        for _form in build_regular_forms(_lemma):
            VERB_FORMS.setdefault(_form, _lemma)

EXTRA_IRREGULAR_FORMS = {
    # saber
    "sei": "saber",
    "sabe": "saber",
    "sabem": "saber",
    "sabia": "saber",
    "soube": "saber",
    "souberam": "saber",
    # trazer
    "trago": "trazer",
    "traz": "trazer",
    "trazem": "trazer",
    "trouxe": "trazer",
    "trouxeram": "trazer",
    # pôr
    "ponho": "pôr",
    "poe": "pôr",
    "poem": "pôr",
    "pus": "pôr",
    "pos": "pôr",
    "puseram": "pôr",
    # pedir
    "peco": "pedir",
    "pede": "pedir",
    "pedem": "pedir",
    "pediu": "pedir",
    "pediram": "pedir",
    # conseguir
    "consigo": "conseguir",
    "consegue": "conseguir",
    "conseguem": "conseguir",
    "conseguiu": "conseguir",
    "conseguiram": "conseguir",
    # dormir
    "durmo": "dormir",
    "dorme": "dormir",
    "dormem": "dormir",
    "dormiu": "dormir",
    "dormiram": "dormir",
    # sentir
    "sinto": "sentir",
    "sente": "sentir",
    "sentem": "sentir",
    "sentiu": "sentir",
    "sentiram": "sentir",
    # ouvir
    "ouco": "ouvir",
    "ouve": "ouvir",
    "ouvem": "ouvir",
    "ouviu": "ouvir",
    "ouviram": "ouvir",
    # sair/cair
    "saio": "sair",
    "sai": "sair",
    "saem": "sair",
    "saiu": "sair",
    "sairam": "sair",
    "caio": "cair",
    "cai": "cair",
    "caem": "cair",
    "caiu": "cair",
    "cairam": "cair",
    # manter
    "mantenho": "manter",
    "mantem": "manter",
    "mantemos": "manter",
    "mantinha": "manter",
    "manteve": "manter",
    # dever
    "devo": "dever",
    "deve": "dever",
    "devem": "dever",
    "devia": "dever",
    "deveria": "dever",
    # poder
    "pude": "poder",
    "puderam": "poder",
    "podera": "poder",
    "poderia": "poder",
    # querer
    "quis": "querer",
    "quiseram": "querer",
    "queria": "querer",
    # dizer
    "digo": "dizer",
    "dizia": "dizer",
    "disseram": "dizer",
    # ver/vir
    "vemos": "ver",
    "viram": "ver",
    "vinha": "vir",
    "vinham": "vir",
    "venho": "vir",
    # ler/escrever
    "lemos": "ler",
    "leram": "ler",
    "escrevo": "escrever",
    "escreve": "escrever",
    "escrevem": "escrever",
    "escreveu": "escrever",
    "escreveram": "escrever",
    # dar
    "damos": "dar",
    "deram": "dar",
    "dava": "dar",
    # formas com alterações ortográficas
    "cheguei": "chegar",
    "fiquei": "ficar",
    "paguei": "pagar",
    "comecei": "começar",
    "conheci": "conhecer",
    "corrigi": "corrigir",
    "viajei": "viajar",
    # futuros do pretérito irregulares e frequentes
    "viria": "vir",
    "viriam": "vir",
    "diria": "dizer",
    "diriam": "dizer",
    "faria": "fazer",
    "fariam": "fazer",
    "teria": "ter",
    "teriam": "ter",
    "seria": "ser",
    "seriam": "ser",
    "estaria": "estar",
    "estariam": "estar",
    # futuros irregulares ou muito frequentes
    "sera": "ser",
    "serao": "ser",
    "tera": "ter",
    "terao": "ter",
    "fara": "fazer",
    "farao": "fazer",
    "poderao": "poder",
    "devera": "dever",
    "deverao": "dever",
    "vira": "vir",
    "virao": "vir",
    # formas imperativas/subjuntivas muito frequentes
    "abra": "abrir",
    "abram": "abrir",
    "faca": "fazer",
    "facam": "fazer",
    "leia": "ler",
    "leiam": "ler",
    "saia": "sair",
    "saiam": "sair",
    "seja": "ser",
    "sejam": "ser",
    "venha": "vir",
    "venham": "vir",
    "veja": "ver",
    "vejam": "ver",
    "fosse": "ser/ir",
    "fossem": "ser/ir",
    "estivesse": "estar",
    "estivessem": "estar",
    "tivesse": "ter",
    "tivessem": "ter",
    "fizesse": "fazer",
    "fizessem": "fazer",
    "pudesse": "poder",
    "pudessem": "poder",
    "viesse": "vir",
    "viessem": "vir",
}
VERB_FORMS.update(EXTRA_IRREGULAR_FORMS)

ACCENTED_VERB_FORMS.update(
    {
        "põe": "pôr",
        "põem": "pôr",
        "mantém": "manter",
        "mantêm": "manter",
        "lê": "ler",
        "vêem": "ver",
        "saí": "sair",
        "caí": "cair",
    }
)

COMMON_ADJECTIVES.update(
    normalized_set(
        """
        antigo antiga atento atenta atual automático automática brasileiro brasileira
        cansado cansada caro cara completo completa correto correta dedicado dedicada
        diferente disponíveis disponível eficiente feliz importante impossível
        interessado interessada livre local necessário necessária novo nova ótimo ótima
        pequeno pequena possível principal provável rápido rápida responsável simples
        silencioso silenciosa suficiente verdadeiro verdadeira
        """
    )
)

COMMON_NOUNS.update(
    normalized_set(
        """
        atividade atividades ajuda aluno alunos análise análises ano anos apoio arquivo
        arquivos aula aulas bairro caderno cadernos candidato candidatos carro carros
        casa casas cidade cidades cliente clientes computador computadores conteúdo
        conteúdos curso cursos dia dias diretor diretora dúvida dúvidas equipe equipes
        escola escolas exercício exercícios funcionário funcionários história horas
        informação informações lugar lugares material materiais mercadoria mercadorias
        mês meses notícia notícias palavra palavras pergunta perguntas problema problemas
        projeto projetos relatório relatórios resposta respostas música músicas sistema sistemas tarefa
        tarefas texto textos usuário usuários vaga vagas
        """
    )
)

PERSONAL_SUBJECT_PRONOUNS = normalized_set(
    "eu tu ele ela nós vós eles elas você vocês a gente"
)

AUXILIARY_VERBS = normalized_set(
    "ter haver ser estar ir poder dever querer começar continuar deixar acabar voltar"
)

IMPERSONAL_WEATHER_VERBS = normalized_set(
    "chover nevar gear trovejar relampejar amanhecer anoitecer ventar"
)

SPEECH_COGNITION_VERBS = normalized_set(
    "achar acreditar afirmar compreender considerar dizer entender esperar explicar "
    "imaginar informar perceber perguntar responder saber supor desejar querer"
)

OBJECT_PREDICATIVE_VERBS = normalized_set(
    "achar considerar declarar eleger julgar nomear tornar"
)

TIME_NOUNS = normalized_set(
    "agora ano anos dia dias hora horas hoje manhã mês meses noite ontem tarde semana semanas"
)

PLACE_NOUNS = normalized_set(
    "aqui ali casa cidade escola fora dentro lugar mercado rua trabalho pouso alegre"
)

ABSTRACT_NOUNS = normalized_set(
    """
    amor aversão certeza confiança desejo dúvida esperança medo necessidade orgulho
    preocupação referência respeito saudade vontade
    """
)

IMPERATIVE_FORMS = normalized_set(
    """
    abra abram faça façam fale falem leia leiam olhe olhem preste prestem responda
    respondam saia saiam seja sejam venha venham veja vejam
    """
)

COORDINATING_CONNECTORS = {
    "e": "coordenada sindética aditiva",
    "nem": "coordenada sindética aditiva",
    "mas": "coordenada sindética adversativa",
    "porem": "coordenada sindética adversativa",
    "contudo": "coordenada sindética adversativa",
    "todavia": "coordenada sindética adversativa",
    "entretanto": "coordenada sindética adversativa",
    "ou": "coordenada sindética alternativa",
    "logo": "coordenada sindética conclusiva",
    "portanto": "coordenada sindética conclusiva",
    "pois": "coordenada sindética conclusiva ou explicativa",
}

SUBORDINATING_CONNECTORS = {
    "porque": "subordinada adverbial causal",
    "como": "subordinada adverbial causal, comparativa ou conformativa",
    "quando": "subordinada adverbial temporal",
    "enquanto": "subordinada adverbial temporal",
    "embora": "subordinada adverbial concessiva",
    "conquanto": "subordinada adverbial concessiva",
    "caso": "subordinada adverbial condicional",
    "se": "subordinada adverbial condicional ou substantiva integrante",
    "conforme": "subordinada adverbial conformativa",
    "consoante": "subordinada adverbial conformativa",
}

# A regência é registrada apenas quando o uso mais comum é suficientemente
# estável. Casos polissêmicos continuam marcados como hipóteses.
VERB_FRAMES = {
    "amar": {"tipo": "VTD", "preps": set()},
    "analisar": {"tipo": "VTD", "preps": set()},
    "aprender": {"tipo": "VTD", "preps": set()},
    "aprovar": {"tipo": "VTD", "preps": set()},
    "buscar": {"tipo": "VTD", "preps": set()},
    "chamar": {"tipo": "VTD", "preps": set()},
    "comer": {"tipo": "VTD", "preps": set()},
    "comprar": {"tipo": "VTD", "preps": set()},
    "compreender": {"tipo": "VTD", "preps": set()},
    "conhecer": {"tipo": "VTD", "preps": set()},
    "corrigir": {"tipo": "VTD", "preps": set()},
    "criar": {"tipo": "VTD", "preps": set()},
    "encontrar": {"tipo": "VTD", "preps": set()},
    "entender": {"tipo": "VTD", "preps": set()},
    "estudar": {"tipo": "VTD ou VI", "preps": set()},
    "fazer": {"tipo": "VTD ou impessoal", "preps": set()},
    "ler": {"tipo": "VTD", "preps": set()},
    "observar": {"tipo": "VTD", "preps": set()},
    "produzir": {"tipo": "VTD", "preps": set()},
    "resolver": {"tipo": "VTD", "preps": set()},
    "usar": {"tipo": "VTD", "preps": set()},
    "ver": {"tipo": "VTD", "preps": set()},
    "vender": {"tipo": "VTD", "preps": set()},
    "alugar": {"tipo": "VTD", "preps": set()},
    "beber": {"tipo": "VTD", "preps": set()},
    "ter": {"tipo": "VTD", "preps": set()},
    "haver": {"tipo": "VTD impessoal", "preps": set()},
    "considerar": {"tipo": "VTD", "preps": set()},
    "machucar": {"tipo": "VTD ou pronominal", "preps": set()},
    "gostar": {"tipo": "VTI", "preps": {"de"}},
    "confiar": {"tipo": "VTI", "preps": {"em"}},
    "obedecer": {"tipo": "VTI", "preps": {"a"}},
    "precisar": {"tipo": "VTI", "preps": {"de"}},
    "depender": {"tipo": "VTI", "preps": {"de"}},
    "lembrar": {"tipo": "VTD ou VTI", "preps": {"de"}},
    "assistir": {"tipo": "VTI ou VTD", "preps": {"a"}},
    "responder": {"tipo": "VTDI ou VTD", "preps": {"a"}},
    "perguntar": {"tipo": "VTDI", "preps": {"a", "para"}},
    "dar": {"tipo": "VTDI", "preps": {"a", "para"}},
    "dizer": {"tipo": "VTDI", "preps": {"a", "para"}},
    "entregar": {"tipo": "VTDI", "preps": {"a", "para"}},
    "enviar": {"tipo": "VTDI", "preps": {"a", "para"}},
    "explicar": {"tipo": "VTDI", "preps": {"a", "para"}},
    "mostrar": {"tipo": "VTDI", "preps": {"a", "para"}},
    "oferecer": {"tipo": "VTDI", "preps": {"a", "para"}},
    "pedir": {"tipo": "VTDI", "preps": {"a", "para"}},
    "chegar": {"tipo": "VI", "preps": set(), "locativo": True},
    "correr": {"tipo": "VI", "preps": set()},
    "dormir": {"tipo": "VI", "preps": set()},
    "entrar": {"tipo": "VI", "preps": set(), "locativo": True},
    "existir": {"tipo": "VI", "preps": set()},
    "ir": {"tipo": "VI", "preps": set(), "locativo": True},
    "morar": {"tipo": "VI", "preps": set(), "locativo": True},
    "nascer": {"tipo": "VI", "preps": set(), "locativo": True},
    "sair": {"tipo": "VI", "preps": set(), "locativo": True},
    "viajar": {"tipo": "VI", "preps": set(), "locativo": True},
    "voltar": {"tipo": "VI", "preps": set(), "locativo": True},
    "ser": {"tipo": "VL", "preps": set()},
    "estar": {"tipo": "VL", "preps": set()},
    "ficar": {"tipo": "VL ou VI", "preps": set(), "locativo": True},
    "parecer": {"tipo": "VL", "preps": set()},
    "permanecer": {"tipo": "VL ou VI", "preps": set(), "locativo": True},
    "continuar": {"tipo": "VL ou auxiliar", "preps": set()},
}


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


# ---------------------------------------------------------------------------
# Análise contextual 2.0
# ---------------------------------------------------------------------------

CLITIC_SUFFIXES = {
    "me": "me",
    "te": "te",
    "se": "se",
    "nos": "nos",
    "vos": "vos",
    "lhe": "lhe",
    "lhes": "lhes",
    "o": "o",
    "a": "a",
    "os": "os",
    "as": "as",
    "lo": "o",
    "la": "a",
    "los": "os",
    "las": "as",
}

IRREGULAR_PARTICIPLES = {
    "aberto": "abrir",
    "aberta": "abrir",
    "abertos": "abrir",
    "abertas": "abrir",
    "coberto": "cobrir",
    "coberta": "cobrir",
    "dito": "dizer",
    "dita": "dizer",
    "eleito": "eleger",
    "eleita": "eleger",
    "entregue": "entregar",
    "entregues": "entregar",
    "escrito": "escrever",
    "escrita": "escrever",
    "escritos": "escrever",
    "escritas": "escrever",
    "feito": "fazer",
    "feita": "fazer",
    "feitos": "fazer",
    "feitas": "fazer",
    "ganho": "ganhar",
    "ganha": "ganhar",
    "morto": "morrer",
    "morta": "morrer",
    "pago": "pagar",
    "paga": "pagar",
    "posto": "pôr",
    "posta": "pôr",
    "preso": "prender",
    "presa": "prender",
    "visto": "ver",
    "vista": "ver",
}


def _tokenize_sentence(sentence: str) -> list[str]:
    """Tokeniza e separa pronomes enclíticos sem quebrar palavras compostas."""
    initial = TOKEN_RE.findall(sentence)
    result: list[str] = []
    for token in initial:
        if "-" not in token or not token[:1].isalpha():
            result.append(token)
            continue
        parts = token.split("-")
        suffix = normalize(parts[-1])
        base = "-".join(parts[:-1])
        base_normalized = normalize(base)
        if (
            suffix in CLITIC_SUFFIXES
            and (
                base_normalized in VERB_FORMS
                or base_normalized.endswith(("ar", "er", "ir", "ou", "eu", "iu", "am", "em"))
            )
        ):
            result.extend([base, CLITIC_SUFFIXES[suffix]])
        else:
            result.append(token)
    return result


def _previous_lexical(words: list[WordAnalysis], index: int) -> int | None:
    for cursor in range(index - 1, -1, -1):
        if words[cursor].classe != "pontuação":
            return cursor
    return None


def _next_lexical(words: list[WordAnalysis], index: int) -> int | None:
    for cursor in range(index + 1, len(words)):
        if words[cursor].classe != "pontuação":
            return cursor
    return None


def _set_analysis(
    word: WordAnalysis,
    classe: str,
    subclasse: str,
    explicacao: str,
    confianca: int,
    morfologia: list[str] | None = None,
    alternativas: list[str] | None = None,
) -> None:
    word.classe = classe
    word.subclasse = subclasse
    word.explicacao = explicacao
    word.confianca = confianca
    if morfologia is not None:
        word.morfologia = morfologia
    if alternativas is not None:
        word.alternativas = alternativas


def _infer_regular_lemma(form: str) -> tuple[str, str] | None:
    """Infere lemas regulares somente a partir de terminações informativas."""
    form = normalize(form)
    patterns = (
        ("ariamos", "ar", "futuro do pretérito"),
        ("eriamos", "er", "futuro do pretérito"),
        ("iriamos", "ir", "futuro do pretérito"),
        ("assemos", "ar", "pretérito imperfeito do subjuntivo"),
        ("essemos", "er", "pretérito imperfeito do subjuntivo"),
        ("issemos", "ir", "pretérito imperfeito do subjuntivo"),
        ("avam", "ar", "pretérito imperfeito do indicativo"),
        ("iamos", "er", "pretérito imperfeito do indicativo"),
        ("aram", "ar", "pretérito perfeito do indicativo"),
        ("eram", "er", "pretérito perfeito ou imperfeito"),
        ("iram", "ir", "pretérito perfeito do indicativo"),
        ("ando", "ar", "gerúndio"),
        ("endo", "er", "gerúndio"),
        ("indo", "ir", "gerúndio"),
        ("ado", "ar", "particípio"),
        ("ido", "er", "particípio"),
        ("aria", "ar", "futuro do pretérito"),
        ("eria", "er", "futuro do pretérito"),
        ("iria", "ir", "futuro do pretérito"),
        ("amos", "ar", "presente ou pretérito perfeito"),
        ("emos", "er", "presente do indicativo"),
        ("imos", "ir", "presente ou pretérito perfeito"),
        ("ava", "ar", "pretérito imperfeito do indicativo"),
        ("iam", "er", "pretérito imperfeito do indicativo"),
        ("ou", "ar", "pretérito perfeito do indicativo"),
        ("eu", "er", "pretérito perfeito do indicativo"),
        ("iu", "ir", "pretérito perfeito do indicativo"),
        ("ei", "ar", "pretérito perfeito do indicativo"),
    )
    for ending, infinitive_ending, tense in patterns:
        if form.endswith(ending) and len(form) > len(ending) + 2:
            stem = form[: -len(ending)]
            return stem + infinitive_ending, tense
    return None


def _verb_features(token: str, lemma: str, morphology: list[str]) -> list[str]:
    word = normalize(token)
    result = [item for item in morphology if not item.startswith("tempo provável:")]
    if any(item in result for item in ("infinitivo", "gerúndio", "particípio")):
        return result

    first_person_singular = normalized_set(
        "sou estou tenho vou posso quero faço digo vejo venho ponho sei leio trago "
        "peço consigo durmo sinto ouço saio caio mantenho devo dou fui vi li"
    )
    if word in first_person_singular or (
        word.endswith("o") and lemma.endswith(("ar", "er", "ir"))
    ):
        result.extend(["1ª pessoa", "singular"])
    elif word.endswith("mos"):
        result.extend(["1ª pessoa", "plural"])
    elif word.endswith(("am", "em")) or token.lower().endswith("ão"):
        result.extend(["3ª pessoa", "plural"])
    else:
        result.extend(["3ª pessoa ou forma dependente do contexto", "singular"])

    if word.endswith(("ava", "avas", "avamos", "avam", "ia", "ias", "iamos", "iam")):
        result.append("tempo provável: pretérito imperfeito do indicativo")
    elif word.endswith(("ou", "eu", "iu", "aram", "eram", "iram")) or word in {
        "fui",
        "foi",
        "foram",
        "vi",
        "li",
        "fez",
        "deu",
        "disse",
        "veio",
        "houve",
    }:
        result.append("tempo provável: pretérito perfeito do indicativo")
    elif word.endswith(("aria", "eria", "iria", "ariam", "eriam", "iriam")):
        result.append("tempo provável: futuro do pretérito")
    elif token.lower().endswith(("rá", "rão")):
        result.append("tempo provável: futuro do presente")
    else:
        result.append("tempo provável: presente ou forma dependente do contexto")
    return list(dict.fromkeys(result))


def _refine_morphology(words: list[WordAnalysis], sentence: str) -> None:
    """Segunda passagem: usa vizinhança e estrutura para resolver homônimos."""
    for index, word in enumerate(words):
        if word.classe == "pontuação":
            continue
        previous_index = _previous_lexical(words, index)
        next_index = _next_lexical(words, index)
        previous = words[previous_index] if previous_index is not None else None
        following = words[next_index] if next_index is not None else None
        normalized = word.normalized

        if (
            normalized in PROPER_NOUNS
            or (
                word.token[:1].isupper()
                and index == 0
                and following
                and following.classe == "verbo"
                and normalized not in CONJUNCTIONS
                and normalized not in ADVERBS
                and normalized not in PREPOSITIONS
            )
            or (
                word.token[:1].isupper()
                and previous
                and previous.token[:1].isupper()
                and previous.classe in {"substantivo", "adjetivo"}
            )
        ) and word.classe in {"substantivo", "adjetivo"}:
            _set_analysis(
                word,
                "substantivo",
                "próprio",
                "Nomeia um ser ou lugar individualizado; a maiúscula reforça essa leitura.",
                94 if normalized in PROPER_NOUNS else 78,
                ["substantivo próprio"],
            )

        if normalized in IRREGULAR_PARTICIPLES:
            lemma = IRREGULAR_PARTICIPLES[normalized]
            _set_analysis(
                word,
                "verbo",
                f"verbo {lemma}",
                f"É particípio irregular ou especial do verbo “{lemma}”.",
                96,
                [f"forma do verbo {lemma}", "particípio", "forma nominal"],
            )
            continue

        if (
            word.classe != "verbo"
            and normalized.endswith(("ados", "adas", "idos", "idas"))
        ):
            singular = normalized[:-1]
            known_lemmas = set(REGULAR_VERBS) | EXTRA_REGULAR_VERBS
            if singular.endswith(("ado", "ada")):
                candidates = [singular[:-3] + "ar"]
            else:
                candidates = [singular[:-3] + "er", singular[:-3] + "ir"]
            lemma = next((item for item in candidates if item in known_lemmas), "")
            if lemma:
                _set_analysis(
                    word,
                    "verbo",
                    f"verbo {lemma} (lema estimado)",
                    "A terminação e a concordância indicam um particípio flexionado.",
                    84,
                    [f"forma provável do verbo {lemma}", "particípio", "forma nominal", "plural"],
                    ["adjetivo formado de particípio, conforme o contexto"],
                )

        if normalized in {"como"}:
            if (
                previous
                and previous.normalized in PERSONAL_SUBJECT_PRONOUNS
                and following
                and following.classe not in {"verbo", "conjunção"}
            ):
                _set_analysis(
                    word,
                    "verbo",
                    "verbo comer",
                    "Depois de um pronome sujeito e antes de um grupo nominal, “como” indica o ato de comer.",
                    88,
                    ["forma do verbo comer", "forma finita", "1ª pessoa", "singular"],
                    ["conjunção ou advérbio em outro contexto"],
                )
            elif sentence.rstrip().endswith("?") and index <= 1:
                _set_analysis(
                    word,
                    "advérbio",
                    "interrogativo de modo",
                    "Introduz uma pergunta sobre o modo como algo acontece.",
                    91,
                    ["classe invariável"],
                    ["conjunção em outro contexto"],
                )

        if normalized == "que":
            previous_verbs = [
                item
                for item in words[:index]
                if item.classe == "verbo"
            ]
            time_construction = bool(
                previous
                and previous.normalized in TIME_NOUNS
                and previous_verbs
                and _word_lemma(previous_verbs[-1]) in {"fazer", "haver"}
            )
            if time_construction:
                _set_analysis(
                    word,
                    "conjunção",
                    "subordinativa temporal",
                    "Depois de uma expressão de tempo, introduz a oração que marca sua duração.",
                    83,
                    ["classe invariável"],
                    ["pronome relativo ou conjunção integrante em outro contexto"],
                )
            elif previous and previous.classe == "substantivo" and following:
                _set_analysis(
                    word,
                    "pronome",
                    "relativo",
                    "Retoma o substantivo anterior e introduz uma oração que o caracteriza.",
                    88,
                    ["classe invariável nesta forma"],
                    ["conjunção integrante em outro contexto"],
                )
            elif sentence.rstrip().endswith("?") and index == 0:
                _set_analysis(
                    word,
                    "pronome",
                    "interrogativo",
                    "Introduz uma pergunta e determina ou substitui um nome.",
                    87,
                    ["pronome interrogativo"],
                    ["conjunção em outro contexto"],
                )

        if normalized == "onde":
            if previous and (
                previous.normalized in PLACE_NOUNS
                or previous.classe == "substantivo"
            ):
                word.subclasse = "relativo locativo"
                word.explicacao = "Retoma um lugar mencionado anteriormente."
                word.confianca = 84
            elif sentence.rstrip().endswith("?"):
                _set_analysis(
                    word,
                    "advérbio",
                    "interrogativo de lugar",
                    "Pergunta pelo lugar relacionado à ação.",
                    91,
                    ["classe invariável"],
                    ["pronome relativo quando retoma um lugar"],
                )

        if normalized == "se":
            previous_is_verb = bool(previous and previous.classe == "verbo")
            next_is_verb = bool(following and following.classe == "verbo")
            begins_clause = previous is None or (
                previous_index is not None
                and any(
                    words[cursor].token in {",", ";", ".", "!", "?"}
                    for cursor in range(max(0, previous_index), index)
                )
            )
            if previous_is_verb or (
                next_is_verb
                and previous
                and previous.classe in {"pronome", "advérbio", "substantivo"}
            ):
                _set_analysis(
                    word,
                    "pronome",
                    "partícula pronominal",
                    "Liga-se ao verbo; a sintaxe decidirá se é reflexivo, apassivador ou índice de indeterminação.",
                    78,
                    ["classe invariável nesta forma"],
                    ["conjunção condicional ou integrante"],
                )
            elif begins_clause and next_is_verb:
                word.classe = "conjunção"
                word.subclasse = "condicional ou integrante"
                word.explicacao = "Introduz uma oração; o verbo anterior e o sentido definem se há condição ou integração."
                word.confianca = 78

        if normalized in {"o", "a", "os", "as"} and word.classe == "artigo":
            if following and following.classe == "verbo":
                previous_lemma = (
                    previous.subclasse.replace("verbo ", "").split("/")[0]
                    if previous and previous.classe == "verbo"
                    else ""
                )
                if "infinitivo" in following.morfologia or previous_lemma in {
                    "começar",
                    "continuar",
                    "voltar",
                }:
                    _set_analysis(
                        word,
                        "preposição",
                        "essencial",
                        "Liga a forma verbal anterior ao infinitivo.",
                        90,
                        ["classe invariável"],
                        ["artigo ou pronome em outro contexto"],
                    )
                elif previous:
                    _set_analysis(
                        word,
                        "pronome",
                        "pessoal oblíquo átono",
                        "Substitui um complemento verbal já conhecido no contexto.",
                        86,
                        ["pronome pessoal", "forma átona"],
                        ["artigo definido em outro contexto"],
                    )

        if normalized in {"um", "uma"} and word.classe == "artigo":
            if previous and previous.normalized in {"so", "somente", "apenas", "exatamente"}:
                _set_analysis(
                    word,
                    "numeral",
                    "cardinal",
                    "A palavra de foco anterior destaca a quantidade exata.",
                    90,
                    ["cardinal", "classe variável em gênero"],
                    ["artigo indefinido em outro contexto"],
                )

        if normalized == "meio":
            if following and following.classe == "adjetivo":
                _set_analysis(
                    word,
                    "advérbio",
                    "intensidade",
                    "Equivale a “um pouco” e modifica o adjetivo seguinte.",
                    93,
                    ["classe invariável"],
                    ["numeral fracionário ou substantivo"],
                )
            elif following and following.classe == "substantivo":
                word.classe = "numeral"
                word.subclasse = "fracionário"
                word.explicacao = "Indica metade da quantidade expressa pelo nome."
                word.confianca = 91

        if normalized in {"muito", "pouco", "bastante", "tanto"}:
            if following and following.classe == "substantivo":
                _set_analysis(
                    word,
                    "pronome",
                    "indefinido adjetivo",
                    "Acompanha o substantivo e indica quantidade imprecisa.",
                    88,
                    ["classe variável conforme o contexto"],
                    ["advérbio quando modifica verbo, adjetivo ou advérbio"],
                )

        if normalized in {
            "muitos",
            "muitas",
            "poucos",
            "poucas",
            "bastantes",
            "tantos",
            "tantas",
            "todos",
            "todas",
            "alguns",
            "algumas",
            "varios",
            "varias",
        } and following and following.classe in {"artigo", "substantivo", "adjetivo"}:
            _set_analysis(
                word,
                "pronome",
                "indefinido adjetivo",
                "Acompanha um grupo nominal e indica totalidade ou quantidade não exata.",
                89,
                ["classe variável"],
                ["advérbio ou numeral em usos específicos"],
            )

        if normalized == "so":
            if following and following.classe == "substantivo":
                _set_analysis(
                    word,
                    "adjetivo",
                    "qualificativo",
                    "Caracteriza o nome com sentido de único ou desacompanhado.",
                    78,
                    ["classe variável"],
                    ["advérbio com sentido de somente"],
                )
            else:
                _set_analysis(
                    word,
                    "advérbio",
                    "exclusão",
                    "Equivale a “somente” no contexto.",
                    82,
                    ["classe invariável"],
                    ["adjetivo em outro contexto"],
                )

        if (
            word.classe == "substantivo"
            and word.confianca <= 60
            and previous
            and (
                previous.normalized in PERSONAL_SUBJECT_PRONOUNS
                or previous.classe in {"substantivo", "pronome", "advérbio"}
            )
        ):
            inference = _infer_regular_lemma(normalized)
            if inference:
                lemma, tense = inference
                _set_analysis(
                    word,
                    "verbo",
                    f"verbo {lemma} (lema estimado)",
                    f"A terminação e a posição na frase sugerem uma forma do verbo “{lemma}”.",
                    69,
                    [f"forma provável do verbo {lemma}", "forma finita", f"tempo provável: {tense}"],
                    ["substantivo ou adjetivo em outro contexto"],
                )

        if (
            word.classe == "substantivo"
            and word.confianca <= 60
            and normalized.endswith(("ando", "endo", "indo"))
        ):
            inference = _infer_regular_lemma(normalized)
            if inference:
                lemma, _ = inference
                _set_analysis(
                    word,
                    "verbo",
                    f"verbo {lemma} (lema estimado)",
                    "A terminação -ndo indica uma forma verbal no gerúndio.",
                    82,
                    [f"forma provável do verbo {lemma}", "gerúndio", "forma nominal"],
                )

        if (
            word.classe == "substantivo"
            and word.confianca <= 60
            and word.token[:1].isupper()
            and (
                index == 0
                or (previous and previous.token in {".", "!", "?"})
                or (following and following.classe in {"verbo", "substantivo"})
            )
        ):
            word.subclasse = "próprio (hipótese contextual)"
            word.explicacao = "A inicial maiúscula e a posição sugerem um nome próprio."
            word.confianca = 72

    # Flexões verbais são acrescentadas depois das correções contextuais.
    for word in words:
        if word.classe != "verbo":
            continue
        lemma = word.subclasse.replace("verbo ", "").split(" ")[0].split("/")[0]
        word.morfologia = _verb_features(word.token, lemma, word.morfologia)


@dataclass
class VerbGroup:
    indices: list[int]
    finite_index: int
    head_index: int
    lemma: str
    auxiliary_lemmas: list[str] = field(default_factory=list)

    @property
    def start(self) -> int:
        return min(self.indices)

    @property
    def end(self) -> int:
        return max(self.indices)


@dataclass
class ClauseSpan:
    indices: list[int]
    verb_group: VerbGroup
    connector_index: int | None = None
    tipo: str = ""


def _word_lemma(word: WordAnalysis) -> str:
    if word.classe != "verbo":
        return ""
    text = word.subclasse.replace("verbo ", "")
    return normalize(text.split(" ")[0].split("/")[0])


def _is_nominal_verb(word: WordAnalysis) -> bool:
    return any(
        item in word.morfologia for item in ("infinitivo", "gerúndio", "particípio")
    )


def _build_verb_groups(words: list[WordAnalysis]) -> list[VerbGroup]:
    verb_indices = [index for index, word in enumerate(words) if word.classe == "verbo"]
    groups: list[VerbGroup] = []
    used: set[int] = set()

    for position, index in enumerate(verb_indices):
        if index in used:
            continue
        word = words[index]
        lemma = _word_lemma(word)
        indices = [index]
        auxiliaries: list[str] = []
        head = index
        if not _is_nominal_verb(word) and lemma in AUXILIARY_VERBS:
            for candidate in verb_indices[position + 1 :]:
                if candidate - index > 5 or candidate in used:
                    break
                between = words[index + 1 : candidate]
                if any(
                    item.classe not in {"advérbio", "preposição", "pronome"}
                    for item in between
                ):
                    break
                if _is_nominal_verb(words[candidate]):
                    indices.append(candidate)
                    auxiliaries.append(lemma)
                    head = candidate
                    used.add(candidate)
                    break
        used.add(index)
        head_lemma = _word_lemma(words[head]) or lemma
        groups.append(
            VerbGroup(
                indices=indices,
                finite_index=index,
                head_index=head,
                lemma=head_lemma,
                auxiliary_lemmas=auxiliaries,
            )
        )

    for group in groups:
        if len(group.indices) > 1:
            for index in group.indices[:-1]:
                words[index].funcao = "verbo auxiliar da locução verbal"
            for index in range(group.indices[0] + 1, group.head_index):
                if words[index].classe == "preposição":
                    words[index].funcao = "elemento de ligação da locução verbal"
                elif words[index].classe == "pronome":
                    words[index].funcao = "pronome ligado à locução verbal"
            words[group.head_index].funcao = "núcleo verbal da locução"
        else:
            words[group.head_index].funcao = "núcleo do predicado"
    return groups


def _clause_connector(words: list[WordAnalysis], indices: list[int]) -> int | None:
    for position, index in enumerate(indices):
        word = words[index]
        if word.classe in {"pontuação", "advérbio"}:
            continue
        if word.classe == "conjunção" or (
            word.classe == "pronome" and "relativo" in word.subclasse
        ):
            return index
        break
    return None


def _build_clause_spans(
    words: list[WordAnalysis], groups: list[VerbGroup]
) -> list[ClauseSpan]:
    if not groups:
        return []
    starts: list[int] = [0]
    for previous, current in zip(groups, groups[1:]):
        between = list(range(previous.end + 1, current.start))
        connectors = [
            index
            for index in between
            if words[index].classe == "conjunção"
            or (words[index].classe == "pronome" and "relativo" in words[index].subclasse)
        ]
        punctuation = [
            index for index in between if words[index].token in {",", ";", ":"}
        ]
        if connectors:
            starts.append(connectors[-1])
        elif punctuation:
            starts.append(punctuation[-1] + 1)
        else:
            starts.append(current.start)

    # Um relativo pode aparecer antes do primeiro verbo: "O livro que comprei chegou".
    first_group = groups[0]
    relative_before = [
        index
        for index in range(0, first_group.start)
        if words[index].classe == "pronome" and "relativo" in words[index].subclasse
    ]
    detached_prefix: list[int] = []
    if relative_before and len(groups) > 1:
        starts[0] = relative_before[-1]
        detached_prefix = list(range(0, starts[0]))

    spans: list[ClauseSpan] = []
    for position, group in enumerate(groups):
        start = starts[position]
        end = starts[position + 1] if position + 1 < len(starts) else len(words)
        indices = list(range(start, end))
        spans.append(
            ClauseSpan(
                indices=indices,
                verb_group=group,
                connector_index=_clause_connector(words, indices),
            )
        )

    if detached_prefix:
        # O antecedente do relativo pertence à oração principal, normalmente
        # organizada pelo último grupo verbal.
        spans[-1].indices = detached_prefix + spans[-1].indices
    return spans


def _classify_clauses(words: list[WordAnalysis], spans: list[ClauseSpan]) -> None:
    subordinate_found = False
    for position, span in enumerate(spans):
        connector = words[span.connector_index] if span.connector_index is not None else None
        connector_word = connector.normalized if connector else ""
        if connector and connector.classe == "pronome" and "relativo" in connector.subclasse:
            left_comma = span.connector_index > 0 and words[span.connector_index - 1].token == ","
            span.tipo = (
                "oração subordinada adjetiva explicativa"
                if left_comma
                else "oração subordinada adjetiva restritiva"
            )
            subordinate_found = True
        elif connector_word in COORDINATING_CONNECTORS:
            span.tipo = "oração " + COORDINATING_CONNECTORS[connector_word]
        elif connector_word == "que":
            previous_group = spans[position - 1].verb_group if position > 0 else None
            if connector and "temporal" in connector.subclasse:
                span.tipo = "oração subordinada adverbial temporal"
            elif previous_group and previous_group.lemma in SPEECH_COGNITION_VERBS:
                span.tipo = "oração subordinada substantiva objetiva direta"
            else:
                span.tipo = "oração subordinada substantiva (hipótese)"
            subordinate_found = True
        elif connector_word == "se":
            previous_group = spans[position - 1].verb_group if position > 0 else None
            if previous_group and previous_group.lemma in SPEECH_COGNITION_VERBS:
                span.tipo = "oração subordinada substantiva objetiva direta"
            else:
                span.tipo = "oração subordinada adverbial condicional"
            subordinate_found = True
        elif connector_word in SUBORDINATING_CONNECTORS:
            span.tipo = "oração " + SUBORDINATING_CONNECTORS[connector_word]
            subordinate_found = True
        elif position > 0:
            span.tipo = "oração coordenada assindética ou justaposta"

    if len(spans) == 1:
        spans[0].tipo = spans[0].tipo or "oração absoluta (período simples)"
    else:
        for position, span in enumerate(spans):
            if span.tipo:
                continue
            if subordinate_found:
                span.tipo = "oração principal"
            elif position == 0:
                span.tipo = "oração coordenada assindética inicial"
            else:
                span.tipo = "oração coordenada assindética"

        if subordinate_found:
            # Em "Quando cheguei, ela saiu" ou "O livro que comprei chegou",
            # a oração sem conector próprio é a principal, ainda que venha depois.
            candidates = [
                span
                for span in spans
                if span.connector_index is None
                and (
                    not span.tipo
                    or "assindética" in span.tipo
                    or "justaposta" in span.tipo
                )
            ]
            if candidates:
                candidates[-1].tipo = "oração principal"

    for span in spans:
        if span.connector_index is not None:
            connector = words[span.connector_index]
            connector.funcao = "conector da " + span.tipo.replace("oração ", "")


def _nominal_groups(
    words: list[WordAnalysis], indices: list[int]
) -> list[dict]:
    groups: list[dict] = []
    current: list[int] = []
    prepositional = False
    prep = ""

    def flush() -> None:
        nonlocal current, prepositional, prep
        if current and any(
            words[index].classe in {"substantivo", "pronome", "numeral", "adjetivo"}
            for index in current
        ):
            groups.append(
                {
                    "indices": current[:],
                    "prepositional": prepositional,
                    "prep": prep,
                }
            )
        current = []
        prepositional = False
        prep = ""

    for position, index in enumerate(indices):
        word = words[index]
        if word.classe == "pontuação" or word.classe == "verbo":
            flush()
            continue
        if word.classe == "advérbio" or word.classe == "interjeição":
            flush()
            continue
        if word.classe == "conjunção":
            flush()
            continue
        if word.classe == "preposição":
            next_index = indices[position + 1] if position + 1 < len(indices) else None
            if (
                current
                and prepositional
                and words[current[-1]].token[:1].isupper()
                and next_index is not None
                and words[next_index].token[:1].isupper()
            ):
                current.append(index)
                continue
            flush()
            current = [index]
            prepositional = True
            prep = word.normalized
            continue
        if word.normalized in {"me", "te", "se", "lhe", "lhes", "nos", "vos", "o", "a", "os", "as"} and (
            "oblíquo" in word.subclasse or "partícula" in word.subclasse
        ):
            flush()
            continue
        if (
            current
            and not prepositional
            and words[current[-1]].classe == "substantivo"
            and word.classe in {"artigo", "pronome"}
        ):
            flush()
        current.append(index)
    flush()
    return groups


def _group_text(words: list[WordAnalysis], indices: list[int]) -> str:
    return _join_tokens(words[index].token for index in indices)


def _mark_group(
    words: list[WordAnalysis],
    indices: list[int],
    head_function: str,
) -> None:
    candidates = [
        index
        for index in indices
        if words[index].classe in {"substantivo", "pronome", "numeral"}
        and words[index].normalized not in {"me", "te", "se", "lhe", "lhes"}
    ]
    if not candidates:
        candidates = [index for index in indices if words[index].classe == "adjetivo"]
    if not candidates:
        return
    head = candidates[-1]
    words[head].funcao = head_function
    for index in indices:
        if index == head:
            continue
        if words[index].classe in {"artigo", "adjetivo", "pronome", "numeral"}:
            words[index].funcao = "adjunto adnominal"


def _subject_hint(word: WordAnalysis) -> str:
    normalized = word.normalized
    if "1ª pessoa" in word.morfologia and "singular" in word.morfologia:
        return "eu"
    if "1ª pessoa" in word.morfologia and "plural" in word.morfologia:
        return "nós"
    if normalized in normalized_set(
        "sou estou tenho vou posso quero faço digo vejo venho sei leio trago peço dou fui vi li"
    ):
        return "eu"
    if normalized.endswith("mos"):
        return "nós"
    lemma = _word_lemma(word)
    if normalized.endswith("ei") or (
        normalized.endswith("i") and lemma.endswith(("er", "ir"))
    ):
        return "eu"
    return "recuperável pela flexão verbal ou pelo contexto"


def _preposition_value(
    prep: str,
    group_indices: list[int],
    words: list[WordAnalysis],
    lemma: str,
) -> str:
    nouns = {words[index].normalized for index in group_indices}
    if nouns & TIME_NOUNS:
        return "tempo"
    if prep in {"em", "no", "na", "nos", "nas", "a", "ao", "para", "ate"} and (
        lemma in LOCATIVE_VERBS or nouns & PLACE_NOUNS
    ):
        return "lugar"
    if prep in {"com"}:
        return "companhia, instrumento ou modo"
    if prep in {"sem"}:
        return "modo ou ausência"
    if prep in {"por", "pelo", "pela"}:
        return "causa, meio ou percurso"
    if prep in {"de", "do", "da"} and lemma in {"sair", "vir", "voltar"}:
        return "origem"
    return "circunstância"


def _is_impersonal_use(
    words: list[WordAnalysis], span: ClauseSpan, lemma: str
) -> tuple[bool, str]:
    if lemma == "haver" and not span.verb_group.auxiliary_lemmas:
        return True, "haver com sentido de existir"
    if lemma in IMPERSONAL_WEATHER_VERBS:
        return True, "verbo que indica fenômeno da natureza"
    after = [
        words[index].normalized
        for index in span.indices
        if index > span.verb_group.end and words[index].classe != "pontuação"
    ]
    if lemma == "fazer" and any(item in TIME_NOUNS or item in {"frio", "calor"} for item in after):
        return True, "fazer indicando tempo decorrido ou fenômeno meteorológico"
    if lemma == "ser" and any(item in {"hora", "horas", "dia", "dias"} for item in after):
        return True, "ser indicando hora ou data"
    return False, ""


def _voice_and_se(
    words: list[WordAnalysis],
    span: ClauseSpan,
    frame: dict,
    after_groups: list[dict],
) -> tuple[str, str]:
    group = span.verb_group
    if (
        group.auxiliary_lemmas
        and "ser" in group.auxiliary_lemmas
        and "particípio" in words[group.head_index].morfologia
    ):
        return "voz passiva analítica", ""

    se_indices = [
        index
        for index in span.indices
        if words[index].normalized == "se"
        and words[index].classe == "pronome"
        and abs(index - group.finite_index) <= 2
    ]
    if not se_indices:
        return "voz ativa ou não marcada", ""
    se_index = se_indices[0]
    frame_type = frame.get("tipo", "")
    has_post_nominal = any(not item["prepositional"] for item in after_groups)
    if ("VTD" in frame_type or "VTDI" in frame_type) and has_post_nominal:
        words[se_index].funcao = "partícula apassivadora"
        words[se_index].subclasse = "pronome apassivador"
        words[se_index].confianca = max(words[se_index].confianca, 86)
        return "voz passiva sintética", "apassivador"
    if "VTI" in frame_type or frame_type.startswith(("VI", "VL")):
        words[se_index].funcao = "índice de indeterminação do sujeito"
        words[se_index].subclasse = "índice de indeterminação"
        words[se_index].confianca = max(words[se_index].confianca, 86)
        return "voz ativa com sujeito indeterminado", "indeterminador"
    words[se_index].funcao = "pronome reflexivo ou parte integrante do verbo (hipótese)"
    return "voz reflexiva ou pronominal (hipótese)", "reflexivo"


def _analyze_clause(
    words: list[WordAnalysis],
    span: ClauseSpan,
    warnings: list[str],
) -> dict:
    group = span.verb_group
    lemma = group.lemma
    frame = VERB_FRAMES.get(lemma, {"tipo": "regência não cadastrada", "preps": set()})
    clause_indices = [
        index for index in span.indices if words[index].classe != "pontuação"
    ]
    before = [index for index in span.indices if index < group.finite_index]
    after = [index for index in span.indices if index > group.end]
    if span.connector_index in before:
        before.remove(span.connector_index)

    before_groups = _nominal_groups(words, before)
    after_groups = _nominal_groups(words, after)
    explicit_candidates = [
        item
        for item in before_groups
        if not item["prepositional"]
        and any(
            words[index].classe in {"substantivo", "pronome", "numeral", "adjetivo"}
            for index in item["indices"]
        )
    ]
    structural_terms: list[dict] = []
    comma_positions = [
        index
        for index in span.indices
        if index < group.finite_index and words[index].token == ","
    ]
    appositive_groups: list[dict] = []
    if len(comma_positions) >= 2:
        appositive_groups = [
            item
            for item in explicit_candidates
            if min(item["indices"]) > comma_positions[0]
            and max(item["indices"]) < comma_positions[1]
        ]
        for item in appositive_groups:
            _mark_group(words, item["indices"], "núcleo do aposto")
            structural_terms.append(
                {"tipo": "aposto explicativo", "texto": _group_text(words, item["indices"])}
            )
        explicit_candidates = [
            item for item in explicit_candidates if item not in appositive_groups
        ]

    vocative_groups: list[dict] = []
    if comma_positions and words[group.finite_index].normalized in IMPERATIVE_FORMS:
        vocative_groups = [
            item
            for item in explicit_candidates
            if max(item["indices"]) < comma_positions[0]
        ]
        for item in vocative_groups:
            _mark_group(words, item["indices"], "núcleo do vocativo")
            structural_terms.append(
                {"tipo": "vocativo", "texto": _group_text(words, item["indices"])}
            )
        explicit_candidates = [
            item for item in explicit_candidates if item not in vocative_groups
        ]

    impersonal, impersonal_reason = _is_impersonal_use(words, span, lemma)
    voice, se_role = _voice_and_se(words, span, frame, after_groups)
    subject_groups: list[dict] = []
    subject_connector_indices: set[int] = set()
    subject_modifier_indices: set[int] = set()
    subject_text = ""
    subject_type = ""

    if impersonal:
        subject_text = "oração sem sujeito"
        subject_type = "inexistente"
    elif se_role == "indeterminador":
        subject_text = "sujeito indeterminado"
        subject_type = "indeterminado"
    elif explicit_candidates:
        # O grupo mais próximo do verbo tende a ser o sujeito. Grupos ligados
        # por "e" antes do verbo são reunidos como sujeito composto.
        subject_groups = [explicit_candidates[-1]]
        if len(explicit_candidates) >= 2:
            first = explicit_candidates[-2]
            between_start = max(first["indices"]) + 1
            between_end = min(subject_groups[0]["indices"])
            if any(
                words[index].normalized == "e"
                for index in range(between_start, between_end)
            ):
                subject_groups.insert(0, first)
        combined_indices = [
            index for item in subject_groups for index in item["indices"]
        ]
        if len(subject_groups) > 1:
            connectors = [
                index
                for index in before
                if min(combined_indices) < index < max(combined_indices)
                and words[index].normalized == "e"
            ]
            combined_indices.extend(connectors)
            subject_connector_indices.update(connectors)
            for connector_index in connectors:
                words[connector_index].funcao = "conector de núcleos do sujeito composto"
            combined_indices.sort()
        last_subject_index = max(combined_indices)
        next_comma = next(
            (
                comma
                for comma in comma_positions
                if comma > last_subject_index
            ),
            group.finite_index,
        )
        modifier_groups = [
            item
            for item in before_groups
            if item["prepositional"]
            and min(item["indices"]) > last_subject_index
            and max(item["indices"]) < next_comma
        ]
        subject_heads = {
            words[index].normalized
            for item in subject_groups
            for index in item["indices"]
            if words[index].classe == "substantivo"
        }
        subject_has_proper_name = any(
            words[index].subclasse == "próprio"
            or (
                words[index].classe == "substantivo"
                and words[index].token[:1].isupper()
            )
            for item in subject_groups
            for index in item["indices"]
        )
        for modifier in modifier_groups:
            subject_modifier_indices.update(modifier["indices"])
            proper_name_continuation = (
                subject_has_proper_name
                and all(
                    words[index].classe == "preposição"
                    or words[index].token[:1].isupper()
                    for index in modifier["indices"]
                )
            )
            if proper_name_continuation:
                words[modifier["indices"][0]].funcao = (
                    "elemento de ligação interno do nome próprio"
                )
                _mark_group(
                    words,
                    modifier["indices"],
                    "continuação do núcleo do sujeito (nome próprio)",
                )
                combined_indices.extend(modifier["indices"])
                continue
            modifier_type = (
                "complemento nominal"
                if subject_heads & ABSTRACT_NOUNS
                else "adjunto adnominal preposicionado"
            )
            words[modifier["indices"][0]].funcao = f"preposição introdutora do {modifier_type}"
            _mark_group(words, modifier["indices"], f"núcleo do {modifier_type}")
            structural_terms.append(
                {
                    "tipo": modifier_type,
                    "texto": _group_text(words, modifier["indices"]),
                }
            )
            combined_indices.extend(modifier["indices"])
        combined_indices.sort()
        subject_text = _group_text(words, combined_indices)
        subject_type = "composto" if len(subject_groups) > 1 else "simples"
        for item in subject_groups:
            _mark_group(words, item["indices"], "núcleo do sujeito")
    else:
        post_nominal = next(
            (item for item in after_groups if not item["prepositional"]),
            None,
        )
        if post_nominal and (
            voice == "voz passiva sintética"
            or frame.get("tipo", "").startswith("VI")
            or lemma in {"existir", "acontecer", "ocorrer", "nascer", "chegar"}
        ):
            subject_groups = [post_nominal]
            subject_text = _group_text(words, post_nominal["indices"])
            subject_type = (
                "simples paciente posposto"
                if voice == "voz passiva sintética"
                else "simples posposto"
            )
            _mark_group(words, post_nominal["indices"], "núcleo do sujeito")
        else:
            hint = _subject_hint(words[group.finite_index])
            subject_text = f"oculto ({hint})"
            subject_type = "oculto ou elíptico"

    excluded = {
        index for item in subject_groups for index in item["indices"]
    } | subject_connector_indices | subject_modifier_indices | {
        index for item in vocative_groups + appositive_groups for index in item["indices"]
    }
    complement_groups = [
        item
        for item in after_groups
        if not any(index in excluded for index in item["indices"])
    ]

    terms: list[dict] = structural_terms[:]
    complements: list[dict] = []
    has_predicative = False
    predicative_indices: set[int] = set()
    direct_used = False
    indirect_used = False
    is_linking = frame.get("tipo", "").startswith("VL") and not group.auxiliary_lemmas

    if is_linking:
        predicative = next(
            (
                item
                for item in complement_groups
                if not item["prepositional"]
                and any(
                    words[index].classe in {"adjetivo", "substantivo", "pronome", "numeral"}
                    for index in item["indices"]
                )
            ),
            None,
        )
        if predicative:
            has_predicative = True
            predicative_indices.update(predicative["indices"])
            _mark_group(
                words,
                predicative["indices"],
                "núcleo do predicativo do sujeito",
            )
            terms.append(
                {
                    "tipo": "predicativo do sujeito",
                    "texto": _group_text(words, predicative["indices"]),
                }
            )
    elif lemma in ACTION_WITH_SUBJECT_PREDICATIVE:
        predicative = next(
            (
                item
                for item in complement_groups
                if not item["prepositional"]
                and any(words[index].classe == "adjetivo" for index in item["indices"])
            ),
            None,
        )
        if predicative:
            has_predicative = True
            predicative_indices.update(predicative["indices"])
            _mark_group(
                words,
                predicative["indices"],
                "núcleo do predicativo do sujeito",
            )
            terms.append(
                {
                    "tipo": "predicativo do sujeito",
                    "texto": _group_text(words, predicative["indices"]),
                }
            )

    clitic_indices = [
        index
        for index in clause_indices
        if words[index].classe == "pronome"
        and "oblíquo" in words[index].subclasse
        and abs(index - group.finite_index) <= 2
    ]
    for clitic_index in clitic_indices:
        clitic = words[clitic_index]
        if clitic.normalized in {"o", "a", "os", "as"}:
            clitic.funcao = "objeto direto"
            terms.append({"tipo": "objeto direto pronominal", "texto": clitic.token})
            complements.append({"tipo": "objeto direto", "texto": clitic.token})
            direct_used = True
        elif clitic.normalized in {"lhe", "lhes"}:
            clitic.funcao = "objeto indireto"
            terms.append({"tipo": "objeto indireto pronominal", "texto": clitic.token})
            complements.append({"tipo": "objeto indireto", "texto": clitic.token})
            indirect_used = True
        elif clitic.normalized not in {"se"}:
            clitic.funcao = "objeto direto, indireto ou reflexivo (conforme a regência)"
            terms.append(
                {
                    "tipo": "complemento pronominal (verificar regência)",
                    "texto": clitic.token,
                }
            )

    object_predicative_candidates: set[int] = set()
    last_nonprepositional_nouns: set[str] = set()
    for item in complement_groups:
        indices = item["indices"][:]
        if lemma in OBJECT_PREDICATIVE_VERBS and not item["prepositional"]:
            trailing_adjectives = [
                index
                for index in indices
                if words[index].classe == "adjetivo"
                and any(
                    words[earlier].classe == "substantivo"
                    for earlier in indices
                    if earlier < index
                )
            ]
            if trailing_adjectives:
                object_predicative_candidates.update(trailing_adjectives)
                indices = [
                    index for index in indices if index not in object_predicative_candidates
                ]
        if any(index in predicative_indices for index in indices):
            continue
        text = _group_text(words, indices)
        if item["prepositional"]:
            prep = item["prep"]
            prep_base = {
                "ao": "a",
                "aos": "a",
                "do": "de",
                "da": "de",
                "dos": "de",
                "das": "de",
                "no": "em",
                "na": "em",
                "nos": "em",
                "nas": "em",
                "pelo": "por",
                "pela": "por",
            }.get(prep, prep)
            if voice == "voz passiva analítica" and prep_base in {"por", "de"}:
                term_type = "agente da passiva"
                words[indices[0]].funcao = "preposição introdutora do agente da passiva"
                _mark_group(words, indices, "núcleo do agente da passiva")
            elif prep_base in frame.get("preps", set()):
                term_type = "objeto indireto"
                indirect_used = True
                words[indices[0]].funcao = "preposição exigida pela regência verbal"
                _mark_group(words, indices, "núcleo do objeto indireto")
                complements.append({"tipo": term_type, "texto": text})
            elif (
                direct_used
                and prep_base == "de"
                and last_nonprepositional_nouns
            ):
                term_type = (
                    "complemento nominal"
                    if last_nonprepositional_nouns & ABSTRACT_NOUNS
                    else "adjunto adnominal preposicionado"
                )
                words[indices[0]].funcao = f"preposição introdutora do {term_type}"
                _mark_group(words, indices, f"núcleo do {term_type}")
            else:
                value = _preposition_value(prep, indices, words, lemma)
                term_type = f"adjunto adverbial de {value}"
                words[indices[0]].funcao = "preposição introdutora do adjunto adverbial"
                _mark_group(words, indices, f"núcleo do {term_type}")
            terms.append({"tipo": term_type, "texto": text})
            continue

        frame_type = frame.get("tipo", "")
        normalized_group = {words[index].normalized for index in indices}
        if normalized_group & TIME_NOUNS and direct_used:
            term_type = "adjunto adverbial de tempo"
            _mark_group(words, indices, "núcleo do adjunto adverbial de tempo")
        elif "VTD" in frame_type and not direct_used:
            term_type = "objeto direto"
            direct_used = True
            _mark_group(words, indices, "núcleo do objeto direto")
            complements.append({"tipo": term_type, "texto": text})
        elif frame_type.startswith("VI"):
            # Um nome depois de verbo intransitivo costuma ser sujeito posposto;
            # se já existe sujeito, mantemos a dúvida explícita.
            term_type = "termo nominal pós-verbal (verificar contexto)"
            _mark_group(words, indices, "função sintática dependente do contexto")
            warnings.append(
                f"Em “{text}”, o termo posterior ao verbo intransitivo “{lemma}” precisa de confirmação contextual."
            )
        elif frame_type.startswith("VL"):
            term_type = "predicativo do sujeito (hipótese)"
            _mark_group(words, indices, "núcleo do predicativo do sujeito")
            has_predicative = True
        elif not direct_used:
            term_type = "objeto direto (hipótese)"
            direct_used = True
            _mark_group(words, indices, "núcleo do objeto direto (hipótese)")
            complements.append({"tipo": term_type, "texto": text})
            if frame_type == "regência não cadastrada":
                warnings.append(
                    f"A regência de “{lemma}” não está cadastrada; “{text}” foi marcado como objeto direto por posição."
                )
        else:
            term_type = "termo nominal adicional"
            _mark_group(words, indices, "termo nominal adicional")
        terms.append({"tipo": term_type, "texto": text})
        last_nonprepositional_nouns = {
            words[index].normalized
            for index in indices
            if words[index].classe == "substantivo"
        }

    if (
        "subordinada adjetiva" in span.tipo
        and span.connector_index is not None
        and words[span.connector_index].classe == "pronome"
    ):
        relative = words[span.connector_index]
        frame_type = frame.get("tipo", "")
        if "VTD" in frame_type and not direct_used:
            relative.funcao = "objeto direto da oração adjetiva"
            terms.append(
                {
                    "tipo": "objeto direto representado pelo pronome relativo",
                    "texto": relative.token,
                }
            )
            direct_used = True
        elif frame_type.startswith("VI"):
            relative.funcao = "termo retomado pelo pronome relativo"

    if lemma in OBJECT_PREDICATIVE_VERBS and direct_used:
        adjective_after = next(iter(sorted(object_predicative_candidates)), None)
        if adjective_after is None:
            adjective_after = next(
                (
                    index
                    for index in after
                    if words[index].classe == "adjetivo"
                    and "objeto" not in words[index].funcao
                ),
                None,
            )
        if adjective_after is not None:
            words[adjective_after].funcao = "predicativo do objeto"
            terms.append(
                {
                    "tipo": "predicativo do objeto",
                    "texto": words[adjective_after].token,
                }
            )
            has_predicative = True

    # Advérbios e locuções circunstanciais simples.
    for index in clause_indices:
        if words[index].classe == "advérbio":
            subtype = words[index].subclasse.split(" ")[0]
            function = f"adjunto adverbial de {subtype}"
            words[index].funcao = function
            terms.append({"tipo": function, "texto": words[index].token})

    if impersonal:
        terms.insert(
            0,
            {
                "tipo": "oração sem sujeito",
                "texto": impersonal_reason,
            },
        )
    elif subject_text:
        terms.insert(
            0,
            {
                "tipo": f"sujeito {subject_type}",
                "texto": subject_text,
            },
        )

    predicate_type = (
        "verbo-nominal (hipótese)"
        if has_predicative and not is_linking
        else ("nominal" if has_predicative else "verbal")
    )
    predicate_indices = [
        index
        for index in clause_indices
        if index not in excluded
        and index != span.connector_index
        and words[index].funcao != "núcleo do sujeito"
    ]
    predicate_text = _group_text(words, predicate_indices)
    terms.insert(
        1 if terms else 0,
        {"tipo": f"predicado {predicate_type}", "texto": predicate_text},
    )

    if frame.get("tipo") == "regência não cadastrada":
        regency = "regência não cadastrada; complementos marcados por hipótese contextual"
    else:
        preps = ", ".join(sorted(frame.get("preps", set())))
        regency = frame["tipo"] + (f"; preposição esperada: {preps}" if preps else "")

    return {
        "texto": _group_text(words, span.indices),
        "tipo": span.tipo,
        "conector": (
            words[span.connector_index].token
            if span.connector_index is not None
            else ""
        ),
        "sujeito": subject_text,
        "tipo_sujeito": subject_type,
        "predicado": predicate_text,
        "tipo_predicado": predicate_type,
        "verbo_principal": words[group.head_index].token,
        "locucao_verbal": (
            _group_text(words, group.indices) if len(group.indices) > 1 else ""
        ),
        "lema": lemma,
        "regencia": regency,
        "voz_verbal": voice,
        "complementos": complements,
        "termos": terms,
    }


def _syntactic_analysis_v2(words: list[WordAnalysis]) -> dict:
    warnings: list[str] = []
    for word in words:
        if word.classe == "pontuação":
            word.funcao = "sinal de pontuação"
        elif word.classe == "interjeição":
            word.funcao = "enunciado interjetivo"

    groups = _build_verb_groups(words)
    if not groups:
        text = _join_tokens(word.token for word in words)
        return {
            "sujeito": "não se aplica sem oração reconhecida",
            "tipo_sujeito": "não identificado",
            "predicado": "não identificado",
            "tipo_predicado": "não identificado",
            "verbo_principal": "não identificado",
            "complementos": [],
            "oracoes": 0,
            "oracoes_detalhadas": [],
            "regencia": "não se aplica",
            "voz_verbal": "não se aplica",
            "termos": [{"tipo": "frase nominal", "texto": text}],
            "avisos": [
                "Não foi identificado verbo; há uma frase nominal ou uma forma verbal ainda não reconhecida."
            ],
        }

    spans = _build_clause_spans(words, groups)
    _classify_clauses(words, spans)
    clauses = [_analyze_clause(words, span, warnings) for span in spans]

    if len(clauses) > 1:
        warnings.append(
            f"Foram reconhecidas {len(clauses)} orações. Observe os conectores e confira relações que dependam do sentido completo."
        )

    # Orações substantivas e adjetivas exercem função na oração principal.
    relation_terms: list[dict] = []
    subordinate_complements: list[dict] = []
    for clause in clauses:
        if "subordinada substantiva objetiva direta" in clause["tipo"]:
            item = {
                "tipo": "oração com função de objeto direto",
                "texto": clause["texto"],
            }
            relation_terms.append(item)
            subordinate_complements.append(
                {"tipo": "objeto direto oracional", "texto": clause["texto"]}
            )
        elif "subordinada adjetiva" in clause["tipo"]:
            relation_terms.append(
                {
                    "tipo": "oração com função de adjunto adnominal",
                    "texto": clause["texto"],
                }
            )

    primary = next(
        (
            clause
            for clause in clauses
            if "principal" in clause["tipo"] or "absoluta" in clause["tipo"]
        ),
        clauses[0],
    )
    primary_predicate = primary["predicado"]
    for complement in subordinate_complements:
        if complement["texto"] not in primary_predicate:
            primary_predicate = f"{primary_predicate} {complement['texto']}".strip()
    all_terms = [
        {**term, "oração": position + 1}
        for position, clause in enumerate(clauses)
        for term in clause["termos"]
    ] + relation_terms

    return {
        "sujeito": primary["sujeito"],
        "tipo_sujeito": primary["tipo_sujeito"],
        "predicado": primary_predicate,
        "tipo_predicado": primary["tipo_predicado"],
        "verbo_principal": primary["verbo_principal"],
        "locucao_verbal": primary["locucao_verbal"],
        "complementos": primary["complementos"] + subordinate_complements,
        "oracoes": len(clauses),
        "oracoes_detalhadas": clauses,
        "regencia": primary["regencia"],
        "voz_verbal": primary["voz_verbal"],
        "termos": all_terms,
        "avisos": list(dict.fromkeys(warnings)),
    }


def analyze_sentence(sentence: str) -> dict:
    sentence = re.sub(r"\s+", " ", sentence.strip())
    if not sentence:
        raise ValueError("Digite uma frase para analisar.")
    if len(sentence) > 500:
        raise ValueError("Use uma frase de até 500 caracteres por análise.")

    tokens = _tokenize_sentence(sentence)
    if not tokens:
        raise ValueError("Não foi possível identificar palavras nessa entrada.")

    words: list[WordAnalysis] = []
    for index, token in enumerate(tokens):
        words.append(_classify_word(token, index, tokens, words))

    _refine_morphology(words, sentence)
    syntax = _syntactic_analysis_v2(words)
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
                "Motor contextual 2.0: regras morfológicas, locuções, regência e divisão "
                "de orações. Confira especialmente palavras ambíguas e usos figurados."
            ),
            "versao_motor": ENGINE_VERSION,
        },
        "legenda": CLASS_DESCRIPTIONS,
    }


if __name__ == "__main__":
    import json
    import sys

    sample = " ".join(sys.argv[1:]) or "O menino comprou um livro ontem."
    print(json.dumps(analyze_sentence(sample), ensure_ascii=False, indent=2))
