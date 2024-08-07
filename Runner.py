"""
A helper class for configuring REINVENT runs in a less manual way
"""

import enum, json, os, datetime, uuid
from .shim import *
from .Parameters import *

__all__ = [
    "Runner",
    'run_job'
]

class RunTypes(enum.Enum):
    reinforcement_learning = 'reinforcement_learning'
    sampling = 'sampling'
    transfer_learning = 'transfer_learning'
    scoring = 'scoring'
    create_model = 'create_model'

class LoggingData:

    __opts__ = (
        'logging_frequency',
        'logging_path',
        'result_folder',
        'job_name',
        'job_id',
        'sender',
        'recipient'
    )
    def __init__(self,
                 *,
                 logging_frequency=10,
                 base_dir=None,
                 output_dir=None,
                 results_folder='results',
                 log_file='progress.log',
                 job_name=None,
                 job_id=None,
                 sender="http://0.0.0.1",
                 recipient="local"
                 ):
        # "sender": "http://0.0.0.1",          # only relevant if "recipient" is set to "remote"
        # "recipient": "local",                # either to local logging or use a remote REST-interface
        # "logging_frequency": 10,             # log every x-th steps
        # "logging_path": os.path.join(output_dir, "progress.log"), # load this folder in tensorboard
        # "result_folder": os.path.join(output_dir, "results"),     # will hold the compounds (SMILES) and summaries
        # "job_name": "Reinforcement learning demo",                # set an arbitrary job name for identification
        # "job_id": "demo"                     # only relevant if "recipient" is set to a specific REST endpoint"

        if job_id is None:
            job_name = 'rnv-{}'.format(str(uuid.uuid4()).replace('-','')[:6])
        if job_name is None:
            job_name = '{}_{}'.format(job_id, datetime.datetime.now().isoformat())
        if base_dir is None:
            base_dir = os.getcwd()
        if output_dir is None:
            output_dir = os.path.join(base_dir, job_name)
        self.opts = dict(
            logging_frequency=logging_frequency,
            logging_path=os.path.join(output_dir, log_file),
            result_folder=os.path.join(output_dir, results_folder),
            job_name=job_name,
            job_id=job_id,
            sender=sender,
            recipient=recipient
        )

class Configuration:
    def __init__(self,
                 *,
                 run_type: RunTypes,
                 version=3.2,
                 **opts
                 ):
        self.run_type = run_type
        self.version = version
        self.log_data = LoggingData(**self.filter_options(opts, LoggingData))

    @classmethod
    def filter_options(cls, opts, obj):
        filter = set(obj.__opts__)
        return {k:opts[k] for k in opts.keys() & filter}

# class RunData:
#     # user_id = "your_id"
#     # reinvent_dir = os.path.expanduser(f"/scratch/user/{user_id}/Reinvent")
#     # reinvent_env = os.path.expanduser(f"/scratch/user/{user_id}/.conda/envs/reinvent")
#     # output_dir = os.path.expanduser(f"/scratch/user/{user_id}/ReinventCommunity/grace_test/pretraining/")
#     def __init__(self, *,
#                  user_id=None,
#                  reinvent_dir=None,
#                  output_dir=None
#                  ):
#         if user_id

class Runner:
    def __init__(self,
                 configuration,
                 results_dir=None
                 ):
        if isinstance(configuration, str):
            configuration = self.load_config(configuration)
        if isinstance(configuration, dict):
            configuration = Configuration(**configuration)
        self.config = configuration
    @classmethod
    def from_parameters(cls, **config):
        return cls(Configuration(**config))

    def load_config(self, path):
        # directly from REINVENT
        with open(path) as f:
            json_input = f.read().replace('\r', '').replace('\n', '')
        try:
            return json.loads(json_input)
        except (ValueError, KeyError, TypeError) as e:
            print(f"JSON format error in file ${path}: \n ${e}")

    default_configuration = 'configs/config.json'
    def run_job(self):
        from running_modes.manager import Manager

        default_config = self.default_configuration
        if not os.path.isfile(default_config):
            default_config = os.path.join(REINVENT_ROOT, default_config)
        base_config = self.load_config(os.path.join(
            REINVENT_ROOT, default_config
        ))

        base_dir = os.path.dirname(self.config.log_data.opts['result_folder'])
        os.makedirs(base_dir, exist_ok=True)

        manager = Manager(base_config, self.config.as_dict())
        manager.run()

def run_job(**config):
    Runner.from_parameters(**config).run_job()

