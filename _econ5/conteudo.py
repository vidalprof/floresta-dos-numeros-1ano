# -*- coding: utf-8 -*-
u"""
============================================================
 CONTEÚDO — "Santa Catarina que Produz" (5º ano, Geografia)

 Pedido do Marcos (18/set/2026): *"Preciso de uma atividade para o 5 ano setor
 primário e setor secundário, detalhes da economia de Santa Catarina e Blumenau,
 cultura, culinária, principais alimentos e produtos. Estilo site com fotos
 textos áudios e um quiz com 25 perguntas ao final"*.

 ⚠️ REGRA ZERO ("nunca chute nunca invente"): cada número e cada fato tem a
    fonte ao lado, em comentário `# FONTE:`, apontando o arquivo colhido pelo
    `pesquisar.yml` em `_pesquisa/web/` (18/set/2026). O que a pesquisa não
    trouxe, NÃO está aqui — por isso não há cidade da cebola, nem ano da
    Marejada, nem "capital de" nenhuma.

 As FOTOS vêm do Wikimedia Commons (`buscar-fotos.yml`, input `commons=`), com
 autor e licença lidos da API e gravados em `creditos.json`; nenhuma é IA.
============================================================
"""
# -*- coding: utf-8 -*-

TURMAS = [u"5º A", u"5º B", u"5º C", u"5º D"]
AVATARES = [u"ec5_cr1.png", u"ec5_cr2.png", u"ec5_cr3.png",
            u"ec5_cr4.png", u"ec5_cr5.png", u"ec5_cr6.png"]
SLUG = u"economia-sc-5ano"
GUIA = u"ec5_guia.png"          # Gali, o explorador (mesmo guia do _geo5, 5º ano)

HISTORIA = (u"Olá! Eu sou o Gali, o explorador, e hoje a nossa expedição é diferente: "
            u"em vez de rios e montanhas, vamos descobrir o que Santa Catarina PRODUZ. "
            u"Quem planta o arroz que você come? De onde vem a maçã da merenda? Quem fez a sua "
            u"camiseta? E como tudo isso sai do estado e chega ao resto do mundo? Vamos passar "
            u"pelo campo, pelo mar, pelas fábricas, pelos portos, e parar em Blumenau, a cidade "
            u"que nasceu da agulha e do tear e hoje faz programas de computador. Explore cada "
            u"parada, ouça as histórias, e no fim mostre o que descobriu no quiz. Vamos?")

TXT_PORTAL_INTRO = (u"Este é o mapa da nossa expedição. Toque numa parada para ir até ela, ou role a "
                    u"página. Cada parada explorada ganha um carimbo. No fim, o quiz com vinte e cinco "
                    u"perguntas.")
TXT_FINAL = (u"Expedição concluída! Agora você sabe o que Santa Catarina planta, cria, pesca, fabrica "
             u"e celebra. O Gali ficou orgulhoso de você. Parabéns, explorador!")
FRASES_NEXT = [u"Boa! Próxima pergunta.", u"Vamos em frente!", u"Continue assim!",
               u"Muito bem, explorador!", u"Falta pouco!"]

# ------------------------------------------------------------------
# SEÇÕES DA REVISTA
#   cls   = cor da etiqueta (classe CSS já existente no index.html)
#   tag   = a palavra curta que aparece na trilha e na etiqueta
#   img   = arquivo em _econ5/img/ (foto do Commons, recortada 1280 px)
#   fatos = 2 ou 3 balas curtas, com número — a criança adora número
#   fala  = o que a voz lê (texto + a bala que mais importa), em frases curtas
# ------------------------------------------------------------------
SECOES = [
 {u"cls": u"eco", u"tag": u"COMEÇO", u"img": u"ec5_intro.jpg",
  u"titulo": u"Três setores, um estado que produz",
  u"texto": (u"Economia é o nome que se dá a tudo o que as pessoas fazem para produzir, vender e "
             u"comprar. Para entender, a gente separa o trabalho em três setores. O setor PRIMÁRIO "
             u"tira da natureza: planta, cria, pesca, corta madeira. O setor SECUNDÁRIO transforma na "
             u"fábrica: o grão vira farinha, o fio vira camiseta, a argila vira piso. E o setor "
             u"TERCIÁRIO vende e serve: a loja, a escola, o hospital, o caminhão que entrega. "
             u"Nesta viagem vamos ver os dois primeiros bem de perto — e descobrir por onde tudo sai."),
  # FONTE: econ5-santa-catarina.md — "Em 2022, a agropecuária respondeu por 6,7% do PIB de SC,
  #        a indústria por 26% (...) e os serviços, por 66,2%".
  u"fatos": [u"De cada 100 reais que Santa Catarina produz, cerca de 7 vêm do campo, 26 da indústria e 66 dos serviços.",
             u"Primário tira da natureza · secundário transforma · terciário vende e serve."],
  u"fala": (u"Economia é tudo o que as pessoas fazem para produzir, vender e comprar. O setor primário "
            u"tira da natureza: planta, cria, pesca. O setor secundário transforma na fábrica: o fio "
            u"vira camiseta. O setor terciário vende e serve: a loja, a escola, o caminhão. De cada cem "
            u"reais que Santa Catarina produz, cerca de sete vêm do campo, vinte e seis da indústria e "
            u"sessenta e seis dos serviços."),
  u"credito": u"Renato Soares/MTur · domínio público"},

 {u"cls": u"pri", u"tag": u"CAMPO", u"img": u"ec5_arroz.jpg",
  u"titulo": u"Setor primário: o arroz do Vale e o milho do Oeste",
  u"texto": (u"Olhe a foto: é uma colheitadeira num arrozal perto de Rio do Sul, no Alto Vale do "
             u"Itajaí. Santa Catarina é o segundo estado que mais produz arroz no Brasil. E o milho? "
             u"O estado colhe 7 milhões de toneladas, mas quase nada vai para a nossa mesa: 97 por cento "
             u"vira ração para porcos e frangos. Ou seja, o milho do campo é o primeiro degrau de uma "
             u"escada que termina no frigorífico."),
  # FONTE: econ5-produtos-agricolas.md — Apec: "segundo lugar na cultura do arroz, fumo e palmito";
  #        econ5-santa-catarina.md — "milho do Estado é de 7 milhões de toneladas - 97% se destinam
  #        ao consumo animal, especialmente à produção de suínos e frangos de corte".
  u"fatos": [u"2º maior produtor de arroz do Brasil.",
             u"7 milhões de toneladas de milho por ano — 97% viram ração.",
             u"Também 2º lugar em fumo e em palmito."],
  u"fala": (u"Esta é uma colheitadeira num arrozal perto de Rio do Sul, no Alto Vale do Itajaí. "
            u"Santa Catarina é o segundo estado que mais produz arroz no Brasil. O estado colhe sete "
            u"milhões de toneladas de milho, mas noventa e sete por cento vira ração para porcos e "
            u"frangos. O milho do campo é o primeiro degrau de uma escada que termina no frigorífico."),
  u"credito": u"Herr stahlhoefer · domínio público"},

 {u"cls": u"pri", u"tag": u"CRIAÇÃO", u"img": u"ec5_suinos.jpg",
  u"titulo": u"Porcos e frangos: o campeão do Brasil",
  u"texto": (u"Quase 3 de cada 10 quilos de carne de porco produzidos no Brasil vêm de Santa Catarina: "
             u"é o primeiro lugar do país, com mais de 16 milhões de cabeças. Em frango, o estado é o "
             u"segundo. A maior parte dessas granjas fica no Oeste, em cidades como Chapecó, cuja "
             u"economia gira em torno da agroindústria: o produtor cria, a indústria abate, embala e "
             u"exporta. A carne suína é, junto com a madeira, o produto que Santa Catarina mais vende "
             u"para outros países."),
  # FONTE: econ5-santa-catarina.md — "maior produtor nacional de carne suína, com 16,88 milhões de
  #        cabeças e 29,5% da produção brasileira"; "segundo lugar na produção de frangos com 13%";
  #        "Carne suína e madeira lideram exportações"; econ5-cultura-culinaria.md — "Chapecó tem sua
  #        economia baseada na agroindústria".
  u"fatos": [u"1º lugar em carne suína: 29,5% do Brasil, mais de 16 milhões de cabeças.",
             u"2º lugar em frango.",
             u"Carne suína e madeira são os campeões de exportação do estado."],
  u"fala": (u"Quase três de cada dez quilos de carne de porco do Brasil vêm de Santa Catarina. É o "
            u"primeiro lugar do país. Em frango, o estado é o segundo. A maior parte das granjas fica no "
            u"Oeste, em cidades como Chapecó, onde a economia gira em torno da agroindústria. A carne "
            u"suína é, junto com a madeira, o que Santa Catarina mais vende para outros países."),
  u"credito": u""},

 {u"cls": u"pri", u"tag": u"POMAR", u"img": u"ec5_maca.jpg",
  u"titulo": u"Maçã e cebola: a serra fria que dá fruta",
  u"texto": (u"Metade das maçãs do Brasil nasce em Santa Catarina: 593 mil toneladas num ano só. A "
             u"maçã gosta de frio, por isso os pomares ficam na Serra, em cidades como São Joaquim e "
             u"Fraiburgo. Na cebola o estado também é o primeiro do país. E repare: a maçã que sobra do "
             u"pomar vira suco e vira o recheio do strudel — o setor primário entregando para o "
             u"secundário."),
  # FONTE: econ5-santa-catarina.md — IBGE: "lidera na maçã (593 mil toneladas, 50,1%), cebola (377
  #        mil toneladas, 23%)"; econ5-cultura-culinaria.md — São Joaquim e Fraiburgo citadas como
  #        cidades da Serra/Oeste (Festa do Vinho Novo de São Joaquim; Fraiburgo); "apfelstrudel
  #        (torta de maçã)".
  u"fatos": [u"593 mil toneladas de maçã: 50,1% de todas as maçãs do Brasil.",
             u"1º lugar também em cebola.",
             u"A maçã gosta de frio — por isso mora na Serra."],
  u"fala": (u"Metade das maçãs do Brasil nasce em Santa Catarina: quinhentas e noventa e três mil "
            u"toneladas num ano só. A maçã gosta de frio, por isso os pomares ficam na Serra, em cidades "
            u"como São Joaquim e Fraiburgo. Na cebola o estado também é o primeiro do país."),
  u"credito": u""},

 {u"cls": u"pri", u"tag": u"MAR", u"img": u"ec5_ostras.jpg",
  u"titulo": u"Ostras e mexilhões: o mar também é lavoura",
  u"texto": (u"Estas redes penduradas na água são 'lanternas' de criar ostras, em Santo Antônio de "
             u"Lisboa, Florianópolis. Criar ostra, mexilhão e vieira no mar chama-se MARICULTURA, e "
             u"aqui Santa Catarina não tem rival: mais de 9 em cada 10 ostras e mexilhões cultivados "
             u"no Brasil saem do litoral catarinense. Pescar e cultivar no mar é setor primário — e "
             u"depois o restaurante que serve a ostra é terciário."),
  # FONTE: econ5-santa-catarina.md — "Na maricultura – cultivo de ostras, vieiras e mexilhões – Santa
  #        Catarina é líder absoluto: representa 91,6% de toda a produção brasileira"; foto do Commons
  #        legendada "A especialidade de Santo Antonio de Lisboa, em Florianópolis, a pesca de ostras".
  u"fatos": [u"91,6% das ostras, mexilhões e vieiras cultivados no Brasil.",
             u"Maricultura = criar frutos do mar no próprio mar.",
             u"Florianópolis tem até a Festa Nacional da Ostra."],
  u"fala": (u"Estas redes penduradas na água são lanternas de criar ostras, em Santo Antônio de Lisboa, "
            u"Florianópolis. Criar ostra e mexilhão no mar chama-se maricultura. Mais de nove em cada "
            u"dez ostras e mexilhões cultivados no Brasil saem do litoral catarinense."),
  u"credito": u"Joao Paulo de Vasconcelos · CC BY-SA 2.0"},

 {u"cls": u"sec2", u"tag": u"FÁBRICA", u"img": u"ec5_ceramica.jpg",
  u"titulo": u"Setor secundário: cada região tem a sua fábrica",
  u"texto": (u"Na foto, trabalhadoras conferem peças numa indústria de cerâmica em Criciúma. O setor "
             u"secundário é isso: pegar o que o primário entregou e transformar. Em Santa Catarina cada "
             u"região ficou boa numa coisa. O Norte, com Joinville e Jaraguá do Sul, faz máquinas, "
             u"motores e móveis. O Oeste faz alimentos. O Planalto Serrano faz papel, celulose e madeira. "
             u"O Sul faz cerâmica de revestimento. E o Vale do Itajaí, o nosso, faz tecido, roupa, navios "
             u"e tecnologia."),
  # FONTE: econ5-santa-catarina.md — "O Norte é polo tecnológico, moveleiro e metal-mecânico"; "O
  #        Oeste concentra atividades de produção alimentar e de móveis"; "O Planalto Serrano tem a
  #        indústria de papel, celulose e da madeira"; "No Sul do estado (...) concentram-se as
  #        principais fábricas de cerâmica de revestimento"; "No Vale do Itajaí, predomina a indústria
  #        têxtil e do vestuário, naval e de tecnologia"; foto CC0 "Trabalhadoras em indústria
  #        cerâmica de Criciúma".
  u"fatos": [u"Norte: máquinas, motores, móveis · Oeste: alimentos · Serra: papel e madeira.",
             u"Sul: cerâmica de revestimento (o piso da sua casa).",
             u"Vale do Itajaí: têxtil, vestuário, naval e tecnologia."],
  u"fala": (u"Na foto, trabalhadoras conferem peças numa indústria de cerâmica em Criciúma. O setor "
            u"secundário pega o que o primário entregou e transforma. O Norte faz máquinas, motores e "
            u"móveis. O Oeste faz alimentos. O Planalto Serrano faz papel e madeira. O Sul faz cerâmica. "
            u"E o Vale do Itajaí, o nosso, faz tecido, roupa, navios e tecnologia."),
  u"credito": u"Anapfana · CC0"},

 {u"cls": u"sec2", u"tag": u"CARVÃO", u"img": u"ec5_carvao.jpg",
  u"titulo": u"Criciúma: a cidade dos homens do carvão",
  u"texto": (u"Este monumento em Criciúma homenageia os 'Homens do Carvão'. No Sul de Santa Catarina "
             u"há carvão mineral debaixo da terra, e durante muitos anos tirar carvão foi o trabalho "
             u"da região. É um carvão que não serve para fazer aço: ele é queimado para gerar energia "
             u"elétrica, ali mesmo, perto da mina. Hoje o Sul também é conhecido pelas fábricas de "
             u"cerâmica de revestimento — os pisos e azulejos que forram as casas do Brasil."),
  # FONTE: econ5-santa-catarina.md — "Como se trata de um carvão de qualidade inferior, é utilizado
  #        apenas na geração de energia termoelétrica e no próprio local da jazida"; "No Sul do estado
  #        (...) concentram-se as principais fábricas de cerâmica de revestimento"; foto Commons "The
  #        monument of the city of Criciúma in honor of the Coal Men".
  u"fatos": [u"O carvão do Sul vira energia elétrica em usinas termoelétricas.",
             u"A mesma região faz os pisos e azulejos de cerâmica."],
  u"fala": (u"Este monumento em Criciúma homenageia os homens do carvão. No Sul de Santa Catarina há "
            u"carvão mineral debaixo da terra. Ele é queimado para gerar energia elétrica perto da "
            u"mina. Hoje o Sul também é conhecido pelas fábricas de cerâmica, os pisos e azulejos das "
            u"casas."),
  u"credito": u"Latinov · CC BY-SA 3.0"},

 {u"cls": u"blu", u"tag": u"1850", u"img": u"ec5_enxaimel.jpg",
  u"titulo": u"1850: nasce Blumenau, colônia de imigrantes",
  u"texto": (u"Blumenau foi fundada em 1850 por imigrantes alemães, na beira do rio Itajaí-Açu. Eles "
             u"trouxeram o jeito de construir casa que você vê na foto — o enxaimel, de madeira e "
             u"tijolo à vista, como esta em Pomerode, cidade vizinha. Trouxeram também a língua, as "
             u"receitas, a cerveja e o costume de trabalhar em oficina. A colônia sofreu com o rio: "
             u"houve enchentes grandes em 1880 e em 1911. Mas foi justamente em 1880 que uma família "
             u"decidiu abrir uma fábrica ali."),
  # FONTE: econ5-cultura-culinaria.md — "Fundada em 1850 por imigrantes alemães"; econ5-historia-
  #        blumenau.md — "Enchentes em Blumenau - Fundação Hermann Hering": "grande enchente no ano de
  #        1880", "Enchente de 1911"; foto Commons "Enxaimel é o principal legado da colonização
  #        alemã" (Pomerode).
  u"fatos": [u"Fundada em 1850 por imigrantes alemães.",
             u"Enxaimel: a casa de madeira e tijolo que eles trouxeram.",
             u"Enchentes grandes em 1880 e 1911 — e a cidade seguiu em frente."],
  u"fala": (u"Blumenau foi fundada em mil oitocentos e cinquenta por imigrantes alemães, na beira do rio "
            u"Itajaí-Açu. Eles trouxeram o enxaimel, a casa de madeira e tijolo à vista, como esta em "
            u"Pomerode. Trouxeram a língua, as receitas, a cerveja. A colônia sofreu enchentes em mil "
            u"oitocentos e oitenta e em mil novecentos e onze. Mas foi em mil oitocentos e oitenta que "
            u"uma família decidiu abrir uma fábrica ali."),
  u"credito": u"Marinelson Almeida · CC BY 2.0"},

 {u"cls": u"blu", u"tag": u"TEAR", u"img": u"ec5_hering.jpg",
  u"titulo": u"1880: os irmãos Hering e um tear que veio de navio",
  u"texto": (u"Em 1880, os irmãos Hermann e Bruno Hering fundaram em Blumenau uma malharia, com um "
             u"tear circular importado da Alemanha: foi a primeira malharia do Sul do Brasil. A foto "
             u"antiga mostra a fábrica de roupas da Companhia Hering. Daquele tear nasceu uma cidade "
             u"inteira de tecidos e roupas: hoje Blumenau concentra 13% dos empregos têxteis de todo o "
             u"estado, e Santa Catarina é o maior polo de vestuário do Brasil. A camiseta que você usa "
             u"pode ter nascido aqui."),
  # FONTE: econ5-historia-blumenau.md — "a empresa criada em 1880, pelos irmãos"; "fundada por Hermann
  #        e Bruno Hering"; "Nasce a Primeira Malharia do Sul do Brasil" (Fundação Cultural de
  #        Blumenau); econ5-blumenau.md — "fundaram a Companhia Hering em Blumenau, utilizando um tear
  #        circular importado da Alemanha"; "concentrando 13% dos empregos formais dessa cadeia em
  #        Santa Catarina"; "Santa Catarina figura como maior polo do vestuário".
  u"fatos": [u"1880: Hermann e Bruno Hering, um tear circular vindo da Alemanha.",
             u"Primeira malharia do Sul do Brasil.",
             u"Blumenau tem 13% dos empregos têxteis de Santa Catarina."],
  u"fala": (u"Em mil oitocentos e oitenta, os irmãos Hermann e Bruno Hering fundaram em Blumenau uma "
            u"malharia, com um tear circular importado da Alemanha. Foi a primeira malharia do Sul do "
            u"Brasil. Daquele tear nasceu uma cidade inteira de tecidos e roupas. Hoje Blumenau tem "
            u"treze por cento dos empregos têxteis de todo o estado."),
  u"credito": u"Wikimedia Commons · domínio público"},

 {u"cls": u"blu", u"tag": u"HOJE", u"img": u"ec5_blumenau.jpg",
  u"titulo": u"Blumenau hoje: do tecido ao computador",
  u"texto": (u"Blumenau tem hoje mais de 360 mil habitantes e continua fazendo roupa — mas ganhou uma "
             u"segunda fama: a tecnologia da informação. Empresas de software nasceram e cresceram na "
             u"cidade; uma delas, a Senior Sistemas, é a maior empresa de programas de gestão do Sul do "
             u"Brasil e dá emprego a mais de 2 mil pessoas. Em Blumenau, de cada 100 reais produzidos, "
             u"58 vêm dos serviços e 29 da indústria de transformação. A cidade que veio do tear "
             u"aprendeu a programar."),
  # FONTE: econ5-blumenau.md — "361.261 habitantes no Censo de 2022"; "Senior Sistemas (...) a maior
  #        empresa de software de gestão da região Sul e é responsável por mais de 2 mil vagas de
  #        empregos na cidade"; "o setor de serviços corresponde a 58% da riqueza gerada, enquanto o
  #        setor de transformação representa 29%".
  u"fatos": [u"361 mil habitantes (Censo 2022).",
             u"Serviços: 58% da riqueza da cidade · indústria de transformação: 29%.",
             u"Polo de tecnologia da informação: a Senior Sistemas emprega mais de 2 mil pessoas."],
  u"fala": (u"Blumenau tem hoje mais de trezentos e sessenta mil habitantes e continua fazendo roupa, "
            u"mas ganhou uma segunda fama: a tecnologia da informação. Empresas de software nasceram e "
            u"cresceram na cidade. De cada cem reais produzidos em Blumenau, cinquenta e oito vêm dos "
            u"serviços e vinte e nove da indústria. A cidade que veio do tear aprendeu a programar."),
  u"credito": u"Charles Ringenberg · CC BY 3.0"},

 {u"cls": u"mar", u"tag": u"PORTOS", u"img": u"ec5_porto.jpg",
  u"titulo": u"Portos: por onde sai o que Santa Catarina produz",
  u"texto": (u"Tudo o que o estado produz precisa viajar. A foto mostra o porto de Itajaí, com seus "
             u"guindastes e contêineres. Santa Catarina tem vários portos no litoral: Itajaí e "
             u"Navegantes, um de frente para o outro no rio; São Francisco do Sul, no Norte, ligado por "
             u"ferrovia a Joinville, Jaraguá do Sul e Mafra; e Imbituba, no Sul, que recebe navios "
             u"gigantes vindos da Ásia. Do porto sai a carne, a madeira, o móvel, a roupa — e entram "
             u"as máquinas e os produtos que compramos de fora."),
  # FONTE: econ5-santa-catarina.md — ferrovia "ligando o porto de São Francisco do Sul à Joinville,
  #        Jaraguá do Sul, Mafra e Porto União"; "Porto de Imbituba entra na escala de navios gigantes
  #        vindos da Ásia"; "São Francisco do Sul e Navegantes (Portonave), que concentram grande
  #        parte da movimentação"; fotos da Marinha do Brasil "Porto de Itajaí, Santa Catarina - 2021".
  u"fatos": [u"Itajaí e Navegantes: contêineres, um porto de cada lado do rio.",
             u"São Francisco do Sul: porto ligado por trem a Joinville e Jaraguá do Sul.",
             u"Imbituba: recebe navios gigantes da Ásia."],
  u"fala": (u"Tudo o que o estado produz precisa viajar. Esta foto mostra o porto de Itajaí, com seus "
            u"guindastes e contêineres. Santa Catarina tem vários portos: Itajaí e Navegantes, São "
            u"Francisco do Sul, ligado por trem a Joinville, e Imbituba, que recebe navios gigantes da "
            u"Ásia. Do porto sai a carne, a madeira, a roupa. E entram as máquinas que compramos de fora."),
  u"credito": u"Marinha do Brasil · CC BY-SA 2.0"},

 {u"cls": u"fes", u"tag": u"FESTA", u"img": u"ec5_okto.jpg",
  u"titulo": u"Oktoberfest: a festa que virou economia",
  u"texto": (u"Em outubro de 1984, Blumenau fez a sua primeira Oktoberfest, no antigo pavilhão da "
             u"Proeb, que hoje é o Parque Vila Germânica: 102 mil pessoas apareceram. A festa virou a "
             u"maior festa alemã das Américas e a segunda maior do mundo. Tem desfile, banda, dança "
             u"típica, e mais de 150 pratos germânicos, como o bretzel, o goulash e o spätzle. Festa "
             u"também é economia: hotel, restaurante, ônibus, artesanato — tudo isso é setor terciário "
             u"trabalhando."),
  # FONTE: econ5-historia-blumenau.md — "Em sua primeira edição, em 1984, recebeu 102 mil pessoas no
  #        antigo pavilhão da Proeb, atual Parque Vila Germânica"; econ5-cultura-culinaria.md — "a
  #        maior festa alemã das Américas e a segunda maior do mundo"; "São mais de 150 pratos
  #        tradicionais germânicos, como o bretzel, o goulash e o spätzle"; "a Vila Germânica possui
  #        importância econômica permanente".
  u"fatos": [u"1ª Oktoberfest: outubro de 1984, 102 mil pessoas.",
             u"Maior festa alemã das Américas, 2ª maior do mundo.",
             u"Mais de 150 pratos típicos na festa."],
  u"fala": (u"Em outubro de mil novecentos e oitenta e quatro, Blumenau fez a sua primeira Oktoberfest, "
            u"e cento e duas mil pessoas apareceram. A festa virou a maior festa alemã das Américas e a "
            u"segunda maior do mundo. Tem desfile, banda, dança e mais de cento e cinquenta pratos "
            u"típicos. Festa também é economia: hotel, restaurante, ônibus, artesanato."),
  u"credito": u"Vitor Pamplona · CC BY 2.0"},

 {u"cls": u"cul", u"tag": u"COZINHA", u"img": u"ec5_comida.jpg",
  u"titulo": u"Na cozinha: cuca, chucrute, marreco e ostra",
  u"texto": (u"A comida conta a história de quem chegou. Dos alemães do Vale vieram a cuca — bolo "
             u"coberto com farofa doce e crocante —, o chucrute com salsicha, o eisbein (joelho de "
             u"porco), o marreco recheado e o strudel de maçã, feito com a maçã da Serra. Em Brusque, o "
             u"marreco ganhou festa própria, a Fenarreco. No litoral, a herança é açoriana: peixe "
             u"assado, camarão e as ostras de Florianópolis. Cada prato junta um produto do campo ou "
             u"do mar com uma tradição de família."),
  # FONTE: econ5-cultura-culinaria.md — "A cuca, bolo de origem alemã coberto com farofa doce
  #        crocante"; "chucrute (...) acompanhado de salsichas"; "eisbein (joelho de porco), chucrute,
  #        salsichas variadas e o famoso marreco recheado"; "apfelstrudel (torta de maçã)"; "Peixe
  #        assado, camarão à milanesa"; "resgate das tradições açorianas" (Florianópolis);
  #        econ5-festas-tipicas.md — "a Fenarreco (abreviação de 'Festa Nacional do Marreco') nasceu
  #        para celebrar o prato típico de marreco recheado" (Brusque).
  u"fatos": [u"Cuca: bolo com farofa doce por cima.",
             u"Chucrute, salsicha, eisbein, marreco recheado, strudel de maçã.",
             u"Litoral: peixe assado, camarão e ostra."],
  u"fala": (u"A comida conta a história de quem chegou. Dos alemães vieram a cuca, bolo coberto com "
            u"farofa doce, o chucrute com salsicha, o joelho de porco, o marreco recheado e o strudel de "
            u"maçã. Em Brusque, o marreco ganhou festa própria, a Fenarreco. No litoral, a herança é "
            u"açoriana: peixe assado, camarão e as ostras de Florianópolis."),
  u"credito": u""},

 {u"cls": u"fes", u"tag": u"VISITA", u"img": u"ec5_turismo.jpg",
  u"titulo": u"Turismo: quando o passeio vira trabalho",
  u"texto": (u"A praia de Balneário Camboriú, a Ponte Hercílio Luz em Florianópolis, as casas enxaimel "
             u"de Pomerode, a Vila Germânica em Blumenau: gente do Brasil inteiro vem passear em Santa "
             u"Catarina. E cada visitante paga hotel, restaurante, passeio de barco, lembrancinha — "
             u"isso é o setor terciário. Em Itajaí, a Marejada celebra o pescado há mais de 36 anos e é "
             u"considerada a maior festa de pescado do Brasil. Turismo é a economia que nasce da "
             u"cultura, da paisagem e da comida."),
  # FONTE: econ5-santa-catarina.md — "A Grande Florianópolis destaca-se nos setores de tecnologia,
  #        turismo, serviços e construção civil"; econ5-festas-tipicas.md — "Com 36 anos de tradição, a
  #        Marejada é considerada a maior festa de pescado do Brasil"; fotos do Commons de Balneário
  #        Camboriú (Praia Central) e da Ponte Hercílio Luz.
  u"fatos": [u"Turismo é setor terciário: hotel, restaurante, passeio, lembrança.",
             u"Marejada, em Itajaí: 36 anos, a maior festa de pescado do Brasil.",
             u"Praia, ponte, enxaimel e festa — a paisagem também produz."],
  u"fala": (u"A praia de Balneário Camboriú, a Ponte Hercílio Luz, as casas enxaimel, a Vila Germânica: "
            u"gente do Brasil inteiro vem passear em Santa Catarina. Cada visitante paga hotel, "
            u"restaurante, passeio de barco. Isso é o setor terciário. Em Itajaí, a Marejada celebra o "
            u"pescado há mais de trinta e seis anos. Turismo é a economia que nasce da cultura, da "
            u"paisagem e da comida."),
  u"credito": u"Nivaldo Cit filho · CC BY-SA 3.0"},
]

# nome da etiqueta no quiz, por chave de cor (a chave É a classe CSS)
SECNOME = {u"eco": u"Economia", u"pri": u"Setor primário", u"sec2": u"Setor secundário",
           u"blu": u"Blumenau", u"mar": u"Portos", u"fes": u"Cultura", u"cul": u"Culinária"}

# ------------------------------------------------------------------
# QUIZ — 25 questões. A ORDEM É A DO curriculo.json:
#   1-12  Santa Catarina: setores e produtos      13-17 Blumenau
#   18-19 portos e transporte                     20-25 cultura e culinária
# `correta` é o índice da opção certa ANTES do embaralhar (o app embaralha).
# Cada pergunta tem a resposta na revista: nada aqui é surpresa.
# ------------------------------------------------------------------
QUESTOES = [
 # ---- 1-12 Santa Catarina: setores e produtos
 {u"sec": u"pri", u"pergunta": u"Plantar arroz, criar porcos e pescar ostras são trabalhos de qual setor da economia?",
  u"opcoes": [u"Setor primário", u"Setor secundário", u"Setor terciário"], u"correta": 0},
 {u"sec": u"sec2", u"pergunta": u"Uma fábrica transforma fio em camiseta. Esse trabalho é de qual setor?",
  u"opcoes": [u"Setor secundário", u"Setor primário", u"Setor terciário"], u"correta": 0},
 {u"sec": u"eco", u"pergunta": u"A loja que vende a camiseta e o caminhão que a entrega fazem parte de qual setor?",
  u"opcoes": [u"Setor terciário", u"Setor primário", u"Setor secundário"], u"correta": 0},
 {u"sec": u"pri", u"pergunta": u"Em qual carne Santa Catarina é o PRIMEIRO produtor do Brasil?",
  u"opcoes": [u"Carne de porco (suína)", u"Carne de boi", u"Carne de peixe"], u"correta": 0},
 {u"sec": u"pri", u"pergunta": u"Quase metade das maçãs do Brasil nasce em Santa Catarina. Por que os pomares ficam na Serra?",
  u"opcoes": [u"Porque a maçã gosta de frio", u"Porque lá tem mar", u"Porque lá chove pouco"], u"correta": 0},
 {u"sec": u"pri", u"pergunta": u"O que acontece com 97% do milho colhido em Santa Catarina?",
  u"opcoes": [u"Vira ração para porcos e frangos", u"Vira pipoca", u"É vendido para a Ásia"], u"correta": 0},
 {u"sec": u"pri", u"pergunta": u"Criar ostras e mexilhões no mar tem um nome. Qual?",
  u"opcoes": [u"Maricultura", u"Agricultura", u"Silvicultura"], u"correta": 0},
 {u"sec": u"pri", u"pergunta": u"Junto com a carne suína, qual produto Santa Catarina mais vende para outros países?",
  u"opcoes": [u"Madeira", u"Ouro", u"Petróleo"], u"correta": 0},
 {u"sec": u"sec2", u"pergunta": u"O Norte de Santa Catarina, com Joinville e Jaraguá do Sul, é famoso por fabricar o quê?",
  u"opcoes": [u"Máquinas, motores e móveis", u"Ostras e camarões", u"Maçã e cebola"], u"correta": 0},
 {u"sec": u"sec2", u"pergunta": u"Qual região de Santa Catarina tem as principais fábricas de cerâmica de revestimento (pisos e azulejos)?",
  u"opcoes": [u"O Sul, perto de Criciúma", u"O Planalto Serrano", u"O Vale do Itajaí"], u"correta": 0},
 {u"sec": u"sec2", u"pergunta": u"O Vale do Itajaí, onde fica Blumenau, é forte em qual indústria?",
  u"opcoes": [u"Têxtil e vestuário", u"Papel e celulose", u"Carvão mineral"], u"correta": 0},
 {u"sec": u"sec2", u"pergunta": u"Para que serve o carvão mineral tirado no Sul de Santa Catarina?",
  u"opcoes": [u"Gerar energia elétrica em usinas", u"Fazer pão", u"Construir navios"], u"correta": 0},
 # ---- 13-17 Blumenau
 {u"sec": u"blu", u"pergunta": u"Blumenau foi fundada em 1850 por imigrantes de qual país?",
  u"opcoes": [u"Alemanha", u"Itália", u"Japão"], u"correta": 0},
 {u"sec": u"blu", u"pergunta": u"Como se chama o estilo de casa de madeira e tijolo à vista que os imigrantes trouxeram?",
  u"opcoes": [u"Enxaimel", u"Oca", u"Arranha-céu"], u"correta": 0},
 {u"sec": u"blu", u"pergunta": u"O que os irmãos Hermann e Bruno Hering fundaram em Blumenau, em 1880?",
  u"opcoes": [u"Uma malharia, com um tear vindo da Alemanha", u"Um porto", u"Uma mina de carvão"], u"correta": 0},
 {u"sec": u"blu", u"pergunta": u"Além do tecido, qual atividade nova deu fama a Blumenau nos últimos anos?",
  u"opcoes": [u"Tecnologia da informação (software)", u"Pesca de ostras", u"Plantação de maçã"], u"correta": 0},
 {u"sec": u"blu", u"pergunta": u"Em Blumenau, de cada 100 reais produzidos, 58 vêm de qual setor?",
  u"opcoes": [u"Serviços", u"Agricultura", u"Mineração"], u"correta": 0},
 # ---- 18-19 portos
 {u"sec": u"mar", u"pergunta": u"Qual porto de Santa Catarina é ligado por FERROVIA a Joinville, Jaraguá do Sul e Mafra?",
  u"opcoes": [u"São Francisco do Sul", u"Imbituba", u"Itajaí"], u"correta": 0},
 {u"sec": u"mar", u"pergunta": u"Para que servem os portos na economia de Santa Catarina?",
  u"opcoes": [u"Para os produtos saírem para outros países e as compras entrarem", u"Só para passeio de barco", u"Para plantar arroz"], u"correta": 0},
 # ---- 20-25 cultura e culinária
 {u"sec": u"fes", u"pergunta": u"Em que ano Blumenau fez a sua primeira Oktoberfest, com 102 mil pessoas?",
  u"opcoes": [u"1984", u"1850", u"2020"], u"correta": 0},
 {u"sec": u"fes", u"pergunta": u"Hotel, restaurante e passeio de barco para os turistas são trabalhos de qual setor?",
  u"opcoes": [u"Setor terciário", u"Setor primário", u"Setor secundário"], u"correta": 0},
 {u"sec": u"cul", u"pergunta": u"O que é a cuca?",
  u"opcoes": [u"Um bolo coberto com farofa doce", u"Uma sopa de peixe", u"Um tipo de queijo"], u"correta": 0},
 {u"sec": u"cul", u"pergunta": u"Qual prato dos imigrantes alemães usa a maçã da Serra catarinense?",
  u"opcoes": [u"Strudel de maçã", u"Chucrute", u"Marreco recheado"], u"correta": 0},
 {u"sec": u"cul", u"pergunta": u"Em Brusque existe a Fenarreco, a Festa Nacional do... quê?",
  u"opcoes": [u"Marreco", u"Camarão", u"Pinhão"], u"correta": 0},
 {u"sec": u"cul", u"pergunta": u"No litoral, a comida tem herança açoriana. Qual destes é um prato do litoral catarinense?",
  u"opcoes": [u"Peixe assado com camarão e ostras", u"Chucrute com salsicha", u"Cuca"], u"correta": 0},
]

# ------------------------------------------------------------------
# TROCAS NO MOLDE — o que o `_vale4` deixou escrito no HTML fora do bloco CONFIG
# (título, capa, quiz, final). O montador avisa se alguma não achar o texto.
# ------------------------------------------------------------------
TROCAS_NO_MOLDE = [
 (u"<title>A Viagem no Tempo do Vale — 4º ano</title>", u"<title>Santa Catarina que Produz — 5º ano</title>"),
 (u'alt="Juca, o bugio guia"', u'alt="Gali, o explorador"'),
 (u'alt="Juca, o bugio"', u'alt="Gali, o explorador"'),
 (u"Viagem no tempo &middot; 4º ano &middot; Colonização do Vale", u"Geografia &middot; 5º ano &middot; Economia de Santa Catarina"),
 (u"<h1>A Viagem no Tempo do Vale</h1>", u"<h1>Santa Catarina que Produz</h1>"),
 (u"<h2>A colonização do Vale do Itajaí</h2>", u"<h2>Campo, mar, fábrica, porto — e Blumenau</h2>"),
 (u"Oi! Eu sou o Juca, o bugio. Vamos viajar pela história do Vale do Itajaí com imagens e narração, e depois responder a um quiz!",
  u"Oi! Eu sou o Gali, o explorador. Vamos descobrir o que Santa Catarina planta, cria, fabrica e celebra, com fotos e narração, e depois responder a um quiz!"),
 (u"&#128266; Ouvir o Juca", u"&#128266; Ouvir o Gali"),
 (u"Toque numa parada do mapa para viajar até ela, ou role a página. Cada parada que você explora ganha um carimbo de ouro. No fim, o quiz!",
  u"Toque numa parada do mapa para ir até ela, ou role a página. Cada parada que você explora ganha um carimbo de ouro. No fim, o quiz!"),
 (u"São perguntas sobre a história e a colonização do Vale. O Juca lê cada pergunta em voz alta.",
  u"São 25 perguntas sobre o que Santa Catarina e Blumenau produzem. O Gali lê cada pergunta em voz alta."),
 (u"<h1>Viagem concluída!</h1>", u"<h1>Expedição concluída!</h1>"),
 (u", você terminou a viagem no tempo pelo Vale!", u", você terminou a expedição por Santa Catarina!"),
 (u"O Juca adorou descobrir a história do Vale com você. Parabéns, explorador do tempo!",
  u"O Gali adorou descobrir com você o que Santa Catarina produz. Parabéns, explorador!"),
 (u'localStorage.setItem("sc5_mudo"', u'localStorage.setItem("ec5_mudo"'),
 (u'localStorage.getItem("sc5_mudo"', u'localStorage.getItem("ec5_mudo"'),
]
