# -*- coding: utf-8 -*-
u"""QUAIS PASTAS SÃO ATIVIDADES — um cérebro só para os portões.

Nem toda pasta que começa com `_` é uma atividade. `_novo` é a área de
PUBLICAÇÃO: na hora de publicar, a atividade é **copiada inteira** para lá. Os
portões que varrem as pastas vizinhas procurando resto de clone encontravam essa
cópia e reprovavam a atividade por ser igual a **si mesma**:

    !! o mascote daqui se chama 'Ará', o MESMO nome do mascote de _novo
    !! 28 IMAGEM(NS) COPIADA(S) DE OUTRA ATIVIDADE
       _naveg/img/nv_base.png  ==  _novo/img/nv_base.png

E isso acontecia justamente no passo de PUBLICAR, que é onde eu mais preciso
confiar no que o portão diz. Portão que grita à toa ensina a ignorar portão.

Dois portões cometeram o mesmo erro separadamente (`clone.py` e
`arte_propria.py`), o que é o sinal clássico de regra copiada em vez de
compartilhada. Por isso a lista mora aqui, e só aqui.
"""
import os

# áreas de serviço da fábrica — não são atividades da criança
NAO_E_ATIVIDADE = (
    "_novo",         # área de publicação (cópia da atividade que vai ao ar)
    "_recuperado",   # o que voltou de outro repositório
    "_lote", "_cartelas", "_imagens",   # matéria-prima de geração
    "_audio",        # saída padrão do workflow de voz
    "_padrao", "_qa", "_templates", "_kit", "_lib_jogo",  # ferramenta
    "_curriculo", "_plano", "_status", "_demos",          # documento
    # ⚠️ LICAO PAGA (set/2026): a COBAIA e uma atividade de mentira gerada pelo
    #    `_qa/cobaia.py` com o texto de EXEMPLO de todas as 84 mecanicas. Como
    #    vizinha, ela fazia o `clone.py` acusar toda atividade de repetir frase
    #    "da _cobaia" — o exemplo da peca e igual em todo lugar, por definicao.
    #    E a `_colecao` e so uma pasta de imagens (`img/`, sem index): o prefixo
    #    dela ("cor_") casava com o nome do portao `_qa/cor_fixa.py` citado num
    #    comentario, e o clone reprovava a _gincana e a _trem, ambas no ar.
    "_cobaia", "_colecao",
)


def e_atividade(nome):
    u"""a pasta é uma ATIVIDADE (e não área de serviço)?"""
    return nome.startswith("_") and os.path.basename(nome.rstrip("/")) not in NAO_E_ATIVIDADE
