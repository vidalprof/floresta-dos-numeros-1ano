# Painel do Laboratório (abrir link em todos os PCs ao mesmo tempo)
Sem instalar nada, sem admin. Só navegador.

- `index.html` = tela do ALUNO. Definir como **página inicial** dos PCs do lab,
  com a sala na URL: `.../index.html?sala=sala1`. Fica "Aguardando o professor".
- `controle.html` = tela do PROFESSOR. Cola o link, "Abrir em todos" → todas as
  telas abrem juntas (dentro de uma moldura, pra o professor seguir no controle).
  "Trazer de volta" → todos voltam pro aguardando. Atalhos salvos no navegador.
- SALA: professor e alunos precisam usar a MESMA sala.
- Canal grátis: ntfy.sh (poll, sem conta). Se a escola bloquear, trocar o HOST
  no topo dos 2 arquivos (ex.: Firebase Realtime, ou outro).
- A atividade abre em IFRAME (as atividades do vidalprof não bloqueiam iframe).
