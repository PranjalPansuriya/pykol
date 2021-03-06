"This module is used as a database for KoL skill information."

from kol.Error import SkillNotFoundError
from kol.data import Skills
from kol.manager import FilterManager
from kol.util import Report

__isInitialized = False
__skillsById = {}
__skillsByName = {}

def init():
	"""
	Initializes the SkillDatabase. This method should be called before the 
	database is ever accessed as it ensures that the database is populated
	with all of the data it needs.
	"""
	global __isInitialized
	if __isInitialized == True:
		return
	
	Report.trace("skilldatabase", "Initializing the skill database.")
	cxt = FilterManager.executeFiltersForEvent("preInitializeSkillDatabase")
	if "returnCode" in cxt and cxt["returnCode"] == FilterManager.FINISHED:
		Report.trace("skilldatabase", "Skill database initialized.")
		__isInitialized = True
		return
		
	for skill in Skills.skills:
		addSkill(skill)
	
	FilterManager.executeFiltersForEvent("postInitializeSkillDatabase")
	__isInitialized = True
	Report.trace("skilldatabase", "Skill database initialized.")

def addSkill(skill):
	"Adds a skill to the database."
	__skillsById[skill["id"]] = skill
	__skillsByName[skill["name"]] = skill

def getSkillFromId(skillId, session=None):
	"Returns information about a skill given its ID."
	if not __isInitialized:
		init()
	
	try:
		return __skillsById[skillId].copy()
	except KeyError:
		cxt = FilterManager.executeFiltersForEvent("couldNotFindSkill", session=session, skillId=skillId)
		if "skill" in cxt:
			skill = cxt["skill"]
			addSkill(skill)
			return skill.copy()
		raise SkillNotFoundError("Skill ID %s is unknown." % skillId)

def getSkillFromName(skillName, session=None):
	"Returns information about a skill given its name."
	if not __isInitialized:
		init()
	
	try:
		return __skillsByName[skillName].copy()
	except KeyError:
		cxt = FilterManager.executeFiltersForEvent("couldNotFindSkill", session=session, skillName=skillName)
		if "skill" in cxt:
			skill = cxt["skill"]
			addSkill(skill)
			return skill.copy()
		raise SkillNotFoundError("The skill '%s' is unknown." % skillName)
