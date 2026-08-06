"""Conteúdo autoral e progressivo do curso Gramática em Análise."""

LESSONS = [
    {
        "id": "fundamentos",
        "module": "Fundamentos",
        "order": 1,
        "title": "Gramática, morfologia e sintaxe",
        "description": "Entenda o que cada tipo de análise observa.",
        "objectives": [
            "Distinguir morfologia, sintaxe e morfossintaxe.",
            "Entender por que a mesma palavra pode mudar de classe conforme o contexto.",
        ],
        "sections": [
            {
                "title": "Três pontos de observação",
                "text": "A morfologia estuda a palavra: sua estrutura, suas flexões e sua classe. A sintaxe estuda a função e as relações que as palavras mantêm dentro da oração. A morfossintaxe observa as duas coisas ao mesmo tempo.",
            },
            {
                "title": "Classe não é função",
                "text": "Em “O aluno leu o livro”, aluno e livro são substantivos. Entretanto, aluno é núcleo do sujeito e livro é núcleo do objeto direto. A classe permanece; a função é determinada pela construção.",
            },
        ],
        "examples": [
            {"sentence": "O aluno leu o livro.", "focus": "aluno", "answer": "substantivo; núcleo do sujeito"},
            {"sentence": "O aluno leu o livro.", "focus": "livro", "answer": "substantivo; núcleo do objeto direto"},
        ],
        "tip": "Pergunte primeiro “o que esta palavra é?” e depois “o que ela faz nesta oração?”.",
        "quiz": {
            "question": "Qual área estuda a função de uma palavra dentro da oração?",
            "options": ["Sintaxe", "Morfologia", "Fonética", "Ortografia"],
            "answer": 0,
            "explanation": "A sintaxe examina funções e relações entre os termos.",
        },
    },
    {
        "id": "substantivo",
        "module": "Classes gramaticais",
        "order": 2,
        "title": "Substantivo",
        "description": "A classe que nomeia seres, ideias, ações e sentimentos.",
        "objectives": ["Reconhecer substantivos no contexto.", "Distinguir classificações e flexões básicas."],
        "sections": [
            {
                "title": "O núcleo dos nomes",
                "text": "Substantivo é a palavra usada para nomear seres, lugares, sentimentos, ações, estados e conceitos. Pode ser comum ou próprio, concreto ou abstrato, simples ou composto, primitivo ou derivado.",
            },
            {
                "title": "Flexões",
                "text": "Muitos substantivos variam em gênero, número e grau. Essas marcas precisam ser observadas junto dos determinantes que os acompanham.",
            },
            {
                "title": "Substantivação",
                "text": "Uma palavra de outra classe pode funcionar como substantivo. Em “O belo emociona”, o artigo transforma o adjetivo belo em um elemento substantivado.",
            },
        ],
        "examples": [
            {"sentence": "A coragem transforma pessoas.", "focus": "coragem", "answer": "substantivo abstrato"},
            {"sentence": "Pouso Alegre cresceu.", "focus": "Pouso Alegre", "answer": "substantivo próprio"},
        ],
        "tip": "Artigos, pronomes, numerais e adjetivos costumam gravitar em torno do substantivo.",
        "quiz": {
            "question": "Em “O impossível aconteceu”, o termo “impossível” está:",
            "options": ["Substantivado", "Funcionando como verbo", "Funcionando como advérbio", "Sem classe"],
            "answer": 0,
            "explanation": "O artigo “o” permite que o adjetivo seja usado como substantivo.",
        },
    },
    {
        "id": "adjetivo",
        "module": "Classes gramaticais",
        "order": 3,
        "title": "Adjetivo",
        "description": "O modificador que caracteriza ou delimita um nome.",
        "objectives": ["Localizar o nome modificado.", "Perceber mudanças de sentido causadas pela posição."],
        "sections": [
            {
                "title": "Caracterização",
                "text": "Adjetivo atribui característica, estado, qualidade, origem ou relação a um substantivo ou equivalente. Em regra, concorda com o nome em gênero e número.",
            },
            {
                "title": "Posição e sentido",
                "text": "A posição pode mudar o sentido: “grande homem” destaca valor ou importância; “homem grande” tende a indicar tamanho.",
            },
            {
                "title": "Locução adjetiva",
                "text": "Uma expressão iniciada por preposição pode ter valor de adjetivo, como “amor de mãe” e “energia do sol”.",
            },
        ],
        "examples": [
            {"sentence": "A resposta correta apareceu.", "focus": "correta", "answer": "adjetivo de resposta"},
            {"sentence": "Compramos energia solar.", "focus": "solar", "answer": "adjetivo relacional"},
        ],
        "tip": "Para confirmar um adjetivo, identifique qual nome ele modifica.",
        "quiz": {
            "question": "Qual palavra caracteriza o substantivo em “A rua silenciosa parecia longa”?",
            "options": ["silenciosa", "rua", "parecia", "a"],
            "answer": 0,
            "explanation": "“Silenciosa” atribui uma característica à rua.",
        },
    },
    {
        "id": "artigo",
        "module": "Classes gramaticais",
        "order": 4,
        "title": "Artigo",
        "description": "O determinante que define ou generaliza o substantivo.",
        "objectives": ["Distinguir artigos definidos e indefinidos.", "Perceber efeitos de sentido da determinação."],
        "sections": [
            {
                "title": "Definir ou apresentar",
                "text": "O, a, os e as são definidos: indicam um referente apresentado como conhecido. Um, uma, uns e umas são indefinidos: introduzem ou apresentam o referente sem determinação precisa.",
            },
            {
                "title": "Efeito no texto",
                "text": "Compare “Um homem entrou” com “O homem entrou”. Na segunda frase, o leitor pressupõe que aquele homem já é identificável no contexto.",
            },
        ],
        "examples": [
            {"sentence": "Uma criança chamou. A criança esperou.", "focus": "Uma / A", "answer": "apresentação e retomada"},
        ],
        "tip": "“Um” também pode ser numeral. O contexto mostra se a intenção é indefinir ou contar.",
        "quiz": {
            "question": "Em “Preciso de um caderno qualquer”, “um” tende a ser:",
            "options": ["Artigo indefinido", "Verbo", "Preposição", "Interjeição"],
            "answer": 0,
            "explanation": "O termo introduz caderno sem identificar qual.",
        },
    },
    {
        "id": "numeral",
        "module": "Classes gramaticais",
        "order": 5,
        "title": "Numeral",
        "description": "Quantidade, ordem, multiplicação e fração.",
        "objectives": ["Reconhecer os principais tipos de numeral.", "Separar numeral de usos imprecisos ou substantivos."],
        "sections": [
            {
                "title": "Tipos",
                "text": "Cardinais indicam quantidade; ordinais, posição; multiplicativos, multiplicação; fracionários, divisão. Numerais podem acompanhar ou substituir substantivos.",
            },
            {
                "title": "Contexto",
                "text": "Em “Comprei um livro”, um pode apenas apresentar um exemplar. Em “Comprei somente um livro”, a ideia de quantidade fica destacada.",
            },
        ],
        "examples": [
            {"sentence": "Dois alunos chegaram em primeiro lugar.", "focus": "Dois / primeiro", "answer": "cardinal / ordinal"},
        ],
        "tip": "Procure uma informação numérica exata ou uma posição em série.",
        "quiz": {
            "question": "“Dobro” pertence a qual tipo de numeral?",
            "options": ["Multiplicativo", "Ordinal", "Cardinal", "Coletivo"],
            "answer": 0,
            "explanation": "Dobro indica multiplicação por dois.",
        },
    },
    {
        "id": "pronome",
        "module": "Classes gramaticais",
        "order": 6,
        "title": "Pronome",
        "description": "A classe que aponta, retoma, substitui ou acompanha nomes.",
        "objectives": ["Conhecer os principais tipos de pronome.", "Distinguir pronome substantivo e adjetivo."],
        "sections": [
            {
                "title": "Referência",
                "text": "Pronomes relacionam os seres às pessoas do discurso ou retomam informações. Podem ser pessoais, possessivos, demonstrativos, indefinidos, relativos, interrogativos e de tratamento.",
            },
            {
                "title": "Substituir ou acompanhar",
                "text": "Em “Meu livro sumiu”, meu acompanha o substantivo e tem valor adjetivo. Em “O meu sumiu”, meu substitui o substantivo e tem valor substantivo.",
            },
        ],
        "examples": [
            {"sentence": "Ela trouxe seu material.", "focus": "Ela / seu", "answer": "pessoal / possessivo"},
            {"sentence": "O livro que comprei chegou.", "focus": "que", "answer": "pronome relativo"},
        ],
        "tip": "Descubra qual termo o pronome representa ou acompanha.",
        "quiz": {
            "question": "Em “Aquela é a minha casa”, “aquela” é pronome:",
            "options": ["Demonstrativo", "Possessivo", "Relativo", "Pessoal"],
            "answer": 0,
            "explanation": "O pronome aponta um referente em relação ao espaço ou ao discurso.",
        },
    },
    {
        "id": "verbo",
        "module": "Classes gramaticais",
        "order": 7,
        "title": "Verbo",
        "description": "A classe que estrutura a oração e varia em pessoa, número, tempo e modo.",
        "objectives": ["Reconhecer formas verbais.", "Identificar locuções e formas nominais."],
        "sections": [
            {
                "title": "O centro da oração",
                "text": "Verbos exprimem ação, estado, mudança de estado ou fenômeno, situando o processo no tempo. Uma forma verbal finita normalmente organiza uma oração.",
            },
            {
                "title": "Flexões",
                "text": "O verbo pode variar em pessoa, número, tempo, modo e voz. Infinitivo, gerúndio e particípio são chamados formas nominais.",
            },
            {
                "title": "Locução verbal",
                "text": "Dois ou mais verbos podem formar uma unidade: “vai estudar”, “tinha chegado”, “pode acontecer”. Um auxilia e o outro carrega o sentido principal.",
            },
        ],
        "examples": [
            {"sentence": "Os alunos estudaram ontem.", "focus": "estudaram", "answer": "verbo estudar; passado"},
            {"sentence": "Ela está aprendendo.", "focus": "está aprendendo", "answer": "locução verbal"},
        ],
        "tip": "Contar verbos ajuda a estimar orações, mas uma locução pode conter dois verbos e formar apenas uma oração.",
        "quiz": {
            "question": "Qual é a forma nominal em “Eles continuam estudando”?",
            "options": ["estudando", "continuam", "eles", "nenhuma"],
            "answer": 0,
            "explanation": "A terminação -ndo marca o gerúndio.",
        },
    },
    {
        "id": "adverbio",
        "module": "Classes gramaticais",
        "order": 8,
        "title": "Advérbio",
        "description": "Circunstâncias de tempo, lugar, modo, intensidade e outras.",
        "objectives": ["Reconhecer o termo modificado.", "Classificar circunstâncias comuns."],
        "sections": [
            {
                "title": "Modificação",
                "text": "O advérbio pode modificar verbo, adjetivo, outro advérbio ou a oração inteira. Em geral, é invariável.",
            },
            {
                "title": "Circunstâncias",
                "text": "Tempo, lugar, modo, intensidade, afirmação, negação e dúvida são valores frequentes. O sentido nasce do contexto, não apenas de uma lista.",
            },
        ],
        "examples": [
            {"sentence": "Talvez ele chegue cedo.", "focus": "Talvez / cedo", "answer": "dúvida / tempo"},
            {"sentence": "Ela fala muito bem.", "focus": "muito / bem", "answer": "intensidade / modo"},
        ],
        "tip": "Pergunte que circunstância a palavra acrescenta e qual elemento ela modifica.",
        "quiz": {
            "question": "Em “A resposta ficou muito clara”, “muito” modifica:",
            "options": ["O adjetivo clara", "O substantivo resposta", "O artigo a", "Nada"],
            "answer": 0,
            "explanation": "O advérbio intensifica o adjetivo “clara”.",
        },
    },
    {
        "id": "preposicao",
        "module": "Classes gramaticais",
        "order": 9,
        "title": "Preposição",
        "description": "A ligação entre termos e as relações de sentido.",
        "objectives": ["Reconhecer preposições e contrações.", "Relacionar preposição e regência."],
        "sections": [
            {
                "title": "Relação",
                "text": "Preposições ligam termos, fazendo o segundo depender do primeiro. Podem indicar origem, destino, causa, posse, meio, assunto e muitas outras relações.",
            },
            {
                "title": "Contrações",
                "text": "Preposição e artigo ou pronome podem se unir: de + o = do; em + a = na; a + a = à. Reconhecer a formação ajuda na análise.",
            },
        ],
        "examples": [
            {"sentence": "O caderno de Maria está na mesa.", "focus": "de / na", "answer": "posse / em + a"},
        ],
        "tip": "Observe quais dois termos a preposição está relacionando.",
        "quiz": {
            "question": "A palavra “pelo” resulta normalmente da união de:",
            "options": ["por + o", "para + o", "perante + o", "por + ele"],
            "answer": 0,
            "explanation": "“Pelo” é contração de por com o.",
        },
    },
    {
        "id": "conjuncao",
        "module": "Classes gramaticais",
        "order": 10,
        "title": "Conjunção",
        "description": "Conectores que coordenam termos ou subordinam orações.",
        "objectives": ["Distinguir coordenação e subordinação.", "Interpretar o sentido do conector."],
        "sections": [
            {
                "title": "Coordenação",
                "text": "Conjunções coordenativas ligam termos ou orações de função equivalente. Podem acrescentar, opor, alternar, concluir ou explicar.",
            },
            {
                "title": "Subordinação",
                "text": "Conjunções subordinativas introduzem uma oração dependente e indicam relações como causa, condição, tempo, concessão e finalidade.",
            },
        ],
        "examples": [
            {"sentence": "Estudei, mas ainda tenho dúvidas.", "focus": "mas", "answer": "adversativa"},
            {"sentence": "Irei se você chamar.", "focus": "se", "answer": "condicional"},
        ],
        "tip": "Substitua o conector por outro de sentido próximo para testar a relação.",
        "quiz": {
            "question": "Em “Embora estivesse cansado, continuou”, há ideia de:",
            "options": ["Concessão", "Adição", "Conclusão", "Alternância"],
            "answer": 0,
            "explanation": "“Embora” apresenta um fato que não impede o resultado.",
        },
    },
    {
        "id": "interjeicao",
        "module": "Classes gramaticais",
        "order": 11,
        "title": "Interjeição",
        "description": "Reações, emoções, chamamentos e estados de espírito.",
        "objectives": ["Reconhecer enunciados interjetivos.", "Interpretar a emoção no contexto."],
        "sections": [
            {
                "title": "Expressividade",
                "text": "Interjeições funcionam como enunciados condensados. O mesmo termo pode exprimir sentimentos diferentes conforme entonação e situação.",
            },
            {
                "title": "Locuções interjetivas",
                "text": "Expressões com mais de uma palavra também podem ter valor interjetivo: “Meu Deus!”, “Ora bolas!”, “Quem me dera!”.",
            },
        ],
        "examples": [
            {"sentence": "Ufa! Terminamos.", "focus": "Ufa", "answer": "interjeição de alívio"},
            {"sentence": "Ó aluno, preste atenção.", "focus": "Ó", "answer": "interjeição de chamamento"},
        ],
        "tip": "Não confunda “ó”, chamamento, com “oh”, normalmente ligado à emoção.",
        "quiz": {
            "question": "Em “Socorro!”, a palavra constitui:",
            "options": ["Interjeição", "Artigo", "Conjunção", "Advérbio"],
            "answer": 0,
            "explanation": "Sozinha, expressa um pedido completo de ajuda.",
        },
    },
    {
        "id": "frase-oracao-periodo",
        "module": "Sintaxe",
        "order": 12,
        "title": "Frase, oração e período",
        "description": "As unidades que organizam os enunciados.",
        "objectives": ["Separar frase, oração e período.", "Contar orações com atenção às locuções verbais."],
        "sections": [
            {
                "title": "Unidades",
                "text": "Frase é um enunciado com sentido no contexto e pode não ter verbo. Oração organiza-se em torno de verbo ou locução verbal. Período é a frase formada por uma ou mais orações e encerrada por pontuação conclusiva.",
            },
            {
                "title": "Simples e composto",
                "text": "Período simples tem uma oração. Período composto possui duas ou mais. A contagem exige reconhecer locuções verbais.",
            },
        ],
        "examples": [
            {"sentence": "Silêncio!", "focus": "enunciado", "answer": "frase nominal"},
            {"sentence": "Ela vai estudar.", "focus": "vai estudar", "answer": "uma locução; uma oração"},
        ],
        "tip": "Nem toda frase tem oração, mas toda oração pode fazer parte de uma frase.",
        "quiz": {
            "question": "“Que dia bonito!” contém quantas orações?",
            "options": ["Nenhuma", "Uma", "Duas", "Três"],
            "answer": 0,
            "explanation": "É uma frase nominal, pois não há verbo.",
        },
    },
    {
        "id": "sujeito",
        "module": "Sintaxe",
        "order": 13,
        "title": "Sujeito",
        "description": "O termo com o qual o verbo normalmente estabelece concordância.",
        "objectives": ["Localizar o núcleo do sujeito.", "Distinguir tipos básicos de sujeito."],
        "sections": [
            {
                "title": "Como encontrar",
                "text": "Localize o verbo, observe sua concordância e pergunte qual termo substantivo está relacionado a ele. O sujeito pode aparecer antes ou depois do verbo.",
            },
            {
                "title": "Tipos",
                "text": "O sujeito pode ser simples, composto, oculto ou indeterminado. Há ainda orações sem sujeito, especialmente com verbos impessoais.",
            },
        ],
        "examples": [
            {"sentence": "Chegaram os convidados.", "focus": "os convidados", "answer": "sujeito simples posposto"},
            {"sentence": "Estudamos muito.", "focus": "nós", "answer": "sujeito oculto"},
        ],
        "tip": "A posição não define o sujeito; a relação com o verbo é mais importante.",
        "quiz": {
            "question": "Em “Pedro e Ana chegaram”, o sujeito é:",
            "options": ["Composto", "Simples", "Oculto", "Inexistente"],
            "answer": 0,
            "explanation": "Há dois núcleos: Pedro e Ana.",
        },
    },
    {
        "id": "predicado",
        "module": "Sintaxe",
        "order": 14,
        "title": "Predicado e predicativos",
        "description": "O que se declara sobre o sujeito e os núcleos dessa declaração.",
        "objectives": ["Distinguir predicado verbal, nominal e verbo-nominal.", "Reconhecer predicativos."],
        "sections": [
            {
                "title": "Três tipos",
                "text": "Predicado verbal tem verbo significativo como núcleo. Predicado nominal apresenta nome predicativo ligado ao sujeito. O verbo-nominal reúne ação e característica.",
            },
            {
                "title": "Verbo de ligação",
                "text": "Ser, estar, ficar e parecer podem ligar uma característica ao sujeito. O contexto decide: em “Ele ficou em casa”, ficou pode indicar permanência em lugar, não simples ligação.",
            },
        ],
        "examples": [
            {"sentence": "O aluno estava atento.", "focus": "atento", "answer": "predicativo do sujeito"},
            {"sentence": "O aluno chegou atento.", "focus": "chegou atento", "answer": "predicado verbo-nominal"},
        ],
        "tip": "Não classifique um verbo isoladamente; examine o sentido que ele assume naquela oração.",
        "quiz": {
            "question": "Em “A sala permanece vazia”, o predicado é:",
            "options": ["Nominal", "Verbal", "Sem núcleo", "Aposto"],
            "answer": 0,
            "explanation": "“Vazia” é o núcleo nominal ligado ao sujeito.",
        },
    },
    {
        "id": "complementos",
        "module": "Sintaxe",
        "order": 15,
        "title": "Complementos verbais e nominais",
        "description": "Objeto direto, objeto indireto e complemento nominal.",
        "objectives": ["Reconhecer a necessidade de complemento.", "Distinguir termo verbal de termo nominal."],
        "sections": [
            {
                "title": "Objetos",
                "text": "Objeto direto completa verbo normalmente sem preposição obrigatória. Objeto indireto completa verbo por meio de preposição exigida. A regência do verbo precisa ser considerada.",
            },
            {
                "title": "Complemento nominal",
                "text": "Completa o sentido de substantivo abstrato, adjetivo ou advérbio, sempre com preposição. Em “necessidade de apoio”, de apoio completa o nome necessidade.",
            },
        ],
        "examples": [
            {"sentence": "Ela comprou um livro.", "focus": "um livro", "answer": "objeto direto"},
            {"sentence": "Ela precisa de apoio.", "focus": "de apoio", "answer": "objeto indireto"},
        ],
        "tip": "Primeiro descubra se o complemento se liga a um verbo ou a um nome.",
        "quiz": {
            "question": "Em “Confio em você”, “em você” é:",
            "options": ["Objeto indireto", "Objeto direto", "Sujeito", "Vocativo"],
            "answer": 0,
            "explanation": "O verbo confiar exige a preposição em.",
        },
    },
    {
        "id": "adjuntos",
        "module": "Sintaxe",
        "order": 16,
        "title": "Adjunto adnominal e adverbial",
        "description": "Termos que delimitam nomes ou acrescentam circunstâncias.",
        "objectives": ["Distinguir modificador nominal e circunstancial.", "Reconhecer valores adverbiais."],
        "sections": [
            {
                "title": "Adjunto adnominal",
                "text": "Acompanha um substantivo para determiná-lo ou caracterizá-lo. Artigos, adjetivos, pronomes e numerais podem exercer essa função.",
            },
            {
                "title": "Adjunto adverbial",
                "text": "Acrescenta circunstância ao verbo, ao adjetivo, ao advérbio ou à oração: tempo, lugar, modo, causa, finalidade e muitas outras.",
            },
        ],
        "examples": [
            {"sentence": "Os dois alunos atentos responderam rapidamente.", "focus": "Os dois atentos", "answer": "adjuntos adnominais"},
            {"sentence": "Chegamos ontem.", "focus": "ontem", "answer": "adjunto adverbial de tempo"},
        ],
        "tip": "Veja se o termo se prende a um substantivo ou acrescenta circunstância ao enunciado.",
        "quiz": {
            "question": "Em “Minha casa antiga foi vendida”, “minha” é:",
            "options": ["Adjunto adnominal", "Objeto direto", "Predicativo", "Advérbio"],
            "answer": 0,
            "explanation": "O pronome possessivo determina o substantivo casa.",
        },
    },
    {
        "id": "aposto-vocativo",
        "module": "Sintaxe",
        "order": 17,
        "title": "Aposto, vocativo e agente da passiva",
        "description": "Esclarecimento, chamamento e autoria da ação na voz passiva.",
        "objectives": ["Separar aposto de vocativo.", "Reconhecer o agente da passiva."],
        "sections": [
            {
                "title": "Aposto e vocativo",
                "text": "Aposto explica, resume, enumera ou especifica outro termo. Vocativo chama o interlocutor e não integra sujeito nem predicado.",
            },
            {
                "title": "Agente da passiva",
                "text": "Na voz passiva analítica, indica quem pratica a ação sofrida pelo sujeito, geralmente introduzido por por ou de.",
            },
        ],
        "examples": [
            {"sentence": "Carlos, meu vizinho, viajou.", "focus": "meu vizinho", "answer": "aposto explicativo"},
            {"sentence": "Carlos, venha aqui.", "focus": "Carlos", "answer": "vocativo"},
        ],
        "tip": "O vocativo conversa com alguém; o aposto fala sobre algum termo.",
        "quiz": {
            "question": "Em “O relatório foi escrito pela equipe”, “pela equipe” é:",
            "options": ["Agente da passiva", "Objeto direto", "Sujeito", "Vocativo"],
            "answer": 0,
            "explanation": "A equipe pratica a ação na construção passiva.",
        },
    },
    {
        "id": "coordenacao",
        "module": "Período composto",
        "order": 18,
        "title": "Orações coordenadas",
        "description": "Orações independentes sintaticamente colocadas lado a lado.",
        "objectives": ["Reconhecer coordenação com e sem conjunção.", "Classificar relações coordenativas."],
        "sections": [
            {
                "title": "Assindética e sindética",
                "text": "A coordenada assindética não é introduzida por conjunção. A sindética apresenta conector e pode ser aditiva, adversativa, alternativa, conclusiva ou explicativa.",
            },
            {
                "title": "Paralelismo",
                "text": "Elementos coordenados devem manter estrutura compatível. O paralelismo torna o texto mais claro e equilibrado.",
            },
        ],
        "examples": [
            {"sentence": "Cheguei, vi, venci.", "focus": "orações", "answer": "coordenadas assindéticas"},
            {"sentence": "Estudei, portanto estou preparado.", "focus": "portanto", "answer": "coordenada conclusiva"},
        ],
        "tip": "Coordenação é relação de equivalência sintática, não simples ausência de sentido entre as partes.",
        "quiz": {
            "question": "“Queria sair, mas estava chovendo” apresenta relação:",
            "options": ["Adversativa", "Aditiva", "Alternativa", "Explicativa"],
            "answer": 0,
            "explanation": "A segunda oração cria contraste com a primeira.",
        },
    },
    {
        "id": "subordinacao",
        "module": "Período composto",
        "order": 19,
        "title": "Orações subordinadas",
        "description": "Orações que exercem função dentro de outra estrutura.",
        "objectives": ["Reconhecer dependência sintática.", "Distinguir subordinadas substantivas, adjetivas e adverbiais."],
        "sections": [
            {
                "title": "Três grandes grupos",
                "text": "Subordinadas substantivas exercem funções típicas de substantivo; adjetivas caracterizam um nome; adverbiais acrescentam circunstância à oração principal.",
            },
            {
                "title": "Teste de substituição",
                "text": "Uma subordinada substantiva muitas vezes pode ser substituída por “isso”. Nas adjetivas, procure um nome antecedente. Nas adverbiais, identifique a circunstância.",
            },
        ],
        "examples": [
            {"sentence": "Espero que você venha.", "focus": "que você venha", "answer": "subordinada substantiva objetiva direta"},
            {"sentence": "O livro que comprei chegou.", "focus": "que comprei", "answer": "subordinada adjetiva restritiva"},
        ],
        "tip": "Descubra qual função a oração inteira realiza em relação à principal.",
        "quiz": {
            "question": "Em “Saí quando a chuva parou”, a oração iniciada por “quando” é:",
            "options": ["Adverbial temporal", "Substantiva subjetiva", "Adjetiva", "Coordenada adversativa"],
            "answer": 0,
            "explanation": "Ela indica o momento em que ocorreu a saída.",
        },
    },
    {
        "id": "morfossintaxe",
        "module": "Integração",
        "order": 20,
        "title": "Análise morfossintática completa",
        "description": "Junte classe, flexão, função e relação entre orações.",
        "objectives": ["Aplicar uma sequência segura de análise.", "Justificar classificações com evidências do contexto."],
        "sections": [
            {
                "title": "Sequência recomendada",
                "text": "Leia o sentido geral; marque verbos e conectores; delimite orações; encontre sujeito e predicado; reconheça complementos; por fim, classifique cada palavra e relacione classe e função.",
            },
            {
                "title": "Ambiguidade faz parte",
                "text": "Uma análise séria admite alternativas. Em “Eu canto”, canto é verbo; em “O canto ecoou”, é substantivo. O contexto decide e a justificativa vale mais do que a etiqueta isolada.",
            },
        ],
        "examples": [
            {"sentence": "Os alunos atentos resolveram a atividade rapidamente.", "focus": "análise", "answer": "sujeito simples + predicado verbal + objeto direto + adjunto adverbial"},
        ],
        "tip": "Sempre registre a evidência que levou à classificação.",
        "quiz": {
            "question": "Na análise completa, qual deve ser uma das primeiras marcações?",
            "options": ["Verbos e conectores", "Somente artigos", "Somente adjetivos", "Apenas a pontuação final"],
            "answer": 0,
            "explanation": "Verbos e conectores ajudam a delimitar as estruturas maiores.",
        },
    },
]

LESSONS.extend(
    [
        {
            "id": "formacao-palavras",
            "module": "Estrutura e escrita",
            "order": 21,
            "title": "Estrutura e formação das palavras",
            "description": "Radical, afixos, desinências, composição e derivação.",
            "objectives": [
                "Reconhecer as partes que formam uma palavra.",
                "Distinguir derivação de composição.",
                "Relacionar a formação ao significado.",
            ],
            "sections": [
                {
                    "title": "Partes da palavra",
                    "text": (
                        "O radical concentra a base de significado compartilhada por palavras "
                        "da mesma família: feliz, felicidade e infelizmente. Prefixos aparecem "
                        "antes do radical; sufixos aparecem depois. Desinências indicam flexões "
                        "como gênero, número, pessoa, tempo e modo. A vogal temática liga o radical "
                        "às desinências verbais ou nominais."
                    ),
                },
                {
                    "title": "Derivação",
                    "text": (
                        "Na derivação, uma palavra nova nasce de outra já existente. Pode ocorrer "
                        "por prefixação, sufixação, uso simultâneo de prefixo e sufixo, mudança de "
                        "classe sem alteração formal ou redução. Em infeliz há prefixação; em "
                        "felicidade há sufixação; em anoitecer ocorre derivação parassintética."
                    ),
                },
                {
                    "title": "Composição",
                    "text": (
                        "Na composição, dois ou mais radicais formam uma unidade. Na justaposição, "
                        "as bases permanecem reconhecíveis, como guarda-chuva. Na aglutinação, há "
                        "alteração sonora ou gráfica, como planalto, formado historicamente por "
                        "plano e alto. O contexto confirma se o conjunto funciona como uma palavra."
                    ),
                },
            ],
            "examples": [
                {
                    "sentence": "Infelizmente, a atividade terminou.",
                    "focus": "infeliz + mente",
                    "answer": "Prefixação e sufixação em etapas.",
                },
                {
                    "sentence": "O guarda-chuva ficou no carro.",
                    "focus": "guarda-chuva",
                    "answer": "Composição por justaposição.",
                },
            ],
            "tip": "Procure primeiro o radical e depois observe o que foi acrescentado antes ou depois dele.",
            "quiz": {
                "question": "Qual palavra apresenta composição por justaposição?",
                "options": ["Guarda-roupa", "Infeliz", "Felizmente", "Refazer"],
                "answer": 0,
                "explanation": "Guarda-roupa reúne dois radicais que permanecem reconhecíveis.",
            },
        },
        {
            "id": "ortografia-acentuacao",
            "module": "Estrutura e escrita",
            "order": 22,
            "title": "Ortografia e acentuação",
            "description": "Sílaba tônica, regras de acento e dúvidas ortográficas frequentes.",
            "objectives": [
                "Identificar oxítonas, paroxítonas e proparoxítonas.",
                "Aplicar regras gerais de acentuação.",
                "Usar a grafia correta em pares frequentes.",
            ],
            "sections": [
                {
                    "title": "Posição da sílaba tônica",
                    "text": (
                        "Oxítonas apresentam a última sílaba tônica; paroxítonas, a penúltima; "
                        "proparoxítonas, a antepenúltima. Toda proparoxítona é acentuada. Oxítonas "
                        "terminadas em a, e, o, em e ens recebem acento, inclusive suas formas "
                        "plurais. As paroxítonas seguem regras específicas de terminação."
                    ),
                },
                {
                    "title": "Hiato e acentos diferenciais",
                    "text": (
                        "Em muitos hiatos, i e u tônicos recebem acento quando formam sílaba "
                        "sozinhos ou com s, como saída e baú. Alguns acentos diferenciam palavras: "
                        "pôde indica passado e pode indica presente; pôr é verbo e por é preposição. "
                        "O acento também distingue têm de tem e vêm de vem."
                    ),
                },
                {
                    "title": "Grafias que exigem contexto",
                    "text": (
                        "Por que aparece em perguntas ou quando equivale a pelo qual; porque costuma "
                        "introduzir explicação ou causa; por quê recebe acento no fim; porquê é "
                        "substantivo. Há indica existência ou tempo passado, enquanto a pode ser "
                        "artigo, preposição ou marca de tempo futuro."
                    ),
                },
            ],
            "examples": [
                {
                    "sentence": "Ele não veio porque estava doente.",
                    "focus": "porque",
                    "answer": "Conjunção causal ou explicativa.",
                },
                {
                    "sentence": "Há dois anos estudo português.",
                    "focus": "há",
                    "answer": "Verbo haver indicando tempo passado.",
                },
            ],
            "tip": "Antes de decorar a grafia, substitua a expressão por outra equivalente e observe o sentido.",
            "quiz": {
                "question": "Qual frase usa corretamente a expressão de causa?",
                "options": [
                    "Faltei porque estava doente.",
                    "Faltei por quê estava doente.",
                    "Faltei por que estava doente.",
                    "Faltei o porquê estava doente.",
                ],
                "answer": 0,
                "explanation": "Porque introduz a causa de faltar.",
            },
        },
        {
            "id": "concordancia",
            "module": "Norma e construção",
            "order": 23,
            "title": "Concordância verbal e nominal",
            "description": "Como verbos e nomes ajustam pessoa, número e gênero.",
            "objectives": [
                "Fazer o verbo concordar com o núcleo do sujeito.",
                "Reconhecer casos de sujeito composto e expressões partitivas.",
                "Aplicar concordância entre substantivos e seus modificadores.",
            ],
            "sections": [
                {
                    "title": "Concordância verbal",
                    "text": (
                        "O verbo normalmente concorda em pessoa e número com o núcleo do sujeito. "
                        "Em Os alunos chegaram, o núcleo alunos exige plural. O sujeito pode vir "
                        "depois do verbo sem perder essa relação. Com sujeito composto anteposto, "
                        "o plural é a forma esperada: Pedro e Ana estudaram."
                    ),
                },
                {
                    "title": "Casos especiais",
                    "text": (
                        "O verbo haver com sentido de existir permanece no singular: havia problemas. "
                        "O verbo fazer indicando tempo também fica no singular: faz dois anos. "
                        "Expressões como a maioria de admitem concordância com o núcleo coletivo ou, "
                        "em certos contextos, com o termo plural que o especifica."
                    ),
                },
                {
                    "title": "Concordância nominal",
                    "text": (
                        "Artigos, pronomes, numerais e adjetivos concordam com o substantivo a que "
                        "se referem. Quando um adjetivo caracteriza mais de um substantivo, gênero, "
                        "posição e sentido influenciam a forma escolhida. Palavras como meio, bastante "
                        "e anexo variam ou permanecem invariáveis conforme a classe usada na frase."
                    ),
                },
            ],
            "examples": [
                {
                    "sentence": "Faz três meses que comecei.",
                    "focus": "faz",
                    "answer": "Singular por indicar tempo decorrido.",
                },
                {
                    "sentence": "As atividades estavam completas.",
                    "focus": "completas",
                    "answer": "Feminino plural em concordância com atividades.",
                },
            ],
            "tip": "Localize o núcleo antes de decidir a forma do verbo ou do adjetivo.",
            "quiz": {
                "question": "Qual frase segue a concordância padrão?",
                "options": [
                    "Havia muitos problemas.",
                    "Haviam muitos problemas.",
                    "Fazem dois anos.",
                    "Existe muitas dúvidas.",
                ],
                "answer": 0,
                "explanation": "Haver com sentido de existir é impessoal e permanece no singular.",
            },
        },
        {
            "id": "regencia-crase",
            "module": "Norma e construção",
            "order": 24,
            "title": "Regência verbal, nominal e crase",
            "description": "Preposições exigidas e o encontro que produz a crase.",
            "objectives": [
                "Identificar preposições exigidas por verbos e nomes.",
                "Distinguir objeto indireto de adjunto adverbial.",
                "Aplicar o teste da crase.",
            ],
            "sections": [
                {
                    "title": "Regência",
                    "text": (
                        "Regência é a relação em que um termo exige ou seleciona uma preposição. "
                        "Gostar pede de; obedecer pede a; confiar pede em. Nomes também podem exigir "
                        "complemento: necessidade de apoio e respeito às regras. O sentido do verbo "
                        "pode mudar sua regência, como ocorre com assistir."
                    ),
                },
                {
                    "title": "Crase",
                    "text": (
                        "A crase gráfica indica a fusão da preposição a com o artigo feminino a ou "
                        "com formas iniciadas por aquele. Troque o termo feminino por um masculino: "
                        "se aparecer ao, haverá crase no feminino. Fui ao mercado; fui à escola. "
                        "Não há crase antes de verbo nem, em regra, antes de palavra masculina."
                    ),
                },
                {
                    "title": "Sentido antes da regra",
                    "text": (
                        "Nem todo a recebe acento. Em Vi a professora, o a é apenas artigo e introduz "
                        "objeto direto. Em Entreguei o relatório à professora, o verbo organiza dois "
                        "complementos e o segundo recebe a preposição exigida, que se funde ao artigo."
                    ),
                },
            ],
            "examples": [
                {
                    "sentence": "Obedeci às regras.",
                    "focus": "às regras",
                    "answer": "Objeto indireto introduzido por a + as.",
                },
                {
                    "sentence": "Cheguei à escola cedo.",
                    "focus": "à escola",
                    "answer": "Preposição a mais artigo feminino.",
                },
            ],
            "tip": "Use o teste do masculino e confirme se o termo anterior realmente exige a preposição a.",
            "quiz": {
                "question": "Em qual frase a crase está correta?",
                "options": [
                    "Entreguei o livro à professora.",
                    "Começou à estudar.",
                    "Visitou à cidade.",
                    "Andou à cavalo.",
                ],
                "answer": 0,
                "explanation": "Entregar algo a alguém exige a preposição, que se une ao artigo feminino.",
            },
        },
        {
            "id": "colocacao-pronominal",
            "module": "Norma e construção",
            "order": 25,
            "title": "Colocação pronominal",
            "description": "Próclise, ênclise e mesóclise com pronomes átonos.",
            "objectives": [
                "Reconhecer as três posições do pronome átono.",
                "Identificar palavras que atraem o pronome.",
                "Empregar o hífen na ênclise e na mesóclise.",
            ],
            "sections": [
                {
                    "title": "Três posições",
                    "text": (
                        "Na próclise, o pronome aparece antes do verbo: não me disseram. Na ênclise, "
                        "vem depois e se liga por hífen: disseram-me. Na mesóclise, entra no interior "
                        "de uma forma do futuro: dir-se-á. A escolha depende da estrutura e também "
                        "do grau de formalidade do texto."
                    ),
                },
                {
                    "title": "Fatores de atração",
                    "text": (
                        "Palavras negativas, pronomes relativos, certos advérbios e conjunções "
                        "subordinativas costumam favorecer a próclise: nunca me avisaram; o livro "
                        "que me deram; quando se levantou. No início formal de oração, evita-se "
                        "começar diretamente por pronome átono."
                    ),
                },
                {
                    "title": "Função do pronome",
                    "text": (
                        "A posição não determina sozinha a função. O, a, os e as normalmente retomam "
                        "objeto direto; lhe e lhes retomam objeto indireto; me, te, nos e vos dependem "
                        "da regência e podem exercer mais de uma função. O se pode ser reflexivo, "
                        "apassivador, indeterminador ou parte integrante do verbo."
                    ),
                },
            ],
            "examples": [
                {
                    "sentence": "Não me contaram a verdade.",
                    "focus": "me",
                    "answer": "Próclise provocada pela palavra negativa.",
                },
                {
                    "sentence": "Entreguei-lhe o relatório.",
                    "focus": "lhe",
                    "answer": "Ênclise; pronome com função de objeto indireto.",
                },
            ],
            "tip": "Primeiro encontre a função do pronome; depois observe se existe uma palavra que favoreça sua posição.",
            "quiz": {
                "question": "Qual frase apresenta ênclise?",
                "options": [
                    "Avisaram-me ontem.",
                    "Não me avisaram.",
                    "Quem me avisou?",
                    "Talvez me avisem.",
                ],
                "answer": 0,
                "explanation": "Em avisaram-me, o pronome aparece depois do verbo e se liga por hífen.",
            },
        },
        {
            "id": "pontuacao-sentido",
            "module": "Norma e construção",
            "order": 26,
            "title": "Pontuação e construção de sentido",
            "description": "Vírgula, dois-pontos, ponto e vírgula e organização sintática.",
            "objectives": [
                "Usar a vírgula sem separar sujeito e verbo.",
                "Pontuar vocativos, apostos e termos deslocados.",
                "Relacionar pontuação à estrutura das orações.",
            ],
            "sections": [
                {
                    "title": "A vírgula organiza",
                    "text": (
                        "A vírgula marca deslocamentos, enumerações e termos intercalados, mas não "
                        "deve separar automaticamente sujeito e predicado. Vocativos e apostos "
                        "explicativos ficam isolados: Ana, venha aqui; Machado de Assis, grande "
                        "escritor brasileiro, nasceu no Rio de Janeiro."
                    ),
                },
                {
                    "title": "Orações",
                    "text": (
                        "Orações coordenadas adversativas e conclusivas costumam ser separadas por "
                        "vírgula. Uma oração adverbial deslocada para o início também costuma recebê-la: "
                        "Quando cheguei, a aula começou. Orações adjetivas explicativas usam vírgulas; "
                        "as restritivas, em regra, não usam."
                    ),
                },
                {
                    "title": "Outros sinais",
                    "text": (
                        "Os dois-pontos introduzem explicação, enumeração, fala ou consequência "
                        "anunciada. O ponto e vírgula separa partes extensas ou já divididas por "
                        "vírgulas. Travessões e parênteses inserem comentários com graus diferentes "
                        "de destaque. A pontuação deve tornar visível a estrutura pretendida."
                    ),
                },
            ],
            "examples": [
                {
                    "sentence": "Quando terminou a prova, o aluno saiu.",
                    "focus": "vírgula",
                    "answer": "Separa a oração adverbial deslocada.",
                },
                {
                    "sentence": "Os alunos que estudaram passaram.",
                    "focus": "sem vírgulas",
                    "answer": "A oração restringe quais alunos passaram.",
                },
            ],
            "tip": "Não pontue apenas pela pausa da fala; identifique os blocos sintáticos da frase.",
            "quiz": {
                "question": "Qual frase está pontuada adequadamente?",
                "options": [
                    "Quando cheguei, a aula começou.",
                    "Os alunos, chegaram cedo.",
                    "A professora explicou, a matéria.",
                    "Meu amigo venha, aqui.",
                ],
                "answer": 0,
                "explanation": "A vírgula separa a oração adverbial temporal deslocada.",
            },
        },
    ]
)


LESSONS_BY_ID = {lesson["id"]: lesson for lesson in LESSONS}


EXERCISES = [
    {
        "id": 1,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "A [criança] encontrou o brinquedo.",
        "answer": "substantivo",
        "options": ["substantivo", "verbo", "advérbio", "preposição"],
        "explanation": "Criança nomeia um ser.",
    },
    {
        "id": 2,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "A criança [encontrou] o brinquedo.",
        "answer": "verbo",
        "options": ["adjetivo", "verbo", "artigo", "numeral"],
        "explanation": "Encontrou exprime a ação e está flexionado.",
    },
    {
        "id": 3,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "Compramos [dois] cadernos.",
        "answer": "numeral",
        "options": ["pronome", "numeral", "conjunção", "interjeição"],
        "explanation": "Dois indica quantidade exata.",
    },
    {
        "id": 4,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "Ela respondeu [calmamente].",
        "answer": "advérbio",
        "options": ["adjetivo", "substantivo", "advérbio", "artigo"],
        "explanation": "Calmamente acrescenta modo à ação de responder.",
    },
    {
        "id": 5,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "Estudei, [mas] ainda tenho dúvidas.",
        "answer": "conjunção",
        "options": ["conjunção", "preposição", "pronome", "verbo"],
        "explanation": "Mas liga orações com sentido de oposição.",
    },
    {
        "id": 6,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função do trecho destacado?",
        "sentence": "[Os novos alunos] chegaram cedo.",
        "answer": "sujeito",
        "options": ["sujeito", "objeto direto", "vocativo", "adjunto adverbial"],
        "explanation": "O trecho concorda com chegaram e apresenta o núcleo alunos.",
    },
    {
        "id": 7,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função do trecho destacado?",
        "sentence": "Ela comprou [um dicionário].",
        "answer": "objeto direto",
        "options": ["predicativo", "objeto direto", "sujeito", "aposto"],
        "explanation": "O trecho completa o verbo comprar sem preposição obrigatória.",
    },
    {
        "id": 8,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função da palavra destacada?",
        "sentence": "Voltaremos [amanhã].",
        "answer": "adjunto adverbial de tempo",
        "options": ["adjunto adverbial de tempo", "objeto indireto", "sujeito", "agente da passiva"],
        "explanation": "A palavra indica quando ocorrerá a ação.",
    },
    {
        "id": 9,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função do trecho destacado?",
        "sentence": "A sala parecia [vazia].",
        "answer": "predicativo do sujeito",
        "options": ["predicativo do sujeito", "objeto direto", "vocativo", "aposto"],
        "explanation": "Vazia atribui um estado ao sujeito por meio do verbo de ligação.",
    },
    {
        "id": 10,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função do trecho destacado?",
        "sentence": "Preciso [de ajuda].",
        "answer": "objeto indireto",
        "options": ["objeto direto", "objeto indireto", "sujeito", "predicativo"],
        "explanation": "O verbo precisar, nesse sentido, exige a preposição de.",
    },
    {
        "id": 11,
        "level": "avancado",
        "type": "oração",
        "prompt": "Classifique a oração destacada.",
        "sentence": "Espero [que você retorne].",
        "answer": "subordinada substantiva objetiva direta",
        "options": [
            "subordinada substantiva objetiva direta",
            "coordenada adversativa",
            "subordinada adverbial temporal",
            "subordinada adjetiva",
        ],
        "explanation": "A oração completa diretamente o sentido de espero.",
    },
    {
        "id": 12,
        "level": "avancado",
        "type": "oração",
        "prompt": "Classifique a oração destacada.",
        "sentence": "O filme [que vimos ontem] era ótimo.",
        "answer": "subordinada adjetiva restritiva",
        "options": [
            "subordinada adjetiva restritiva",
            "subordinada substantiva subjetiva",
            "coordenada conclusiva",
            "subordinada adverbial causal",
        ],
        "explanation": "A oração delimita o substantivo filme sem vírgulas.",
    },
    {
        "id": 13,
        "level": "avancado",
        "type": "oração",
        "prompt": "Classifique a oração destacada.",
        "sentence": "Continuamos [embora estivéssemos cansados].",
        "answer": "subordinada adverbial concessiva",
        "options": [
            "subordinada adverbial concessiva",
            "coordenada aditiva",
            "subordinada substantiva predicativa",
            "oração sem sujeito",
        ],
        "explanation": "O cansaço não impediu a continuidade da ação.",
    },
    {
        "id": 14,
        "level": "avancado",
        "type": "morfossintaxe",
        "prompt": "Em “O belo emociona”, como se analisa “belo”?",
        "sentence": "O [belo] emociona.",
        "answer": "adjetivo substantivado e núcleo do sujeito",
        "options": [
            "adjetivo substantivado e núcleo do sujeito",
            "advérbio e adjunto adverbial",
            "verbo e núcleo do predicado",
            "preposição e objeto indireto",
        ],
        "explanation": "O artigo substantiva o adjetivo, que passa a ocupar o núcleo do sujeito.",
    },
    {
        "id": 15,
        "level": "avancado",
        "type": "morfossintaxe",
        "prompt": "Em qual opção “canto” é substantivo?",
        "sentence": "Observe o contexto.",
        "answer": "O canto dos pássaros acordou a cidade.",
        "options": [
            "O canto dos pássaros acordou a cidade.",
            "Eu canto todos os dias.",
            "Quando canto, fico feliz.",
            "Talvez eu canto esteja correto.",
        ],
        "explanation": "O artigo “o” determina canto como nome; nas outras construções válidas, canto é verbo.",
    },
    {
        "id": 16,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "[Uma] professora explicou a atividade.",
        "answer": "artigo",
        "options": ["artigo", "advérbio", "conjunção", "verbo"],
        "explanation": "Uma apresenta o substantivo professora de maneira indefinida.",
    },
    {
        "id": 17,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "A explicação [clara] ajudou.",
        "answer": "adjetivo",
        "options": ["substantivo", "adjetivo", "preposição", "interjeição"],
        "explanation": "Clara caracteriza o substantivo explicação.",
    },
    {
        "id": 18,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "[Ela] trouxe o caderno.",
        "answer": "pronome",
        "options": ["numeral", "pronome", "artigo", "advérbio"],
        "explanation": "Ela é pronome pessoal e representa a pessoa de quem se fala.",
    },
    {
        "id": 19,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "O livro [de] português sumiu.",
        "answer": "preposição",
        "options": ["preposição", "verbo", "adjetivo", "artigo"],
        "explanation": "De liga livro a português e estabelece uma relação.",
    },
    {
        "id": 20,
        "level": "iniciante",
        "type": "classe",
        "prompt": "Qual é a classe da palavra destacada?",
        "sentence": "[Ufa]! A prova terminou.",
        "answer": "interjeição",
        "options": ["conjunção", "interjeição", "pronome", "substantivo"],
        "explanation": "Ufa expressa alívio de maneira condensada.",
    },
    {
        "id": 21,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a classificação do sujeito destacado?",
        "sentence": "[Pedro e Ana] estudaram juntos.",
        "answer": "sujeito composto",
        "options": ["sujeito simples", "sujeito composto", "sujeito oculto", "oração sem sujeito"],
        "explanation": "O sujeito apresenta dois núcleos: Pedro e Ana.",
    },
    {
        "id": 22,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função do termo destacado?",
        "sentence": "[Alunos], abram o livro.",
        "answer": "vocativo",
        "options": ["sujeito", "objeto direto", "vocativo", "aposto"],
        "explanation": "Alunos chama os interlocutores e fica fora de sujeito e predicado.",
    },
    {
        "id": 23,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função do trecho destacado?",
        "sentence": "Machado de Assis, [grande escritor brasileiro], nasceu no Rio de Janeiro.",
        "answer": "aposto explicativo",
        "options": ["aposto explicativo", "vocativo", "objeto indireto", "agente da passiva"],
        "explanation": "O trecho explica quem é Machado de Assis.",
    },
    {
        "id": 24,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função da palavra destacada?",
        "sentence": "[Minha] mochila desapareceu.",
        "answer": "adjunto adnominal",
        "options": ["adjunto adnominal", "adjunto adverbial", "predicativo", "núcleo do predicado"],
        "explanation": "O pronome possessivo determina o substantivo mochila.",
    },
    {
        "id": 25,
        "level": "intermediario",
        "type": "função",
        "prompt": "Qual é a função do trecho destacado?",
        "sentence": "A atividade foi corrigida [pela professora].",
        "answer": "agente da passiva",
        "options": ["objeto indireto", "agente da passiva", "sujeito", "complemento nominal"],
        "explanation": "A professora pratica a ação que o sujeito sofre na voz passiva.",
    },
    {
        "id": 26,
        "level": "avancado",
        "type": "oração",
        "prompt": "Classifique a oração iniciada pelo conector destacado.",
        "sentence": "Tentei explicar, [porém ninguém ouviu].",
        "answer": "coordenada sindética adversativa",
        "options": [
            "coordenada sindética adversativa",
            "subordinada adverbial causal",
            "coordenada sindética conclusiva",
            "subordinada adjetiva",
        ],
        "explanation": "Porém introduz oposição ao que foi declarado antes.",
    },
    {
        "id": 27,
        "level": "avancado",
        "type": "oração",
        "prompt": "Qual relação a oração destacada estabelece?",
        "sentence": "Fiquei em casa [porque estava chovendo].",
        "answer": "causa",
        "options": ["causa", "condição", "finalidade", "comparação"],
        "explanation": "A chuva apresenta a causa de permanecer em casa.",
    },
    {
        "id": 28,
        "level": "avancado",
        "type": "morfossintaxe",
        "prompt": "Em qual frase “jovem” funciona como substantivo?",
        "sentence": "Compare os contextos.",
        "answer": "O jovem apresentou o projeto.",
        "options": [
            "O jovem apresentou o projeto.",
            "O aluno jovem apresentou o projeto.",
            "A pesquisadora jovem chegou.",
            "Conheci uma equipe jovem.",
        ],
        "explanation": "Na primeira, jovem vem determinado pelo artigo e ocupa o núcleo do sujeito.",
    },
    {
        "id": 29,
        "level": "avancado",
        "type": "morfossintaxe",
        "prompt": "Qual análise explica corretamente os dois usos de “meio”?",
        "sentence": "Bebi [meio] copo e fiquei [meio] cansada.",
        "answer": "numeral no primeiro uso e advérbio no segundo",
        "options": [
            "numeral no primeiro uso e advérbio no segundo",
            "advérbio nos dois usos",
            "substantivo nos dois usos",
            "adjetivo no primeiro e pronome no segundo",
        ],
        "explanation": "O primeiro indica fração; o segundo equivale a “um pouco” e não varia.",
    },
    {
        "id": 30,
        "level": "avancado",
        "type": "oração",
        "prompt": "Qual é o tipo de sujeito em “Precisa-se de funcionários”?",
        "sentence": "[Precisa-se de funcionários].",
        "answer": "sujeito indeterminado",
        "options": ["sujeito indeterminado", "sujeito simples", "sujeito composto", "oração sem sujeito"],
        "explanation": "Com verbo transitivo indireto, o se atua como índice de indeterminação do sujeito.",
    },
]

EXERCISES.extend(
    [
        {
            "id": 31,
            "level": "iniciante",
            "type": "morfossintaxe",
            "prompt": "Qual processo aparece na palavra destacada?",
            "sentence": "Ele ficou [infeliz] com o resultado.",
            "answer": "derivação prefixal",
            "options": [
                "derivação prefixal",
                "composição por justaposição",
                "derivação regressiva",
                "composição por aglutinação",
            ],
            "explanation": "O prefixo in- foi acrescentado à base feliz.",
        },
        {
            "id": 32,
            "level": "iniciante",
            "type": "classe",
            "prompt": "Qual forma completa corretamente a frase?",
            "sentence": "Não fui à aula [___] estava doente.",
            "answer": "porque",
            "options": ["porque", "por quê", "porquê", "por que"],
            "explanation": "Porque introduz a causa de não ter ido à aula.",
        },
        {
            "id": 33,
            "level": "iniciante",
            "type": "classe",
            "prompt": "Qual palavra é uma proparoxítona?",
            "sentence": "Observe a posição da sílaba tônica.",
            "answer": "médico",
            "options": ["médico", "café", "papel", "tambor"],
            "explanation": "Mé-di-co tem a antepenúltima sílaba tônica.",
        },
        {
            "id": 34,
            "level": "iniciante",
            "type": "morfossintaxe",
            "prompt": "Qual frase apresenta ênclise?",
            "sentence": "Observe a posição do pronome átono.",
            "answer": "Entregaram-me o documento.",
            "options": [
                "Entregaram-me o documento.",
                "Não me entregaram o documento.",
                "Quem me entregou o documento?",
                "Talvez me entreguem o documento.",
            ],
            "explanation": "O pronome me aparece depois do verbo e se liga a ele por hífen.",
        },
        {
            "id": 35,
            "level": "intermediario",
            "type": "função",
            "prompt": "Qual alternativa segue a concordância verbal padrão?",
            "sentence": "Escolha a construção adequada.",
            "answer": "Faz dois anos que estudo.",
            "options": [
                "Faz dois anos que estudo.",
                "Fazem dois anos que estudo.",
                "Haviam muitos alunos.",
                "Existe muitas dúvidas.",
            ],
            "explanation": "Fazer indicando tempo decorrido é impessoal e permanece no singular.",
        },
        {
            "id": 36,
            "level": "intermediario",
            "type": "função",
            "prompt": "Por que ocorre crase no trecho destacado?",
            "sentence": "Entreguei o relatório [à professora].",
            "answer": "fusão da preposição a com o artigo a",
            "options": [
                "fusão da preposição a com o artigo a",
                "acentuação obrigatória de toda palavra feminina",
                "marcação de objeto direto",
                "indicação de verbo no passado",
            ],
            "explanation": "Entregar algo a alguém exige a preposição, que se funde ao artigo.",
        },
        {
            "id": 37,
            "level": "intermediario",
            "type": "função",
            "prompt": "Qual é a função do trecho destacado?",
            "sentence": "Obedecemos [às regras].",
            "answer": "objeto indireto",
            "options": [
                "objeto indireto",
                "objeto direto",
                "predicativo do sujeito",
                "agente da passiva",
            ],
            "explanation": "O verbo obedecer exige a preposição a.",
        },
        {
            "id": 38,
            "level": "intermediario",
            "type": "função",
            "prompt": "Por que a vírgula foi usada?",
            "sentence": "[Quando a aula terminou], os alunos saíram.",
            "answer": "separar oração adverbial deslocada",
            "options": [
                "separar oração adverbial deslocada",
                "separar sujeito e verbo",
                "marcar objeto direto",
                "substituir os dois-pontos",
            ],
            "explanation": "A oração temporal veio antes da oração principal.",
        },
        {
            "id": 39,
            "level": "avancado",
            "type": "morfossintaxe",
            "prompt": "Como se classifica a estrutura verbal destacada?",
            "sentence": "Ela [havia sido avisada].",
            "answer": "locução verbal na voz passiva analítica",
            "options": [
                "locução verbal na voz passiva analítica",
                "três orações coordenadas",
                "predicado nominal sem verbo",
                "voz passiva sintética",
            ],
            "explanation": "Havia e sido funcionam como auxiliares, e avisada é o núcleo no particípio.",
        },
        {
            "id": 40,
            "level": "avancado",
            "type": "oração",
            "prompt": "Classifique a oração destacada.",
            "sentence": "[Ao terminar a prova], o aluno saiu.",
            "answer": "subordinada adverbial temporal reduzida de infinitivo",
            "options": [
                "subordinada adverbial temporal reduzida de infinitivo",
                "coordenada sindética aditiva",
                "subordinada substantiva objetiva direta",
                "subordinada adjetiva explicativa",
            ],
            "explanation": "A estrutura indica tempo e apresenta o verbo terminar no infinitivo.",
        },
        {
            "id": 41,
            "level": "avancado",
            "type": "oração",
            "prompt": "Classifique a oração destacada.",
            "sentence": "A verdade é [que ele mentiu].",
            "answer": "subordinada substantiva predicativa",
            "options": [
                "subordinada substantiva predicativa",
                "subordinada adverbial causal",
                "coordenada conclusiva",
                "subordinada adjetiva restritiva",
            ],
            "explanation": "A oração funciona como predicativo do sujeito A verdade.",
        },
        {
            "id": 42,
            "level": "avancado",
            "type": "oração",
            "prompt": "Qual função a oração destacada exerce?",
            "sentence": "Tenho certeza [de que ele virá].",
            "answer": "complemento nominal oracional",
            "options": [
                "complemento nominal oracional",
                "objeto direto oracional",
                "oração coordenada adversativa",
                "adjunto adverbial de lugar",
            ],
            "explanation": "A oração completa o sentido do nome abstrato certeza.",
        },
    ]
)


# Mantém o gabarito equilibrado entre A, B, C e D sem alterar o conteúdo
# das questões. A ordem é determinística para que as alternativas não mudem
# quando o aluno simplesmente recarrega a página.
LESSON_ANSWER_SLOTS = [
    0, 2, 1, 1, 3, 1, 3, 3, 2, 1, 2, 0, 0,
    1, 1, 0, 2, 2, 0, 3, 3, 3, 2, 0, 0, 1,
]

EXERCISE_ANSWER_SLOTS = [
    3, 0, 0, 1, 0, 3, 1, 2, 0, 3, 3, 1, 3, 1,
    0, 2, 3, 1, 2, 2, 1, 1, 0, 0, 2, 3, 1, 1,
    2, 2, 0, 0, 0, 1, 1, 3, 2, 0, 2, 3, 2, 3,
]


def _distribute_answer_positions():
    if len(LESSONS) != len(LESSON_ANSWER_SLOTS):
        raise ValueError("Atualize LESSON_ANSWER_SLOTS ao adicionar ou remover aulas.")
    if len(EXERCISES) != len(EXERCISE_ANSWER_SLOTS):
        raise ValueError("Atualize EXERCISE_ANSWER_SLOTS ao adicionar ou remover exercícios.")

    for lesson, target_slot in zip(LESSONS, LESSON_ANSWER_SLOTS):
        quiz = lesson["quiz"]
        correct_option = quiz["options"].pop(quiz["answer"])
        quiz["options"].insert(target_slot, correct_option)
        quiz["answer"] = target_slot

    for exercise, target_slot in zip(EXERCISES, EXERCISE_ANSWER_SLOTS):
        correct_option = exercise["answer"]
        current_slot = exercise["options"].index(correct_option)
        exercise["options"].pop(current_slot)
        exercise["options"].insert(target_slot, correct_option)


_distribute_answer_positions()


def module_groups():
    groups = []
    for lesson in LESSONS:
        group = next((item for item in groups if item["name"] == lesson["module"]), None)
        if not group:
            group = {"name": lesson["module"], "lessons": []}
            groups.append(group)
        group["lessons"].append(lesson)
    return groups
