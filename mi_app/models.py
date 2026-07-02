from django.db import models


class Player(models.Model):
    nombre = models.CharField(max_length=120)
    apodo = models.CharField(max_length=80, blank=True)
    foto = models.ImageField(upload_to='player_photos/', blank=True, null=True)

    def __str__(self):
        return self.apodo or self.nombre


class Match(models.Model):
    FORMATO_CHOICES = [
        ('7vs7', '7 vs 7'),
        ('8vs8', '8 vs 8'),
        ('9vs9', '9 vs 9'),
        ('10vs10', '10 vs 10'),
        ('11vs11', '11 vs 11'),
    ]
    COLOR_CHOICES = [
        ('blanco', 'Blanco'),
        ('negro', 'Negro'),
    ]

    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    jugadores = models.ManyToManyField(Player, blank=True)
    equipo1_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='blanco')
    equipo2_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='negro')

    def __str__(self):
        return f"Partido {self.formato} - {self.fecha:%Y-%m-%d %H:%M}"

    def get_required_player_count(self):
        return int(self.formato.split('vs')[0]) * 2

    def get_team_color(self, team_number):
        return self.equipo1_color if team_number == 1 else self.equipo2_color


class TeamAssignment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='asignaciones')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.IntegerField(choices=[(1, 'Equipo 1'), (2, 'Equipo 2')])

    def __str__(self):
        return f"{self.player} - Equipo {self.team} ({self.match.formato})"


class TierEntry(models.Model):
    CATEGORY_CHOICES = [
        ('crack', 'Crack'),
        ('bueno', 'Bueno'),
        ('puede_ser_mejor', 'Puede ser mejor'),
        ('tronco', 'Tronco'),
        ('lesionado', 'Lesionado'),
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='puede_ser_mejor')

    class Meta:
        unique_together = ('player', 'match')

    def __str__(self):
        return f"{self.player} - {self.get_category_display()}"
