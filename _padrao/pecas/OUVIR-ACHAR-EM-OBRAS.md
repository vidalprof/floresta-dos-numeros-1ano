# ⚠️ `ouvir-achar` ESTÁ NO MEIO DE UMA REFAÇÃO VISUAL — NÃO PUBLICAR ASSIM

**Estado:** a bancada REPROVA (`bash _qa/peca.sh _padrao/pecas/ouvir-achar.html` → 1)
e a tela está pior do que estava. Isto é trabalho interrompido, não trabalho pronto.

## O que está quebrado agora (visto no print, não deduzido)

- os cartões continuam **empilhados numa coluna**, quando deviam ser dois por linha;
- o **medalhão vaza para fora** do cartão;
- o **nome sumiu** atrás do cartão seguinte;
- o **alto-falante desapareceu** de cada opção;
- o botão de voz **cobre a última palavra do enunciado**.

## Por que quebrou

Eu troquei o `.opts` e o `.opt.fig` por substituição de texto, mas a peça já tinha
um `.opts{display:block}` vindo do MOLDE. Depois que o integrador põe o nome da
peça na frente de cada regra, as duas ficam com a mesma força e vale a ORDEM no
arquivo — que não é a que eu supus. Mexer em CSS às cegas, sem olhar entre um
passo e outro, foi o método errado.

## Como retomar (o caminho certo)

1. **Desenhar olhando.** Renderizar a peça, mudar UMA regra, renderizar de novo.
   Nada de três mudanças por vez.
2. **O molde é o Broto** (`_jardim/index.html`): figura GRANDE e redonda,
   centrada; respostas em pastilhas numa grade; borda de baixo mais grossa.
   O "jeito do Broto" já está na ponte (`CSS_PONTE` do `integrar.py`) — a peça
   só precisa não brigar com ele.
3. **Regra do Marcos que vale para toda a refação** (ago/2026):
   *"quero que a atividade seja um app lindo, sonoro, didático — se a
   interatividade não se adequa, não utilizar"*. Ou seja: mecânica que não
   couber para quem está se alfabetizando SAI, não se remenda.
4. **E o som e a dica vêm primeiro**, não por último: *"a atividade tem que
   ajudar o estudante pequeno, os sons e as dicas são fundamentais, estão se
   alfabetizando"*.
