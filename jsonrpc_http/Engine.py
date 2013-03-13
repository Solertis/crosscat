import inspect
import sys
from collections import Counter
#
import numpy
#
import tabular_predDB.cython.State as State


class Engine(object):

    def __init__(self):
        self.seed = 0

    def get_next_seed(self):
        SEED = self.seed
        self.seed += 1
        return SEED

    def initialize(self, M_c, M_r, T, initialization=None):
        # FIXME: why is M_r passed?
        p_State = State.p_State(M_c, T, initialization=initialization)
        X_L = p_State.get_X_L()
        X_D = p_State.get_X_D()
        return M_c, M_r, X_L, X_D

    def analyze(self, M_c, T, X_L, X_D, kernel_list, n_steps, c, r,
                max_iterations, max_time):
        p_State = State.p_State(M_c, T, X_L, X_D)
        # FIXME: actually pay attention to kernerl_list, max_time, etc
        for idx in range(n_steps):
            p_State.transition()
        #
        X_L_prime = p_State.get_X_L()
        X_D_prime = p_State.get_X_D()
        return X_L_prime, X_D_prime

    def simple_predictive_sample(self, M_c, X_L, X_D, Y, q):
        x = []
        # FIXME: handle multiple queries
        assert(len(q)==1)
        for query in q:
            which_row = query[0]
            which_column = query[1]
            #
            num_rows = len(X_D[0])
            num_cols = len(M_c['column_metadata'])
            is_observed_row = which_row < num_rows
            is_observed_col = which_column < num_cols
            assert(is_observed_col)
            # FIXME: handle unobserved rows
            assert(is_observed_row)
            if is_observed_col and is_observed_row:
                SEED = self.get_next_seed()
                sample = simple_predictive_sample_observed(M_c, X_L, X_D,
                                                           which_row,
                                                           which_column,
                                                           SEED)
                x.append(sample)
            elif is_observed_col and not is_observed_row:
                SEED = self.get_next_seed()
                sample = simple_predictive_sample_unobserved(M_c, X_L, X_D,
                                                             Y,
                                                             which_column,
                                                             SEED)
                x.append(sample)
            else:
                # FIXME: not handling unobserved columns for now
                assert(False)
        return x

    def simple_predictive_probability(self, M_c, X_L, X_D, Y, Q, n):
        p = None
        return p

    def impute(self, M_c, X_L, X_D, Y, q, n):
        # FIXME: actually implement 
        # FIXME: just spitting out random normals for now 
        SEED = self.get_next_seed()
        random_state = numpy.random.RandomState(SEED)
        #
        e = random_state.normal(size=len(q)).tolist()
        return e

    def conditional_entropy(M_c, X_L, X_D, d_given, d_target,
                            n=None, max_time=None):
        e = None
        return e

    def predictively_related(self, M_c, X_L, X_D, d,
                                           n=None, max_time=None):
        m = []
        return m

    def contextual_structural_similarity(self, X_D, r, d):
        s = []
        return s

    def structural_similarity(self, X_D, r):
        s = []
        return s

    def structural_anomalousness_columns(self, X_D):
        a = []
        return a

    def structural_anomalousness_rows(self, X_D):
        a = []
        return a

    def predictive_anomalousness(self, M_c, X_L, X_D, T, q, n):
        a = []
        return a

# helper functions
get_name = lambda x: getattr(x, '__name__')
get_Engine_attr = lambda x: getattr(Engine, x)
is_Engine_method_name = lambda x: inspect.ismethod(get_Engine_attr(x))
#
def get_method_names():
    return filter(is_Engine_method_name, dir(Engine))
#
def get_method_name_to_args():
    method_names = get_method_names()
    method_name_to_args = dict()
    for method_name in method_names:
        method = Engine.__dict__[method_name]
        arg_str_list = inspect.getargspec(method).args[1:]
        method_name_to_args[method_name] = arg_str_list
    return method_name_to_args
