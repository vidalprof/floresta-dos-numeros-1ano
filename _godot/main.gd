extends Node2D

# PROVA: personagem com FISICA NATIVA da engine (CharacterBody2D + move_and_slide).
# Nada de colisao na mao: paredes/obstaculo sao StaticBody2D com CollisionShape2D.

var player: CharacterBody2D
var fps_label: Label
const SPEED := 220.0

func _ready() -> void:
	# fundo (grama)
	var bg := ColorRect.new()
	bg.color = Color(0.56, 0.82, 0.42)
	bg.size = Vector2(640, 360)
	add_child(bg)

	# paredes + obstaculo (colisores NATIVOS)
	_parede(Vector2(320, 8), Vector2(640, 16))
	_parede(Vector2(320, 352), Vector2(640, 16))
	_parede(Vector2(8, 180), Vector2(16, 360))
	_parede(Vector2(632, 180), Vector2(16, 360))
	_parede(Vector2(420, 200), Vector2(96, 96))   # obstaculo no meio

	# player (CharacterBody2D)
	player = CharacterBody2D.new()
	player.position = Vector2(150, 180)
	var cs := CollisionShape2D.new()
	var circ := CircleShape2D.new()
	circ.radius = 18.0
	cs.shape = circ
	player.add_child(cs)
	var corpo := ColorRect.new()
	corpo.color = Color(0.33, 0.78, 0.90)
	corpo.size = Vector2(36, 36)
	corpo.position = Vector2(-18, -18)
	player.add_child(corpo)
	add_child(player)

	# HUD de FPS (prova que roda + quantos quadros)
	fps_label = Label.new()
	fps_label.position = Vector2(12, 8)
	fps_label.add_theme_color_override("font_color", Color.BLACK)
	add_child(fps_label)

	var dica := Label.new()
	dica.text = "Godot Web - setas pra andar (fisica nativa: nao atravessa)"
	dica.position = Vector2(12, 332)
	dica.add_theme_color_override("font_color", Color(0.1, 0.2, 0.1))
	add_child(dica)

func _parede(pos: Vector2, sz: Vector2) -> void:
	var w := StaticBody2D.new()
	w.position = pos
	var cs := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = sz
	cs.shape = rect
	w.add_child(cs)
	var vis := ColorRect.new()
	vis.color = Color(0.55, 0.40, 0.26)
	vis.size = sz
	vis.position = -sz / 2.0
	w.add_child(vis)
	add_child(w)

func _physics_process(_delta: float) -> void:
	var dir := Vector2.ZERO
	dir.x = Input.get_axis("ui_left", "ui_right")
	dir.y = Input.get_axis("ui_up", "ui_down")
	if dir.length() > 0.0:
		dir = dir.normalized()
	player.velocity = dir * SPEED
	player.move_and_slide()   # FISICA NATIVA — velocidade zera no impacto sozinha

func _process(_delta: float) -> void:
	if fps_label:
		fps_label.text = "FPS: %d" % Engine.get_frames_per_second()
