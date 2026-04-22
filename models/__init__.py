# -*- coding: utf-8 -*-
from . import vehicle_make        # extends rfh.vehicle.make
from . import vehicle_model       # extends rfh.vehicle.model (adds engine_ids)
from . import vehicle_engine      # spare.vehicle.engine (new model)
from . import product_compatibility  # spare.product.compatibility (bridge)
from . import product_template    # extends product.template (compatibility tab)
from . import vehicle_extension   # extends rfh.vehicle (adds engine_id) + rfh.job.card.part
from . import job_card_extension  # extends rfh.job.card (Find Parts button)
