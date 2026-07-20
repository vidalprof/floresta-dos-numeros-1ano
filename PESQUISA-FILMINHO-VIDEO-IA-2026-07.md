# Pesquisa — "Filminho" de abertura/final por IA (vídeo) para 1 HTML offline (2026-07)

> Pergunta do Marcos: "não tem um app que faça um pequeno filme de abertura e final?". Alvo: 1 HTML,
> offline, PC FRACO, 6-12. Força: [FORTE]/[CONSENSO]/[OPINIÃO].

## VEREDITO (uma linha) [OPINIÃO forte]
Pro alvo (1 HTML/offline/Chromebook-Intel HD), **vídeo real embutido quase nunca compensa**. Ordem:
1. **Motion-comic turbinado (tempo real)** — anima as imagens que já geramos (Ken Burns + parallax + fades
   + partículas + narração), **peso extra ≈ zero**, decode = imagem, roda liso. Parece abertura de filme.
2. **Vídeo IA DESTILADO em sprite-sheet / WebP animado** (~0,2-0,5MB, cabe base64, decodifica como imagem,
   loopa) — quando quer o "brilho" de vídeo sem o peso.
3. **Vídeo real, curto, ARQUIVO SEPARADO** (~1-1,5MB, H.264 720p, NÃO base64) — só quando o movimento não
   dá pra fingir (personagem fluido, câmera atravessando, água/fogo) E é one-shot (abertura/final).

## FERRAMENTAS de vídeo por IA (via API/workflow)
**Nuvem (paga por uso, "centavos"):**
- **Veo 3/3.1 (via Gemini API — nosso `GEMINI_API_KEY`)** [FORTE]: `generate_videos` (dispara→poll→baixa),
  **image-to-video** (anima nossa cena). Custo $0,15/s (Fast) a $0,40/s. Clipe 8s = $1,20-$3,20. **SEM tier
  grátis p/ vídeo** — a chave precisa estar no **billing pago**. 720p/1080p 24fps mp4 c/ áudio. Watermark SynthID.
- **MiniMax/Hailuo** ~$0,045/s @768p (o mais barato); **Runway Gen-4 Turbo** $0,05/s; **Pika** (via fal) $0,05/s;
  **Kling** ~$0,084-0,168/s; **Luma Ray2** ~$0,16/s. Todos img2vid, uso comercial ok.
- **Gateways fal.ai / Replicate** [FORTE]: uma API → vários modelos, pay-as-you-go sem assinatura (ex.: Wan 2.5
  $0,05/s). Rodam os open-source por você (não precisa GPU própria).
- **Pollinations vídeo** (grátis, sem chave) [OPINIÃO/não verificado]: anuncia text/img2vid em gen.pollinations.ai
  — vale TENTAR de graça no workflow, mas **sem prometer** qualidade (a rede do chat bloqueia o teste).

**Open-source no runner grátis do Actions? NÃO [FORTE]:** o runner é 2 vCPU/7GB/SEM GPU; SVD/AnimateDiff/
CogVideoX/LTX/Wan exigem 8-24GB de VRAM. Rodá-los = via fal/Replicate (centavos), não no Actions grátis.

## PESO (números) [FORTE]
`MB ≈ bitrate(Mbps) × s ÷ 8`. Clipe 8s 720p: **H.264 ~1,2Mbps ≈ 1,2MB** (HW decode universal, o mais seguro);
**VP9 webm ~0,7Mbps ≈ 0,7MB** (HW desde 2015); **AV1 ≈ 0,5MB MAS software-decode em PC de escola = TRAVA →
EVITAR**; **sprite-sheet WebP ~0,2-0,5MB** (decodifica como imagem, trivial). **base64 infla ~33% e vira texto**
(custa parse/RAM no boot) → **vídeo real = arquivo separado**; base64 só p/ o leve (sprite/WebP).
`<video muted playsinline preload="none" poster>` sem controls/loop; webm+mp4 como `<source>`; ffmpeg `+faststart`.

## PIPELINE (workflow) — quando quiser vídeo real
`gerar-video.yml` (workflow_dispatch): imagem base → `google-genai` `generate_videos` (Veo img2vid, poll, baixa
via Files API) → **ffmpeg** otimiza (H.264 720p ~1,5Mbps `+faststart` + VP9 webm) → commita `_novo/abertura.mp4`
+`.webm`. Trocar Veo por **fal.ai** (`FAL_KEY`) p/ Wan/Hailuo mais barato. QA de peso: se .mp4 > ~1,5MB, sobe o crf.

## RECOMENDAÇÃO p/ A Fábrica de Estrelas
- **De graça e confiável:** motion-comic turbinado (item 1) — é o caminho padrão.
- **Se quiser o "uau" de vídeo:** gerar 2 clipes (abertura+final ~8s) UMA vez por IA e **destilar em WebP/sprite**
  (item 2) p/ caber leve; ou arquivo mp4/webm separado (item 3) se topar ~1MB ao lado do HTML. Custo total dos
  2 clipes: ~$0,50-1,00 (Wan/Hailuo/Runway Turbo) a ~$2,40 (Veo Fast) — precisa billing pago no Gemini/fal.

## FONTES
Veo pricing https://developers.googleblog.com/veo-3-and-veo-3-fast-new-pricing · Veo API https://ai.google.dev/gemini-api/docs/video
· fal.ai https://fal.ai/pricing · MiniMax https://platform.minimax.io/docs/guides/pricing-video · Runway
https://docs.dev.runwayml.com/guides/pricing · Wan/LTX/SVD (VRAM) https://willitrunai.com/blog/wan-2-2-vram-requirements
· runners https://docs.github.com/en/actions/reference/runners/github-hosted-runners · codec/decode
https://sureshot.video/blog/best-video-format-for-web · base64 https://debugbear.com/blog/base64-data-urls-html-css
· sprite/Ken Burns https://joshwcomeau.com/animation/sprites · https://www.kirupa.com/html5/ken_burns_effect_css.htm
· Pollinations https://github.com/pollinations/pollinations
