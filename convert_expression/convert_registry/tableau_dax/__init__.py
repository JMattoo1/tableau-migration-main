from .custom import *
from .standard import *

custom_registry = {
    'IF': [struc_reform_no_shift_node,struc_reform_if_to_switch],
    'ZN': [struc_reform_no_shift_node,struc_reform_zn_to_if_isblank ],
    'FIXED': [struc_reform_no_shift_node, struc_reform_fixed_to_calculate],
    'CASE': [struc_reform_no_shift_node, struc_reform_case_to_switch],
    'TOTAL': [struc_reform_shift_total_to_calculate, struc_reform_total_to_calculate],
    'INDEX': [struc_reform_no_shift_node, struc_reform_index_to_rankx],
}

standard_registry = {
    'aggregation': [struc_reform_no_shift_node, struc_reform_aggregation_exp],
    'undefined': [struc_reform_no_shift_node,struc_reform_undefined_exp],
    'exp': [struc_reform_no_shift_node, struc_reform_expression_exp],
    'logical': [struc_reform_no_shift_node, struc_reform_logical_exp],
    'operators': [struc_reform_no_shift_node, struc_reform_operators_exp],
    'undefined': [struc_reform_no_shift_node, struc_reform_undefined_exp],
    'group': [struc_reform_no_shift_node, struc_reform_group_exp],
    'typeConv': [struc_reform_no_shift_node, struc_reform_typeConv_to_convert_exp],
    'string': [struc_reform_no_shift_node, struc_reform_string_exp],
    'dateTime': [struc_reform_no_shift_node, struc_reform_dateTime_exp],
    'tableCal': [struc_reform_no_shift_node, struc_reform_tableCal_exp],
}

reformImplementExpressions = tuple(reformCusImplementExpressions.union(reformStdImplementExpressions))

reformSafeExpressions = tuple(reformStdSafeExpressions.union(reformCusSafeExpressions))