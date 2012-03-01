#Copyright (C) 2011 Robert Lanfear and Brett Calcott
#
#This program is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the
#Free Software Foundation, either version 3 of the License, or (at your
#option) any later version.
#
#This program is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#General Public License for more details. You should have received a copy
#of the GNU General Public License along with this program.  If not, see
#<http://www.gnu.org/licenses/>. PartitionFinder also includes the PhyML
#program and the PyParsing library both of which are protected by their
#own licenses and conditions, using PartitionFinder implies that you
#agree with those licences and conditions as well.

import logging
log = logging.getLogger("subset")
import os
import weakref
import cPickle as pickle

import alignment
import phyml_models

from math import log as logarithm

from util import PartitionFinderError
class SubsetError(PartitionFinderError):
    pass

class Subset(object):
    """A Subset of Partitions
    """

    # TODO: changes this to AllSubsets?
    _cache = weakref.WeakValueDictionary()

    # Return the SAME subset if the partitions are identical
    # This is basically a pythonized factory
    # See here: http://codesnipers.com/?q=python-flyweights
    def __new__(cls, *parts):
        cacheid = frozenset(parts)
        obj = Subset._cache.get(cacheid, None)
        if not obj:
            obj = object.__new__(cls)
            Subset._cache[cacheid] = obj

            # Error checking....
            tempparts = set()
            for p in parts:
                if p.partition_set is None:
                    log.error("You cannot add a Partition to a Subset until "
                              "the Partition belongs to a PartitionSet")
                    raise SubsetError

                if p in tempparts:
                    log.error("%s is duplicated in a Subset", p)
                    raise SubsetError

                tempparts.add(p)

            obj.partitions = cacheid
            
            # a list of columns in the subset
            obj.columns = []
            obj.columnset = set()
            for p in parts:
                obj.columns += p.columns
                obj.columnset |= p.columnset
            obj.columns.sort()

            obj.results = {}
            obj.best_info_score = None #e.g. AIC, BIC, AICc
            obj.best_model = None
            obj.best_params = None
            obj.best_lnl = None
            obj.alignment_path = None
            log.debug("Created %s", obj)
        # else:
            # log.debug("Reused %s", obj)

        return obj

    # def __init__(self, *parts):
        # Everything is relegated to above...

    def __str__(self):
        return "Subset(%s)" % ", ".join([str(p) for p in self.partitions])

    @property
    def name(self):
        # Cache this
        if hasattr(self, '_name'):
            nm = self._name
        else:
            s = sorted([p.name for p in self.partitions])
            nm = '-'.join(s)
            # Don't go crazy
            if len(nm) > 50:
                s = sorted([str(p.sequence) for p in self.partitions])
            nm = '-'.join(s)
            self._name = nm

        return nm

    def __iter__(self):
        return iter(self.partitions)

    def add_model_result(self, model, result):
        result.model = model
        result.params = phyml_models.get_num_params(model)

        K = float(result.params)
        n = float(len(self.columnset))
        lnL = float(result.lnl)		   
        result.aic  = (-2.0*lnL) + (2.0*K)
        result.bic  = (-2.0*lnL) + (K * logarithm(n))
        result.aicc = result.aic + (((2.0*K)*(K+1.0))/(n-K-1.0))

        log.debug("Adding model to subset. Model: %s, params %d" %(model, K))

        if model in self.results:
            log.error("Can't add model result %s, it already exists in %s",
                    model, self)
        self.results[model] = result

    def model_selection(self, method, models):
        #model selection is done after we've added all the models
        self.best_info_score = None #reset this before model selection

        for model in models:
            result=self.results[model]
            if method=="AIC" or method=="aic":
                info_score = result.aic
            elif method=="AICc" or method=="AICC" or method=="aicc":
                info_score = result.aicc
            elif method=="BIC" or method=="bic":
                info_score = result.bic
            else:
                log.error("Model selection option %s not recognised, please check", method)
                raise SubsetError
		
            if self.best_info_score is None or info_score < self.best_info_score:
                self.best_lnl = result.lnl
                self.best_info_score = info_score
                self.best_model = result.model
                self.best_params = result.params
        log.debug("Model Selection. best model: %s, params: %d" %(self.best_model, self.best_params))


    _template = "%-15s | %-15s | %-15s | %-15s | %-15s\n"
    def write_summary(self, path):
        # Sort everything
        model_results = [(r.bic, r) for r in self.results.values()]
        model_results.sort()
        f = open(path, 'w')
        f.write("Model selection results for subset: %s\n" % self.name)
        f.write("Subset alignment stored here: %s\n" % self.alignment_path)
        f.write("Models are organised according to their BIC scores\n\n")
        f.write(Subset._template % ("Model", "lNL", "AIC", "AICc", "BIC"))
        for bic, r in model_results:
            f.write(Subset._template % (r.model, r.lnl, r.aic, r.aicc, r.bic))

    
    # These are the fields that get stored for quick loading
    _store = "alignment_path best_lnl best_info_score best_model best_params results".split()

    def write_binary_summary(self, path):
        """Write out the results we've collected to a binary file"""
        f = open(path, 'wb')
        store = dict([(x, getattr(self, x)) for x in Subset._store])
        pickle.dump(store, f, -1)

    def read_binary_summary(self, path):
        if not os.path.exists(path):
            return False

        log.debug("Reading binary cached results for %s", self)
        f = open(path, 'rb')
        self.__dict__.update(pickle.load(f))
