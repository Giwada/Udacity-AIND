import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    Model selection, that is, the process of choosing a structure
    or an order of a model remains a critical part of any
    signal processing technique
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores       
        
        best_score = float("inf")
        best_model = None  
        for n in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n)
                logL = model.score(self.X, self.lengths)
                
                parameters = n ** 2 + 2 * n * model.n_features - 1
                
                bic = (-2)* logL + np.log(len(self.X)) * parameters
                
                if bic < best_score:
                    best_score = bic
                    best_model = model
                return best_model
            except:
                return self.base_model(self.n_constant)
        return best_model
        

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        # dic_score = log(p(X(i)) - 1/(M - 1)SUM(log(P(X(all but i))
        best_score = float("-inf")
        best_model = None     
        for n in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n)
                dic_arrays = []
                for word, (X, lengths) in self.hwords.items():
                    if word != self.this_word:
                        dic_arrays.append(model.score(X, lengths))
                dic = model.score(self.X, self.lengths) - np.mean(dic_arrays)
                
                if dic > best_score:
                    best_score = dic
                    best_model = model
                return best_model    
            except:
                return self.base_model(self.n_constant)
        return best_model
            

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds
    '''
    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        
        best_score = float("inf")
        best_model = None
        split_method =  KFold(n_splits=2)
        for n in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n)
                logs_array = []        
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    # Get train sequences
                    X_train, lengths_train = combine_sequences(cv_train_idx, self.sequences)
                    # Get test sequences
                    X_test, lengths_test   = combine_sequences(cv_test_idx, self.sequences)
                                                         
                    logL = model.score(X_test, lengths_test)
                    # Add each model score
                    logs_array.append(logL)
                # Calculate mean of all scores    
                mean_score = np.mean(logs_array)
                
                if mean_score < best_score:
                    best_score = mean_score
                    best_model = model
                return best_model
            except:
                return self.base_model(self.n_constant)
        return best_model
