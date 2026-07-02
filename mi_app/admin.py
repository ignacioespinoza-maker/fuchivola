from django.contrib import admin

from .models import Match, Player, TeamAssignment, TierEntry


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apodo')
    search_fields = ('nombre', 'apodo')


class TeamAssignmentInline(admin.TabularInline):
    model = TeamAssignment
    extra = 0


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('formato', 'fecha', 'equipo1_color', 'equipo2_color')
    inlines = [TeamAssignmentInline]


@admin.register(TierEntry)
class TierEntryAdmin(admin.ModelAdmin):
    list_display = ('player', 'match', 'category')
    list_filter = ('category',)
