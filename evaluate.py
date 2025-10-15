from copy import copy
from lexer import *
from parser_ import *

def evaluate(tree: all_node | None) -> Any:
    if isinstance(tree, BNode):
        left_node = evaluate(tree.l_node)
        right_node = evaluate(tree.r_node)

        if isinstance(tree, AddNode):
            if isinstance(left_node, VariableNode) and isinstance(right_node, VariableNode):
                if left_node.value.value != right_node.value.value:
                    raise Exception("Two variables are not supported yet")
                temp_coef = evaluate(AddNode(left_node.coefficient, right_node.coefficient))
                if temp_coef.value.value == 0:
                    return ConstantNode(Constant(TokenType.CONSTANT, 0 , False))
                return VariableNode(left_node.value, temp_coef)

            elif isinstance(left_node, AddNode) and isinstance(right_node, AddNode):
                if isinstance(left_node.l_node, VariableNode) and isinstance(right_node.l_node, VariableNode):
                    return evaluate(AddNode(AddNode(left_node.l_node, right_node.l_node), AddNode(left_node.r_node, right_node.r_node)))
                elif isinstance(left_node.l_node, VariableNode) and isinstance(right_node.r_node, VariableNode):
                    return evaluate(AddNode(AddNode(left_node.l_node, right_node.r_node), AddNode(left_node.r_node, right_node.l_node)))
                elif isinstance(left_node.r_node, VariableNode) and isinstance(right_node.l_node, VariableNode):
                    return evaluate(AddNode(AddNode(left_node.r_node, right_node.l_node), AddNode(left_node.l_node, right_node.r_node)))
                elif isinstance(left_node.r_node, VariableNode) and isinstance(right_node.r_node, VariableNode):
                    return evaluate(AddNode(AddNode(left_node.r_node, right_node.r_node), AddNode(left_node.l_node, right_node.l_node)))

            elif isinstance(left_node, VariableNode) and isinstance(right_node, AddNode):
                if isinstance(right_node.l_node, VariableNode):
                    return evaluate(AddNode(AddNode(left_node, right_node.l_node), right_node.r_node))
                elif isinstance(right_node.r_node, VariableNode):
                    return evaluate(AddNode(right_node.l_node, AddNode(left_node, right_node.r_node)))
            
            elif isinstance(right_node, VariableNode) and isinstance(left_node, AddNode):
                if isinstance(left_node.l_node, VariableNode):
                    return evaluate(AddNode(AddNode(right_node, left_node.l_node), left_node.r_node))
                elif isinstance(left_node.r_node, VariableNode):
                    return evaluate(AddNode(left_node.l_node, AddNode(right_node, left_node.r_node)))

            elif isinstance(left_node, ConstantNode) and isinstance(right_node, AddNode):
                if isinstance(right_node.l_node, ConstantNode):
                    return evaluate(AddNode(AddNode(left_node, right_node.l_node), right_node.r_node))
                elif isinstance(right_node.r_node, ConstantNode):
                    return evaluate(AddNode(right_node.l_node, AddNode(left_node, right_node.r_node)))
            
            elif isinstance(right_node, ConstantNode) and isinstance(left_node, AddNode):
                if isinstance(left_node.l_node, ConstantNode):
                    return evaluate(AddNode(AddNode(right_node, left_node.l_node), left_node.r_node))
                elif isinstance(left_node.r_node, ConstantNode):
                    return evaluate(AddNode(left_node.l_node, AddNode(right_node, left_node.r_node)))

            elif isinstance(left_node, ConstantNode) and isinstance(right_node, ConstantNode):
                return ConstantNode(Constant(TokenType.CONSTANT, float(left_node.value.value) + float(right_node.value.value), right_node.value.float | left_node.value.float))

            elif isinstance(left_node, ConstantNode):
                if left_node.value.value == 0:
                    return right_node
                
            elif isinstance(right_node, ConstantNode):
                if right_node.value.value == 0:
                    return left_node

            if isinstance(left_node, DivideNode):
                return DivideNode(evaluate(AddNode(left_node.l_node, MultiplyNode(left_node.r_node, right_node))), left_node.r_node)
            
            elif isinstance(right_node, DivideNode):
                return DivideNode(evaluate(AddNode(right_node.l_node, MultiplyNode(right_node.r_node, left_node))), right_node.r_node)    

            return AddNode(left_node, right_node)

        elif isinstance(tree, SubtractNode):

            return evaluate(AddNode(left_node, MinusNode(right_node)))
            
        elif isinstance(tree, MultiplyNode):

            if isinstance(left_node, VariableNode) and isinstance(right_node, VariableNode):
                if left_node.value.value != right_node.value.value:
                    raise Exception("Two different variables are not supported yet")
                raise Exception("Quadratic equation is not supported yet")
            
            elif isinstance(left_node, BNode) and isinstance(right_node, BNode):
                if isinstance(left_node, AddNode) and isinstance(right_node, AddNode):
                    return evaluate(AddNode(AddNode(MultiplyNode(left_node.l_node, right_node.l_node), MultiplyNode(left_node.l_node, right_node.r_node)), AddNode(MultiplyNode(left_node.r_node, right_node.l_node), MultiplyNode(left_node.r_node, right_node.r_node))))

                elif isinstance(left_node, DivideNode) and isinstance(right_node, AddNode):
                    return DivideNode(evaluate(MultiplyNode(left_node.l_node, right_node)), left_node.r_node)

                elif isinstance(right_node, DivideNode) and isinstance(left_node, AddNode):
                    return DivideNode(evaluate(MultiplyNode(right_node.l_node, left_node)), right_node.r_node)

                elif isinstance(left_node, DivideNode) and isinstance(right_node, DivideNode):
                    left_node.l_node = evaluate(DivideNode(left_node.l_node, right_node.r_node))
                    right_node.r_node = ConstantNode(Constant(TokenType.CONSTANT, 1, False))
                    right_node.l_node = evaluate(DivideNode(right_node.l_node, left_node.r_node))
                    left_node.r_node = right_node.r_node
                    return evaluate(DivideNode(MultiplyNode(left_node.l_node, right_node.l_node), MultiplyNode(left_node.r_node, right_node.r_node)))

            elif isinstance(left_node, VariableNode):
                if isinstance(right_node, BNode):
                    temp_left_node = evaluate(MultiplyNode(left_node, right_node.l_node))
                    temp_right_node = right_node.r_node

                    if isinstance(right_node, MultiplyNode) == False and isinstance(right_node, DivideNode) == False:
                        temp_right_node = evaluate(MultiplyNode(left_node, right_node.r_node))

                    right_node.l_node = temp_left_node
                    right_node.r_node = temp_right_node

                    return evaluate(right_node)

                return VariableNode(left_node.value, evaluate(MultiplyNode(left_node.coefficient, right_node)))

            elif isinstance(right_node, VariableNode):
                if isinstance(left_node, BNode):
                    temp_left_node = evaluate(MultiplyNode(right_node, left_node.l_node))
                    temp_right_node = left_node.r_node

                    if isinstance(left_node, MultiplyNode) == False and isinstance(left_node, DivideNode) == False:
                        temp_right_node = evaluate(MultiplyNode(right_node, left_node.r_node))

                    left_node.l_node = temp_left_node
                    left_node.r_node = temp_right_node

                    return evaluate(left_node)
                
                return VariableNode(right_node.value, evaluate(MultiplyNode(right_node.coefficient, left_node)))

            elif isinstance(left_node, ConstantNode) and isinstance(right_node, ConstantNode):
                return ConstantNode(Constant(TokenType.CONSTANT, float(left_node.value.value) * float(right_node.value.value), left_node.value.float | right_node.value.float))

            elif isinstance(left_node, ConstantNode):
                if isinstance(right_node, BNode):
                    temp_left_node = evaluate(MultiplyNode(left_node, right_node.l_node))
                    temp_right_node = right_node.r_node

                    if isinstance(right_node, MultiplyNode) == False and isinstance(right_node, DivideNode) == False:
                        temp_right_node = evaluate(MultiplyNode(left_node, right_node.r_node))

                    right_node.l_node = temp_left_node
                    right_node.r_node = temp_right_node

                    return evaluate(right_node)
            
            elif isinstance(right_node, ConstantNode):
                if isinstance(left_node, BNode):
                    temp_left_node = evaluate(MultiplyNode(right_node, left_node.l_node))
                    temp_right_node = left_node.r_node

                    if isinstance(left_node, MultiplyNode) == False and isinstance(left_node, DivideNode) == False:
                        temp_right_node = evaluate(MultiplyNode(right_node, left_node.r_node))

                    left_node.l_node = temp_left_node
                    left_node.r_node = temp_right_node

                    return evaluate(left_node)

        elif isinstance(tree, DivideNode):

            if isinstance(left_node, VariableNode) and isinstance(right_node, VariableNode):
                if left_node.value.value != right_node.value.value:
                    raise Exception("Two different variables are not supported yet")
                return ConstantNode(Constant(TokenType.CONSTANT, float(left_node.coefficient.value.value) / float(right_node.coefficient.value.value), False))

            elif left_node == right_node:
                return ConstantNode(Constant(TokenType.CONSTANT, 1.0, True))

            elif isinstance(left_node, VariableNode):
                temp = evaluate(DivideNode(left_node.coefficient, right_node))
                if isinstance(temp, DivideNode):
                    return DivideNode(left_node, right_node)
                return VariableNode(left_node.value, temp)

            elif isinstance(right_node, VariableNode):
                temp = copy(right_node)
                temp.coefficient = ConstantNode(Constant(TokenType.CONSTANT, 1, False))
                return DivideNode(evaluate(DivideNode(left_node, right_node.coefficient)), temp)

            elif isinstance(left_node, ConstantNode) and isinstance(right_node, ConstantNode):
                return ConstantNode(Constant(TokenType.CONSTANT, float(left_node.value.value) / float(right_node.value.value), left_node.value.float | right_node.value.float))

            elif isinstance(right_node, ConstantNode):
                if right_node.value.value == 1:
                    return left_node
                elif isinstance(left_node, BNode):
                    left_node.l_node = evaluate(DivideNode(left_node.l_node, right_node))
                    temp_right_node = evaluate(DivideNode(left_node.r_node, right_node))

                    if isinstance(left_node, DivideNode):
                        temp_right_node = left_node.r_node

                    left_node.r_node = temp_right_node

                    return left_node

            elif isinstance(left_node, AddNode) and isinstance(right_node, AddNode):
                if isinstance(left_node.l_node, VariableNode) and isinstance(right_node.l_node, VariableNode):
                    temp_coef = evaluate(DivideNode(left_node.l_node, right_node.l_node))

                    if evaluate(DivideNode(left_node.r_node, right_node.r_node)) == temp_coef:
                        return temp_coef
                elif isinstance(left_node.l_node, VariableNode) and isinstance(right_node.r_node, VariableNode):
                    temp_coef = evaluate(DivideNode(left_node.l_node, right_node.r_node))

                    if evaluate(DivideNode(left_node.r_node, right_node.l_node)) == temp_coef:
                        return temp_coef
                elif isinstance(left_node.r_node, VariableNode) and isinstance(right_node.l_node, VariableNode):
                    temp_coef = evaluate(DivideNode(left_node.r_node, right_node.l_node))

                    if evaluate(DivideNode(left_node.l_node, right_node.r_node)) == temp_coef:
                        return temp_coef
                elif isinstance(left_node.r_node, VariableNode) and isinstance(right_node.r_node, VariableNode):
                    temp_coef = evaluate(DivideNode(left_node.r_node, right_node.r_node))

                    if evaluate(DivideNode(left_node.l_node, right_node.l_node)) == temp_coef:
                        return temp_coef

            elif isinstance(left_node, DivideNode) and isinstance(right_node, DivideNode):
                right_node.l_node, right_node.r_node = right_node.r_node, right_node.l_node
                left_node.l_node = evaluate(DivideNode(left_node.l_node, right_node.r_node))
                right_node.r_node = ConstantNode(Constant(TokenType.CONSTANT, 1, False))
                right_node.l_node = evaluate(DivideNode(right_node.l_node, left_node.r_node))
                left_node.r_node = right_node.r_node
                return evaluate(DivideNode(MultiplyNode(left_node.l_node, right_node.l_node), MultiplyNode(left_node.r_node, right_node.r_node)))

            elif isinstance(right_node, DivideNode):
                right_node.l_node, right_node.r_node = right_node.r_node, right_node.l_node
                return evaluate(MultiplyNode(left_node, right_node))

            return DivideNode(left_node, right_node)

    elif isinstance(tree, Node):
        if isinstance(tree, ConstantNode):
            return tree
        elif isinstance(tree, VariableNode):
            if isinstance(tree.coefficient, ConstantNode):
                if tree.coefficient.value.value == 0:
                    return ConstantNode(Constant(TokenType.CONSTANT, 0 , False))
                return tree
            elif isinstance(tree.coefficient, BNode):
                tree.coefficient = evaluate(tree.coefficient)

                if isinstance(tree.coefficient, BNode):
                    return evaluate(MultiplyNode(VariableNode(tree.value, ConstantNode(Constant(TokenType.CONSTANT, 1, False))), tree.coefficient))

                return evaluate(MultiplyNode(tree.coefficient, VariableNode(tree.value, ConstantNode(Constant(TokenType.CONSTANT, 1, False)))))
        elif isinstance(tree, PlusNode):
            return evaluate(tree.value)
        elif isinstance(tree, MinusNode):
            temp_value = evaluate(tree.value)
            if isinstance(temp_value, ConstantNode):
                temp_value.value.value = -float(temp_value.value.value)
            elif isinstance(temp_value, VariableNode):
                temp_value.coefficient.value.value = -float(temp_value.coefficient.value.value)
            else:
                if isinstance(temp_value, ConstantNode):
                    temp_value.value.value = -float(temp_value.value.value)
                elif isinstance(temp_value, VariableNode):
                    temp_value.coefficient.value.value = -float(temp_value.coefficient.value.value)
                
                    return temp_value
                elif isinstance(temp_value, AddNode):
                    return AddNode(evaluate(MinusNode(temp_value.l_node)), evaluate(MinusNode(temp_value.r_node)))
                elif isinstance(temp_value, DivideNode):
                    return DivideNode(evaluate(MinusNode(temp_value.l_node)), temp_value.r_node)
            return temp_value
        
    return ConstantNode(Constant(TokenType.CONSTANT, 0, False))