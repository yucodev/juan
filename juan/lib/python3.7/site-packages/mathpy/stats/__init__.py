from __future__ import absolute_import

from .aov import anova_oneway, manova_oneway
from .fa import fa
from .hypothesis import ttest, mann_whitney, degrees_of_freedom
from .simulate import simulate_corr_matrix, add_noise
from .summary import corr, covar, pearson, spearman, var, var_cond
