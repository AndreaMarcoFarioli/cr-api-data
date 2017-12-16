"""
Card Stats
Combine multiple CSVs for a unified json file.
"""

from .base import BaseGen


class Card:
    """Data about a single card."""
    def __init__(self):
        pass

class TroopCard(Card):
    """Troops, aka characters in CSVs.

    Params:
        :data: a dictionary of fields from a row in CSV.
    """
    def __init__(self, data):
        self._data = data

    @property
    def speed_en(self):
        speed = self._data.get('speed')
        if speed is None:
            return None
        speed = int(speed)
        if speed <= 45:
            return 'slow'
        if speed <= 60:
            return 'medium'
        if speed <= 90:
            return 'fast'
        if speed <= 120:
            return 'very fast'
        return None

    @property
    def dps(self):
        if not self._data.get('hit_speed'):
            return None
        if not self._data.get('damage'):
            return None
        if self._data.get('hit_speed') == 0:
            return None
        return self._data.get('damage') / self._data.get('hit_speed') * 1000

    def to_dict(self):
        data = self._data
        props = ['speed_en', 'dps']
        for prop in props:
            data[prop] = getattr(self, prop)
        return data




class Buildings(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="buildings", json_id="cards_stats")


class AreaEffectsObjects(BaseGen):
    """Spells."""
    def __init__(self, config):
        super().__init__(config, id="area_effect_objects")

class Characters(BaseGen):
    """Characters."""
    def __init__(self, config):
        super().__init__(config, id="characters")


class CardStats(BaseGen):
    """Card stats"""
    def __init__(self, config):
        super().__init__(config, json_id="cards_stats")
        self.config = config
        self.exclude_fields = [
            "LoopingEffect", "OneShotEffect", "ScaledEffect", "HitEffect", "Pushback",
            "PushbackAll", "MinPushback", "MaximumTargets",
            "ProjectileStartHeight",
            "ProjectilesToCenter", "SpawnsAEO", "ControlsBuff", "Clone", "AttractPercentage"

        ]

    def run(self):
        buildings = Buildings(self.config)
        buildings_data = buildings.load_csv(exclude_empty=True)

        area_effect_objects = AreaEffectsObjects(self.config)
        area_effect_objects_data = area_effect_objects.load_csv()

        characters = Characters(self.config)
        characters_data = characters.load_csv(exclude_empty=True)
        troops = []
        for character_data in characters_data:
            troop = TroopCard(character_data)
            troops.append(troop.to_dict())

        self.save_json({
            "troop": characters_data,
            "building": buildings_data,
            "spell": area_effect_objects_data
        })


