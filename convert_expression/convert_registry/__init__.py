from .tableau_dax import custom_registry as td_cust_reg, standard_registry as td_stand_reg, reformImplementExpressions as td_imple_exp, reformSafeExpressions as td_safe_exp

registry: dict[str,dict] = {
    'tableau_dax': [td_stand_reg, td_cust_reg, td_imple_exp, td_safe_exp]
}