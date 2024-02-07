from __future__ import annotations

from app.data.database.components import ComponentType
from app.data.database.database import DB
from app.data.database.skill_components import SkillComponent, SkillTags
from app.engine import (action, banner, combat_calcs, engine, equations,
                        image_mods, item_funcs, item_system, skill_system,
                        target_system)
from app.engine.game_state import game
from app.engine.objects.unit import UnitObject
from app.utilities import utils, static_random


class DoNothing(SkillComponent):
    nid = 'do_nothing'
    desc = 'does nothing'
    tag = SkillTags.CUSTOM

    expose = ComponentType.Int
    value = 1

class Powerstaff(SkillComponent):
	nid = 'powerstaff'
	desc = 'After using a staff, unit can move again.'
	tag = SkillTags.MOVEMENT
	
	def end_combat(self,playback, unit, item, target, mode):
		playbacks = [p for p in playback if p.nid in ('mark_hit', 'heal_hit')]
		if item_system.weapon_type(unit, item) == 'Staff' and any(p.main_attacker is unit for p in playbacks):
			action.do(action.Reset(unit))
			action.do(action.TriggerCharge(unit, self.skill))
	
class GiveBacker(SkillComponent):
	nid = 'givebacker'
	desc = "Adds damage equal to HP lost."
	tag = SkillTags.COMBAT

	def modify_damage(self, unit, item):
		value = unit.get_max_hp() - unit.get_hp()
		return value

