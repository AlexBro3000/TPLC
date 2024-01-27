import Lexer.Lexer as Lexer
import Parser.Term as Term


class Semantic:
    def __init__(self, result_parsing):
        self.data = result_parsing.data

    @property
    def semantic(self):
        layer = 0

        analysis_result = []
        dlt_code = []
        semantic = {
            "const": {
                "var": [
                    {"layer": 0,
                     "identifier": "true",
                     "type": "bool",
                     "using": True},
                    {"layer": 0,
                     "identifier": "false",
                     "type": "bool",
                     "using": True}
                ],
                "func": [
                    {"layer": 0,
                     "identifier": "Print",
                     "type": None,
                     "code": []},
                    {"layer": 0,
                     "identifier": "Println",
                     "type": None,
                     "code": []}
                ]
            },
            "var": {
                "var": [], "func": []
            }
        }

        for i, elem in enumerate(self.data[1:]):
            elem = elem.data[0]

            match type(elem):
                case Term.ConstDecl | Term.VarDecl:
                    del_code, analysis = declaration(elem, semantic, i + 1, layer)

                    analysis_result.extend(analysis)
                    dlt_code.extend(del_code)
                case Term.FunctionDecl:
                    vrbl = {
                        "index": i + 1,
                        "layer": layer,
                        "identifier": elem.data[0].token,
                        "param": [],
                        "type": None,
                        "code": elem.data[2].data
                    }
                    # Проверка на переопределение значений по умолчанию
                    if (
                            is_to_array(vrbl, semantic['const']['var'], layer) or
                            is_to_array(vrbl, semantic['const']['func'], layer)
                    ):
                        analysis_result.append(
                            {"type": "E", "message": "Redeclaring a function", "identifier": vrbl['identifier']}
                        )
                        dlt_code.append(vrbl['index'])
                        continue
                    # Проверка на соответствие типов
                    if len(elem.data[1].data) == 4:
                        vrbl_params = get_param(elem.data[1].data[1].data, semantic, layer + 1)
                        vrbl_type = get_type(elem.data[1].data[3].data)
                    else:
                        vrbl_params = []
                        vrbl_type = None
                        if len(elem.data[1].data) == 0:
                            pass
                        elif elem.data[1].data[0] == 1:
                            vrbl_params = get_param(elem.data[1].data[1].data, semantic, layer + 1)
                        elif elem.data[1].data[0] == 2:
                            vrbl_type = get_type(elem.data[1].data[1].data)
                    if vrbl_params:
                        if len(vrbl_params[0]) != 0:
                            analysis_result.extend(vrbl_params[0])
                            dlt_code.append(vrbl['index'])
                            continue
                        else:
                            vrbl_params = vrbl_params[1]
                    if vrbl_type is not None and vrbl_type == "NULL":
                        analysis_result.append(
                            {"type": "E",
                             "message": "The function returns unknown type",
                             "identifier": vrbl['identifier']}
                        )
                        dlt_code.append(vrbl['index'])
                        continue
                    vrbl['param'] = vrbl_params
                    vrbl['type'] = vrbl_type
                    # Проверка на переопределение
                    if (
                            is_to_array(vrbl, semantic['var']['var'], layer) or
                            is_to_array(vrbl, semantic['var']['func'], layer)
                    ):
                        if is_to_array(vrbl, semantic['var']['var'], layer):
                            vrbl_tmp = get_to_array(vrbl, semantic['var']['var'], layer)
                            if vrbl_tmp['using']:
                                analysis_result.append(
                                    {"type": "W", "message": "Redeclaring a function", "identifier": vrbl['identifier']}
                                )
                                semantic['var']['var'].remove(vrbl_tmp)
                            else:
                                analysis_result.append(
                                    {"type": "E", "message": "Redeclaring a function", "identifier": vrbl['identifier']}
                                )
                                dlt_code.append(vrbl['index'])
                                continue
                        else:
                            analysis_result.append(
                                {"type": "E", "message": "Redeclaring a function", "identifier": vrbl['identifier']}
                            )
                            dlt_code.append(vrbl['index'])
                            continue
                    semantic['var']['func'].append(vrbl)

        dlt_code = sorted(list(set(dlt_code)))
        for i in range(len(dlt_code) - 1, -1, -1):
            del self.data[dlt_code[i]]

        for i, func in enumerate(semantic['var']['func']):
            analysis_result.extend(func_block(func, semantic, layer + 1))

        return analysis_result


def get_param(code, semantic, layer):
    analysis_result = []
    params_result = []

    for params in code:
        params_type = get_type(params.data[1].data)

        for param in params.data[0].data:
            vrbl = {
                "layer": layer,
                "identifier": param.token,
                "type": params_type,
                "using": True
            }
            # Проверка на переопределение значений по умолчанию
            if (
                    is_to_array(vrbl, semantic['const']['var'], layer) or
                    is_to_array(vrbl, semantic['const']['func'], layer)
            ):
                analysis_result.append(
                    {"type": "E",
                     "message": "Redeclaring a variable in function parameters",
                     "identifier": vrbl['identifier']}
                )
                break
            # Проверка на переопределение
            if is_to_array(vrbl, params_result, layer):
                analysis_result.append(
                    {"type": "E",
                     "message": "Redeclaring a variable in function parameters",
                     "identifier": vrbl['identifier']}
                )
                break
            params_result.append(vrbl)
    return analysis_result, params_result


def get_type(code):
    if isinstance(code[0], Lexer.Token):
        match code[0].token:
            case "int":
                return "int"
            case "float64":
                return "float"
            case "string":
                return "string"
            case "bool":
                return "bool"
    else:
        match code[0].data[-1].token:
            case "int":
                return "int"
            case "float64":
                return "float"
            case "string":
                return "string"
            case "bool":
                return "bool"
    return "NULL"


def get_type_list(type_list):
    type_list = list(set(type_list))
    if len(type_list) > 1:
        if "NONE" in type_list:
            return "NONE"
        else:
            return "NULL"
    else:
        if len(type_list) == 1:
            return type_list[0]
        return "NULL"


def get_type_expression(code, semantic, layer):
    type_tmp = []
    for i, elem in enumerate(code):
        if isinstance(elem, Lexer.Token):
            match elem.code:
                case "identifier":
                    vrbl = {"identifier": elem.token}
                    if is_to_array(vrbl, semantic['const']['var'], layer):
                        elem_semantic = get_to_array(vrbl, semantic['const']['var'], layer)
                        elem_semantic['using'] = True
                        type_tmp.append(elem_semantic['type'])
                        continue
                    if is_to_array(vrbl, semantic['var']['var'], layer):
                        elem_semantic = get_to_array(vrbl, semantic['var']['var'], layer)
                        elem_semantic['using'] = True
                        type_tmp.append(elem_semantic['type'])
                        continue
                    type_tmp.append('NONE')
                case "int_lit":
                    type_tmp.append("int")
                    continue
                case "float_lit":
                    type_tmp.append("float")
                    continue
                case "string_lit":
                    type_tmp.append("string")
                    continue
        else:
            if isinstance(elem, str):
                continue
            if isinstance(elem, Term.Operand):
                type_tmp.extend(get_type_operand(elem.data, semantic, layer))
                continue
            if isinstance(elem, Term.UnaryExpr):
                type_tmp.extend(get_type_unary_expr(elem.data, semantic, layer))
                continue
            if isinstance(elem, Term.PrimaryExpr):
                type_tmp.extend(get_type_primary_expr(elem.data, semantic, layer))
                continue
    return type_tmp


def get_type_operand(code, semantic, layer):
    type_tmp = None
    code = code[1]

    if isinstance(code, Term.Expression):
        type_tmp = get_type_expression(code.data, semantic, layer)
    if isinstance(code, Term.Operand):
        type_tmp = get_type_operand(code.data, semantic, layer)
    if isinstance(code, Term.PrimaryExpr):
        type_tmp = get_type_primary_expr(code.data, semantic, layer)
    if isinstance(code, Term.UnaryExpr):
        type_tmp = get_type_unary_expr(code.data, semantic, layer)
    if isinstance(code, Lexer.Token):
        match code.code:
            case "identifier":
                vrbl = {"identifier": code.token}
                if is_to_array(vrbl, semantic['const']['var'], layer):
                    type_tmp = get_to_array(vrbl, semantic['const']['var'], layer)
                    if type_tmp is None:
                        type_tmp = "NULL"
                    else:
                        type_tmp['using'] = True
                        type_tmp = [type_tmp['type']]
                elif is_to_array(vrbl, semantic['var']['var'], layer):
                    type_tmp = get_to_array(vrbl, semantic['var']['var'], layer)
                    if type_tmp is None:
                        type_tmp = "NULL"
                    else:
                        type_tmp['using'] = True
                        type_tmp = [type_tmp['type']]
                else:
                    type_tmp = "NONE"
            case "int_lit":
                type_tmp = ["int"]
            case "float_lit":
                type_tmp = ["float"]
            case "string_lit":
                type_tmp = ["string"]
    return type_tmp


def get_type_primary_expr(code, semantic, layer):
    type_tmp = []

    code_tmp = None
    i = 1
    while True:
        if len(code) <= i:
            break
        match code[i]:
            case "dot":
                code_tmp = "N"
                i += 2
            case "lsbr":
                if code_tmp is None:
                    code_tmp = "A"
                elif code_tmp != "A":
                    code_tmp = "N"
                i += 3
            case "lbr":
                if code_tmp is None:
                    code_tmp = "F"
                elif code_tmp != "F":
                    code_tmp = "N"
                if code[i + 1] == "rbr":
                    i += 2
                else:
                    i += 3

    if code_tmp == "A" and isinstance(code[0], Lexer.Token):
        if is_to_array({"identifier": code[0].token}, semantic['const']['var'], layer):
            elem_semantic = get_to_array({"identifier": code[0].token}, semantic['const']['var'], layer)
        else:
            elem_semantic = get_to_array({"identifier": code[0].token}, semantic['var']['var'], layer)
        if elem_semantic is None:
            type_tmp = ["NULL"]
        else:
            elem_semantic['using'] = True
            if elem_semantic['type'] is None:
                type_tmp = ["NULL"]
            else:
                type_tmp = [elem_semantic['type']]

    if code_tmp == "F" and isinstance(code[0], Lexer.Token):
        if is_to_array({"identifier": code[0].token}, semantic['const']['func'], layer):
            elem_semantic = get_to_array({"identifier": code[0].token}, semantic['const']['func'], layer)
        else:
            elem_semantic = get_to_array({"identifier": code[0].token}, semantic['var']['func'], layer)
        if elem_semantic is None:
            type_tmp = ["NONE"]
        elif elem_semantic['type'] is None:
            type_tmp = ["NULL"]
        else:
            if isinstance(code[2], Term.ExpressionList):
                for it in code[2].data:
                    tmp = get_type_list(get_type_expression(it.data, semantic, layer))
                    if tmp == "NULL" or tmp == "NONE":
                        type_tmp = [tmp]
                        break
            if not type_tmp:
                type_tmp = [elem_semantic['type']]

    return type_tmp


def get_type_unary_expr(code, semantic, layer):
    type_tmp = ["NULL"]
    code = code[-1]

    if isinstance(code, Term.Expression):
        type_tmp = get_type_expression(code.data, semantic, layer)
    if isinstance(code, Term.Operand):
        type_tmp = get_type_operand(code.data, semantic, layer)
    if isinstance(code, Term.PrimaryExpr):
        type_tmp = get_type_primary_expr(code.data, semantic, layer)
    if isinstance(code, Term.UnaryExpr):
        type_tmp = get_type_unary_expr(code.data, semantic, layer)
    if isinstance(code, Lexer.Token):
        match code.code:
            case "identifier":
                vrbl = {"identifier": code.token}
                if is_to_array(vrbl, semantic['const']['var'], layer):
                    type_tmp = get_to_array(vrbl, semantic['const']['var'], layer)
                    if type_tmp is None:
                        type_tmp = "NULL"
                    else:
                        type_tmp['using'] = True
                        type_tmp = [type_tmp['type']]
                if is_to_array(vrbl, semantic['var']['var'], layer):
                    type_tmp = get_to_array(vrbl, semantic['var']['var'], layer)
                    if type_tmp is None:
                        type_tmp = "NULL"
                    else:
                        type_tmp['using'] = True
                        type_tmp = [type_tmp['type']]
                else:
                    type_tmp = "NONE"
            case "int_lit":
                type_tmp = ["int"]
            case "float_lit":
                type_tmp = ["float"]
            case "string_lit":
                type_tmp = ["string"]
    return type_tmp


def get_to_array(elem, array, layer):
    elem_arr = None
    for elem_array in array:
        if elem_array['identifier'] == elem['identifier'] and layer >= elem_array['layer']:
            if elem_arr is None:
                elem_arr = elem_array
            elif elem_array['layer'] > elem_arr['layer']:
                elem_arr = elem_array
    return elem_arr


def is_to_array(elem, array, layer):
    elem_arr = None
    for elem_array in array:
        if elem_array['identifier'] == elem['identifier'] and layer >= elem_array['layer']:
            if elem_arr is None:
                elem_arr = elem_array
            elif elem_array['layer'] > elem_arr['layer']:
                elem_arr = elem_array
    if elem_arr is not None:
        return True
    return False


def is_type(vrbl_type_1, vrbl_type_2):
    if vrbl_type_1 is None:
        return True
    if vrbl_type_1 == vrbl_type_2:
        return True
    return False


def clear_semantic_var(semantic, layer):
    for i in range(len(semantic['var']['var']) - 1, -1, -1):
        elem = semantic['var']['var'][i]
        if elem['layer'] >= layer:
            semantic['var']['var'].pop(i)


def declaration(code, semantic, index, layer):
    analysis_result = []

    vrbl = {
        "index": index,
        "layer": layer,
        "identifier": code.data[0].token,
        "type": "NULL",
        "using": False
    }

    # Проверка на переопределение значений по умолчанию
    if is_to_array(vrbl, semantic['const']['var'], layer) or is_to_array(vrbl, semantic['const']['func'], layer):
        return [index], [{
            "type": "E", "message": "Redeclaring a variable", "identifier": vrbl['identifier']
        }]

    # Проверка на соответствие типов
    if len(code.data) == 3:
        vrbl_type_1 = get_type(code.data[1].data)
        vrbl_type_2 = get_type_list(get_type_expression(code.data[2].data, semantic, layer))
    else:
        vrbl_type_1 = None
        vrbl_type_2 = get_type_list(get_type_expression(code.data[1].data, semantic, layer))
    if vrbl_type_1 == "NULL" or vrbl_type_2 == "NULL":
        return [index], [{
            "type": "E", "message": "Expression contains multiple types", "identifier": vrbl['identifier']
        }]
    if vrbl_type_1 == "NONE" or vrbl_type_2 == "NONE":
        return [index], [{
            "type": "E", "message": "Unknown variable", "identifier": vrbl['identifier']
        }]
    if not is_type(vrbl_type_1, vrbl_type_2):
        return [index], [{
            "type": "E",
            "message": "Type mismatch: " + vrbl_type_1 + " / " + vrbl_type_2,
            "identifier": vrbl['identifier']
        }]
    vrbl['type'] = vrbl_type_2

    # Проверка на переопределение
    if is_to_array(vrbl, semantic['var']['var'], layer) or is_to_array(vrbl, semantic['var']['func'], layer):
        if is_to_array(vrbl, semantic['var']['var'], layer):
            vrbl_tmp = get_to_array(vrbl, semantic['var']['var'], layer)
            if vrbl_tmp['using']:
                semantic['var']['var'].remove(vrbl_tmp)
                analysis_result.append({
                    "type": "W", "message": "Redeclaring a variable", "identifier": vrbl['identifier']
                })
            else:
                index, vrbl_tmp['index'] = vrbl_tmp['index'], index
                return [index], [{
                    "type": "E", "message": "Redeclaring a variable", "identifier": vrbl['identifier']
                }]
        else:
            return [index], [{
                "type": "E", "message": "Redeclaring a variable", "identifier": vrbl['identifier']
            }]
    semantic['var']['var'].append(vrbl)
    return [], analysis_result


def block(code, name, func_type, semantic, layer, layer_block):
    analysis_result = []
    del_code = []
    for i, elem in enumerate(code[:]):
        elem = elem.data
        match type(elem[0]):
            case Term.ConstDecl | Term.VarDecl:
                analysis = declaration(elem[0], semantic, i, layer)
                del_code.extend(analysis[0])
                analysis_result.extend(analysis[1])
            case Term.SimpleStmt:
                if len(elem[0].data) == 1:
                    vrbl_type = get_type_list(get_type_expression(elem[0].data[0].data, semantic, layer))
                    if vrbl_type == "NONE":
                        analysis_result.append({
                            "type": "E", "message": "Unknown variable / function", "identifier": name
                        })
                        del_code.append(i)
                        continue
                else:
                    elem_l = elem[0].data[0].data
                    if not isinstance(elem_l[0], Lexer.Token):
                        analysis_result.append({
                            "type": "E", "message": "Not identifier", "identifier": name
                        })
                        del_code.append(i)
                        continue
                    if len(elem[0].data) == 2:
                        if isinstance(elem[0].data[1], Lexer.Token):
                            vrbl_type = get_type_list(get_type_expression(elem_l, semantic, layer))
                            if vrbl_type == "NULL" or vrbl_type == "NONE":
                                if vrbl_type == "NULL":
                                    analysis_result.append({
                                        "type": "E", "message": "Expression contains multiple types",
                                        "identifier": name
                                    })
                                    del_code.append(i)
                                    continue
                                else:
                                    analysis_result.append({
                                        "type": "E", "message": "Unknown variable",
                                        "identifier": name
                                    })
                                    del_code.append(i)
                                    continue
                        else:
                            elem_r = elem[0].data[1].data
                            vrbl = {
                                "index": i, "layer": layer, "identifier": elem_l[0].token,
                                "type": "NULL", "using": False
                            }
                            # Проверка на переопределение значений по умолчанию
                            if (
                                    is_to_array(vrbl, semantic['const']['var'], layer) or
                                    is_to_array(vrbl, semantic['const']['func'], layer)
                            ):
                                analysis_result.append({
                                    "type": "E", "message": "Redeclaring a variable", "identifier": name
                                })
                                del_code.append(i)
                                continue
                            # Проверка на соответствие типов
                            vrbl_type = get_type_list(get_type_expression(elem_r, semantic, layer))
                            if vrbl_type == "NULL" or vrbl_type == "NONE":
                                if vrbl_type == "NULL":
                                    analysis_result.append({
                                        "type": "E", "message": "Expression contains multiple types",
                                        "identifier": name
                                    })
                                    del_code.append(i)
                                    continue
                                else:
                                    analysis_result.append({
                                        "type": "E", "message": "Unknown variable",
                                        "identifier": name
                                    })
                                    del_code.append(i)
                                    continue
                            vrbl['type'] = vrbl_type
                            # Проверка на переопределение
                            if (
                                    is_to_array(vrbl, semantic['var']['var'], layer) or
                                    is_to_array(vrbl, semantic['var']['func'], layer)
                            ):
                                if is_to_array(vrbl, semantic['var']['var'], layer):
                                    vrbl_tmp = get_to_array(vrbl, semantic['var']['var'], layer)
                                    if vrbl_tmp['using']:
                                        semantic['var']['var'].remove(vrbl_tmp)
                                        analysis_result.append({
                                            "type": "W", "message": "Redeclaring a variable",
                                            "identifier": name
                                        })
                                    else:
                                        analysis_result.append({
                                            "type": "E", "message": "Redeclaring a variable",
                                            "identifier": name
                                        })
                                        del_code.append(vrbl_tmp['index'])
                                        vrbl_tmp['index'] = i
                                        continue
                                else:
                                    analysis_result.append({
                                        "type": "E", "message": "Redeclaring a variable", "identifier": name
                                    })
                                    del_code.append(i)
                                    continue
                            semantic['var']['var'].append(vrbl)
                    if len(elem[0].data) == 3:
                        elem_r = elem[0].data[2].data
                        vrbl_type_left = get_type_list(get_type_expression(elem_l, semantic, layer))
                        vrbl_type_right = get_type_list(get_type_expression(elem_r, semantic, layer))
                        if vrbl_type_left == "NULL" or vrbl_type_right == "NULL":
                            analysis_result.append({
                                "type": "E", "message": "Expression contains multiple types",
                                "identifier": name
                            })
                            del_code.append(i)
                            continue
                        if vrbl_type_left == "NONE" or vrbl_type_right == "NONE":
                            analysis_result.append({
                                "type": "E", "message": "Unknown variable",
                                "identifier": name
                            })
                            del_code.append(i)
                            continue
                        if not is_type(vrbl_type_left, vrbl_type_right):
                            analysis_result.append({
                                "type": "E", "message": "Type mismatch: " + vrbl_type_left + " / " + vrbl_type_right,
                                "identifier": name
                            })
                            del_code.append(i)
                            continue
            case Term.IfStmt:
                flag, analysis = if_block(elem[0], name, func_type, semantic, layer + 1)
                if not flag:
                    del_code.append(i)
                analysis_result.extend(analysis)
                continue
            case Term.SwitchStmt:
                flag, analysis = switch_block(elem[0], name, func_type, semantic, layer + 1)
                if not flag:
                    del_code.append(i)
                analysis_result.extend(analysis)
                continue
            case Term.ForStmt:
                flag, analysis = for_block(elem[0], name, func_type, semantic, layer + 1)
                if not flag:
                    del_code.append(i)
                analysis_result.extend(analysis)
                continue
            case _:
                if isinstance(elem[0], str):
                    match elem[0]:
                        case "Continue":
                            if layer_block != "cycle":
                                analysis_result.append({
                                    "type": "E", "message": "Continue is not in loop", "identifier": name
                                })
                                del_code.append(i)
                                continue
                        case "Break":
                            if layer_block != "cycle" and layer_block != "branching":
                                analysis_result.append({
                                    "type": "E", "message": "Break is not in loop or switch", "identifier": name
                                })
                                del_code.append(i)
                                continue
                        case "Return":
                            if func_type is None:
                                if len(elem) > 1:
                                    analysis_result.append({
                                        "type": "E", "message": "None return value", "identifier": name
                                    })
                                    del_code.append(i)
                                    continue
                            else:
                                if len(elem) == 1:
                                    analysis_result.append({
                                        "type": "E", "message": "Not return value", "identifier": name
                                    })
                                    del_code.append(i)
                                    continue
                                else:
                                    vrbl_type = get_type_list(get_type_expression(elem[1].data, semantic, layer))

                                    if vrbl_type == "NULL" or vrbl_type == "NONE":
                                        if vrbl_type == "NULL":
                                            analysis_result.append({
                                                "type": "E", "message": "Expression contains multiple types in return",
                                                "identifier": name
                                            })
                                        else:
                                            analysis_result.append({
                                                "type": "E", "message": "Unknown variable in return",
                                                "identifier": name
                                            })
                                        del_code.append(i)
                                        continue
                                    if not is_type(func_type, vrbl_type):
                                        analysis_result.append({
                                            "type": "E", "message": "Type mismatch: " + func_type + " / " + vrbl_type,
                                            "identifier": name
                                        })
                                        del_code.append(i)
                                        continue

    del_code = sorted(list(set(del_code)))
    for i in range(len(del_code) - 1, -1, -1):
        del code[del_code[i]]

    clear_semantic_var(semantic, layer)
    return analysis_result, del_code


def func_block(func, semantic, layer):
    semantic['var']['var'].extend(func['param'])
    analysis_result, _ = block(func["code"], func['identifier'], func['type'], semantic, layer, "block")
    clear_semantic_var(semantic, layer)
    return analysis_result


def if_block(code, name, func_type, semantic, layer):
    analysis_result = []

    dlt_code = []
    stp = 0
    while True:
        index = stp + 1
        while index < len(code.data) and not isinstance(code.data[index], str):
            index += 1
        vrbl_type = get_type_list(get_type_expression(code.data[stp].data, semantic, layer))
        if vrbl_type == "NULL" or vrbl_type == "NONE":
            if vrbl_type == "NULL":
                analysis_result.append({
                    "type": "W", "message": "Expression contains multiple types",
                    "identifier": name + " if"
                })
            else:
                analysis_result.append({
                    "type": "E", "message": "Unknown variable",
                    "identifier": name + " if"
                })
                dlt_code.extend(list(range(stp - 1, index)))

                if index < len(code.data):
                    if code.data[index] == "elif":
                        if stp == 0 or stp - 2 in dlt_code:
                            dlt_code.append(index)
                        stp = index + 1
                        continue
                    else:
                        stp = index
                        while index < len(code.data):
                            index += 1
                        dlt_code.extend(list(range(stp, index)))
                        break
                else:
                    break
        analysis = block(code.data[stp + 1:index], name + " if", func_type, semantic, layer, "condition")
        for it in analysis[0]:
            analysis_result.append(it)
        for it in analysis[1]:
            dlt_code.append(it + stp + 1)
        clear_semantic_var(semantic, layer)
        stp = index
        if len(code.data) > stp:
            if code.data[stp] == "elif":
                stp += 1
                continue
            else:
                analysis = block(code.data[stp + 1:], name + " if", func_type, semantic, layer, "condition")
                for it in analysis[0]:
                    analysis_result.append(it)
                for it in analysis[1]:
                    dlt_code.append(it + stp + 1)
                break
        else:
            break
    dlt_code = sorted(list(set(dlt_code)))
    for i in range(len(dlt_code) - 1, -1, -1):
        if dlt_code[i] >= 0:
            del code.data[dlt_code[i]]

    if len(code.data):
        return True, analysis_result
    return False, analysis_result


def switch_block(code, name, func_type, semantic, layer):
    analysis_result = []
    dlt_code = []

    vrbl_type = get_type_list(get_type_expression(code.data[0].data, semantic, layer))
    if vrbl_type == "NULL" or vrbl_type == "NONE":
        if vrbl_type == "NULL":
            analysis_result.append(
                {"type": "W", "message": "Expression contains multiple types", "identifier": name + " switch"})
        else:
            return False, [{"type": "E", "message": "Unknown variable", "identifier": name + " switch"}]
    for i, expr_case in enumerate(code.data[1:]):
        if expr_case.data[0] == "case":
            dlt_expr = []
            for j, expr in enumerate(expr_case.data[1].data):
                vrbl_type_expr = get_type_list(get_type_expression(expr.data, semantic, layer))
                if vrbl_type_expr == "NONE":
                    analysis_result.append({"type": "E", "message": "Unknown variable", "identifier": name + " switch"})
                    dlt_expr.append(j)
                    continue
                if not is_type(vrbl_type, vrbl_type_expr):
                    analysis_result.append({
                        "type": "E", "message": "Type mismatch: " + vrbl_type + " / " + vrbl_type_expr,
                        "identifier": name + " switch"
                    })
                    dlt_expr.append(j)
                    continue

            dlt_expr = sorted(list(set(dlt_expr)))
            for j in range(len(dlt_expr) - 1, -1, -1):
                if dlt_expr[j] >= 0:
                    del expr_case.data[1].data[dlt_expr[j]]

            if len(expr_case.data[1].data) == 0:
                dlt_code.append(i + 1)
                continue
        else:
            pass

        analysis, _ = block(expr_case.data[-1].data, name + " switch", func_type, semantic, layer, "branching")
        analysis_result.extend(analysis)
        clear_semantic_var(semantic, layer)

        if len(expr_case.data[-1].data) == 0:
            dlt_code.append(i + 1)
            continue

    dlt_code = sorted(list(set(dlt_code)))
    for i in range(len(dlt_code) - 1, -1, -1):
        if dlt_code[i] >= 0:
            del code.data[dlt_code[i]]

    if len(code.data) > 1:
        return True, analysis_result
    return False, analysis_result


def for_block(code, name, func_type, semantic, layer):
    analysis_result = []

    stp = 0
    if code.data[0] == "for":
        if len(code.data[1].data) == 2:
            elem_l = code.data[1].data[0]
            elem_r = code.data[1].data[1]
            if not isinstance(elem_l.data[0], Lexer.Token):
                return False, [{"type": "E", "message": "Not identifier", "identifier": name + " for"}]
            if isinstance(elem_r, Lexer.Token):
                return False, [{"type": "E", "message": "The first element is the counter declaration",
                                "identifier": name + " for"}]
            elem_l = elem_l.data
            elem_r = elem_r.data

            vrbl = {
                "index": 0, "layer": layer, "identifier": elem_l[0].token,
                "type": "NULL", "using": True
            }
            # Проверка на переопределение значений по умолчанию
            if is_to_array(vrbl, semantic['const']['var'], layer) or is_to_array(vrbl, semantic['const']['func'],
                                                                                 layer):
                return False, [{"type": "E", "message": "Redeclaring a variable", "identifier": name + " for"}]
            # Проверка на соответствие типов
            vrbl_type = get_type_list(get_type_expression(elem_r, semantic, layer))
            if vrbl_type == "NULL" or vrbl_type == "NONE":
                if vrbl_type == "NULL":
                    return False, [{"type": "E", "message": "Expression contains multiple types", "identifier": name + " for"}]
                else:
                    return False, [{"type": "E", "message": "Unknown variable", "identifier": name + " for"}]
            vrbl['type'] = vrbl_type
            # Проверка на переопределение
            if is_to_array(vrbl, semantic['var']['func'], layer):
                return False, [{"type": "E", "message": "Redeclaring a variable", "identifier": name + " for"}]
            semantic['var']['var'].append(vrbl)
        else:
            return False, [{"type": "E", "message": "The first element is the counter declaration", "identifier": name + " for"}]

        vrbl_type = get_type_list(get_type_expression(code.data[2].data[0].data, semantic, layer))
        if vrbl_type == "NULL" or vrbl_type == "NONE":
            if vrbl_type == "NULL":
                return False, [{"type": "E", "message": "Expression contains multiple types", "identifier": name + " for"}]
            else:
                return False, [{"type": "E", "message": "Unknown variable", "identifier": name + " for"}]

        if len(code.data[3].data) == 2 or len(code.data[3].data) == 3:
            elem_l = code.data[3].data[0]
            elem_r = code.data[3].data[-1]
            if not isinstance(elem_l.data[0], Lexer.Token):
                return False, [{"type": "E", "message": "Not identifier", "identifier": name + " for"}]
            if len(code.data[3].data) == 2:
                if not isinstance(elem_r, Lexer.Token):
                    return False, [{"type": "E", "message": "The third element is the counter increment",
                                    "identifier": name + " for"}]
                vrbl_type = get_type_list(get_type_expression(elem_l.data, semantic, layer))
                if vrbl_type == "NULL" or vrbl_type == "NONE":
                    if vrbl_type == "NULL":
                        return False, [{"type": "E", "message": "Expression contains multiple types",
                                        "identifier": name + " for"}]
                    else:
                        return False, [{"type": "E", "message": "Unknown variable", "identifier": name + " for"}]
            else:
                vrbl_type = get_type_list(get_type_expression(elem_l.data, semantic, layer))
                if vrbl_type == "NULL" or vrbl_type == "NONE":
                    if vrbl_type == "NULL":
                        return False, [{"type": "E", "message": "Expression contains multiple types",
                                        "identifier": name + " for"}]
                    else:
                        return False, [{"type": "E", "message": "Unknown variable", "identifier": name + " for"}]
                vrbl_type = get_type_list(get_type_expression(elem_r.data, semantic, layer))
                if vrbl_type == "NULL" or vrbl_type == "NONE":
                    if vrbl_type == "NULL":
                        return False, [{"type": "E", "message": "Expression contains multiple types",
                                        "identifier": name + " for"}]
                    else:
                        return False, [{"type": "E", "message": "Unknown variable", "identifier": name + " for"}]
        else:
            return False, [{"type": "E", "message": "The third element is the counter increment", "identifier": name + " for"}]

        stp = 4
    else:
        vrbl_type = get_type_list(get_type_expression(code.data[1].data[0].data, semantic, layer))
        if vrbl_type == "NULL" or vrbl_type == "NONE":
            if vrbl_type == "NULL":
                return False, [{"type": "E", "message": "Expression contains multiple types", "identifier": name + " for"}]
            else:
                return False, [{"type": "E", "message": "Unknown variable", "identifier": name + " for"}]

        stp = 2

    analysis, dlt_code = block(code.data[stp:], name + " for", func_type, semantic, layer, "cycle")
    analysis_result.extend(analysis)
    clear_semantic_var(semantic, layer)

    dlt_code = sorted(list(set(dlt_code)))
    for i in range(len(dlt_code) - 1, -1, -1):
        if dlt_code[i] >= 0:
            del code.data[dlt_code[i] + stp]

    if len(code.data) > stp:
        return True, analysis_result
    return False, analysis_result
