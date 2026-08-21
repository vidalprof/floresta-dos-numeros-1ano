# 🏦 Banco de imagens (PERMANENTE — reuso entre atividades)

Diferente da raiz `_imagens/` (que é caixa de entrada e é esvaziada), esta pasta
`banco/` **fica guardada** para reaproveitar em outras atividades. Todas com
**fundo transparente** (recortadas), estilo realista ilustrado.

## animais/ (34 quando completo)
- **mamiferos/**: cachorro, gato, morcego, baleia, onca, macaco
- **aves/**: tucano, arara, coruja, pinguim, beija-flor, galinha
- **repteis/**: jacare, jiboia, tartaruga, lagarto, camaleao
- **anfibios/**: sapo, perereca, ra, salamandra
- **peixes/**: dourado, tubarao, cavalo-marinho, peixe-palhaco, arraia
- **invertebrados/**: (PENDENTE — cartela ainda não gerada: borboleta, joaninha,
  abelha, aranha, caracol, minhoca, caranguejo, polvo)

## mascotes/
- tato-tatu-naturalista.png (pose parada; faltam as camadas fala/pisca)

## cenarios/
- museu-historia-natural.jpg (fundo largo, com fundo)

## avatares/
- naturalista-1..6.png (crianças exploradoras, tons variados)

## _cartelas_originais/
As folhas originais do ChatGPT (com fundo), caso precise recortar de novo.

> Origem: cartelas geradas no ChatGPT (ago/2026), recortadas com border-flood+
> connected-components (`scratchpad/cortar.py`) — sem custo de recorte pago.

## ⚠️ Lição do recorte (ago/2026) — o Marcos viu o Tato "faltando partes"
O recorte por border-flood come o BRANCO que encosta no fundo branco. Deu certo nos
bichos (o branco deles é cercado por contorno escuro), mas comeu o JALECO branco do
Tato. Regra: sujeito com muito branco (jaleco, avental) → recortar com limiar ALTO
(só o branco puro do fundo sai, ~250) e sempre `binary_fill_holes` para fechar
buracos internos (branco preso entre patas/tentáculos — pegou o lagarto e o polvo).
