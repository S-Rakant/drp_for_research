REGISTRY = {}

from .coordinate import Coordinate
REGISTRY["coordinate"] = Coordinate

from .onehot import Onehot
REGISTRY["onehot"] = Onehot

from .onehot_fov import OnehotFov
REGISTRY["onehot_fov"] = OnehotFov

from .heu_onehot import HeuOnehot
REGISTRY["heu_onehot"] = HeuOnehot

from .heu_onehot_fov import HeuOnehotFov
REGISTRY["heu_onehot_fov"] = HeuOnehotFov

#新しくwrapperを追加
from .ad_dim_onehot_small_fov import AdDimOnehotSmallFov
REGISTRY["ad_dim_onehot_small_fov"] = AdDimOnehotSmallFov

from .ad_dim_onehot_medium_fov import AdDimOnehotMediumFov
REGISTRY["ad_dim_onehot_medium_fov"] = AdDimOnehotMediumFov

from .ad_dim_onehot_large_fov import AdDimOnehotLargeFov
REGISTRY["ad_dim_onehot_large_fov"] = AdDimOnehotLargeFov