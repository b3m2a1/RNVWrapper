
class Parameter:
    __props__ = None
    __required_props__ = None
    __default_props__ = {}
    def __init__(self, name, **opts):
        opts = self.prep_opts(opts)
        if self.__required_props__ is not None:
            missing_keys = set(self.__required_props__) - opts.keys()
            if len(missing_keys) > 0:
                raise ValueError(
                    "Parameter '{}' requires keys {}".format(
                        name, missing_keys
                    )
                )
        if self.__props__ is not None:
            excess_keys = opts.keys() - set(self.__props__)
            if len(excess_keys) > 0:
                raise ValueError(
                    "For paremeter '{}', unknown keys {}, full set: {}".format(
                        name, excess_keys, self.__props__
                    )
                )
        self.name = name
        self.opts = opts
    def prep_opts(self, opts):
        return dict(self.__default_props__, **opts)
    def as_dict(self):
        return dict(self.opts, name=self.name)
class NamedParameter(Parameter):
    name = None
    def __init__(self, **opts):
        if self.name is None: raise ValueError("{} isn't intended to be instantiated directly")
        super().__init__(self.name, **opts)
class DiversityFilter(NamedParameter):
    name='diversity_filter'
    __props__ = ['nbmax', 'minscore', 'minsimilarity']