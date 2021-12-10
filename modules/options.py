

import modules.arguments as arguments
import modules.version as version


# ~~~ #        variables
# some versioning args
ver = version.ver
purpose = version.__purpose__
copyright = f'Copyright ©️ 2021, {version.__author__}'
license_info = version.__license__
# args used by other modules
args = arguments.get_args()
