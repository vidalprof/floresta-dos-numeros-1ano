> caminhada **a cada ~34px percorridos** — senão o pé patina na aceleração. Enquanto o
> personagem acelera/desacelera, um relógio de "a cada 140 ms" faz o pé escorregar (moonwalk); um
> relógio de "a cada 34 px" faz o pé **prender** no chão em qualquer velocidade.

É assim que o motor top-down realmente escolhe o quadro — **pela distância acumulada, não por
ms fixo**:

```js
/* real: _pub_confeitaria/proto/index.html — quadro do chef pela DISTÂNCIA andada */
chef.dTot = (chef.dTot||0) + passo;        // passo = distância percorrida neste frame
chef.frame4 = Math.floor(chef.dTot/13)%4;  // ciclo de 4 poses: um quadro a cada 13px
chef.frame  = Math.floor(chef.dTot/24)%2;  // ciclo de 2 poses: um quadro a cada 24px
```

Repare que o quadro é `Math.floor(distância / passoEmPx)`, não `Math.floor(agora / passoEmMs)`.
Assim, se o chef está parando, os quadros também "param"; se dispara, aceleram junto. Zero patinada.

**Onde o TEMPO ainda manda.** Timing por tempo continua correto para tudo que **não é
locomoção**: respiração (`mvResp` 2.6s), squash de pouso (180 ms), aceno idle (~4s/~6s), clima
(dia 70s/noite 45s). Para essas, vale o corolário técnico clássico do navegador: **o relógio é o
tempo real, nunca a contagem de frames** — o PC da escola roda a 18 fps num dia e 60 no outro.
Deslocamento eased do mundo lateral usa `MV.vx += (alvo - MV.vx) * .16` por tick de 33 ms, e o
quique é senoidal; nada depende de "contar frames do navegador".

> **Nota honesta sobre o mundo lateral.** No `mvTick`, a troca de pose de andar do chef é
> disparada por `if (ag - MV.tFrame > 135)` — ou seja, **135 ms** entre poses. Isso não contradiz
> a regra: como a velocidade do mundo é fortemente suavizada (easing `.16`) e no cruzeiro fica
> quase constante, "135 ms" ≈ "~34 px" na prática. O **padrão seguro** — o que nunca patina em
> aceleração — é a distância; o 135 ms é o equivalente aceitável quando a velocidade é eased e
> estável. Na dúvida, **use distância**. (O "135 ms do demo" é canônico e testado — mexer nele é
> mecânica de motor, `MUNDO-VIVO-ESPINHA.md` §6/§7.)

**Erro típico.** Contar frames do navegador (o câmera-lenta do PC fraco); `dt` sem teto (aba
minimizada volta e o personagem atravessa a parede); e — o clássico do projeto — trocar o quadro
de andar por **tempo** e ver o pé patinar na aceleração. A cura é o `dTot` acima.

---

## Tabela final — quantos quadros para quê
