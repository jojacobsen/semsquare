#!/usr/bin/env python3
import pandas as pd
import json
import plspm.config as c
from plspm.plspm import Plspm
from plspm.scheme import Scheme
from plspm.mode import Mode
from plspm.scale import Scale

#fake input for testing
big_input = { "data": "",
              "scheme": "centroid",
               "latent_variables":[
                  {
                     "name":"POLINS",
                     "mode":"reflective",
                     "pointed_lvs":[
                        "AGRI",
                        "IND"
                     ],
                     "pointed_mvs":[
                        {
                           "name":"ecks",
                           "scaling":""
                        },
                        {
                           "name":"death",
                           "scaling":""
                        },
                        {
                           "name":"demo",
                           "scaling":"NOM"
                        },
                        {
                           "name":"inst",
                           "scaling":""
                        }
                     ]
                  },
                  {
                     "name":"AGRI",
                     "mode":"reflective",
                     "pointed_lvs":[

                     ],
                     "pointed_mvs":[
                        {
                           "name":"gini",
                           "scaling":""
                        },
                        {
                           "name":"farm",
                           "scaling":""
                        },
                        {
                           "name":"rent",
                           "scaling":""
                        }
                     ]
                  },
                  {
                     "name":"IND",
                     "mode":"reflective",
                     "pointed_lvs":[

                     ],
                     "pointed_mvs":[
                        {
                           "name":"gnpr",
                           "scaling":"ORD"
                        },
                        {
                           "name":"labo",
                           "scaling":"ORD"
                        }
                     ]
                  }
               ]
        }

#read data from json
input = json.dumps(big_input)
input_json = json.loads(input)

#dataset = pd.read_json(input_json["data"])
#just for testing use csv from github - later on read dataset from json
dataset = pd.read_csv("https://raw.githubusercontent.com/GoogleCloudPlatform/plspm-python/trunk/tests/data/russa.csv", delimiter=",", index_col=0)

### run pls path
default_scale = Scale.NUM #Alternatives: Scale.NOM, Scale.ORD
default_scheme = Scheme.CENTROID #Alternatives: Scheme.FACTORIAL Scheme.PATH

scaling_dict = {"ORD": Scale.ORD,
                "NUM": Scale.NUM,
                "NOM": Scale.NOM,
                "": default_scale}

mode_dict = {"reflective": Mode.A,
             "formative": Mode.B}

scheme_dict = {"centroid": Scheme.CENTROID,
               "factorial": Scheme.FACTORIAL,
               "path": Scheme.PATH,
               "": default_scheme}

scheme = scheme_dict[input_json["scheme"]]

#initialize structure
structure = c.Structure()

#add paths to structure
for latent_var in input_json["latent_variables"]:
    if latent_var["pointed_lvs"]:
        structure.add_path(latent_var["pointed_lvs"], [latent_var["name"]])

config = c.Config(structure.path(), default_scale=default_scale)
for latent_var in input_json["latent_variables"]:
    if latent_var["pointed_mvs"]:
        config.add_lv(latent_var["name"], mode_dict[latent_var["mode"]], *[c.MV(mv["name"], scaling_dict[mv["scaling"]]) if mv["scaling"] else c.MV(mv["name"]) for mv in latent_var["pointed_mvs"]])

plspm_calc = Plspm(dataset, config, scheme, 100, 0.0000001)

print(plspm_calc.inner_summary())
print(plspm_calc.effects())

