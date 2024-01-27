# * SourceFile		    ::= PackageClause ";" *** { TopLevelDecl ";" *** }
# * PackageClause		::= "package" identifier
# * TopLevelDecl		::= Declaration | FunctionDecl
# * Declaration		    ::= ConstDecl | VarDecl
# * ConstDecl			::= "const" Identifier [ Type ] "=" Expression
# * VarDecl			    ::= "var" Identifier [ Type ] "=" Expression
# * Type				::= identifier | ArrayType | "(" Type ")"
# * ArrayType			::= "[" Expression "]" Type
# * FunctionDecl		::= "func" identifier Signature Block
# * Signature			::= "(" [ ParameterList ] ")" [ Type ]
# * ParameterList		::= ParameterDecl { "," ParameterDecl }
# * ParameterDecl		::= IdentifierList Type
# * Block				::= "{" StatementList "}"
# * StatementList		::= *** { Statement ";" *** }
# * Statement			::= Declaration | SimpleStmt | "continue" | "break" |
#                           "return" [ Expression ] | IfStmt | SwitchStmt | ForStmt
# * SimpleStmt		    ::= Expression ( [ "++" | "--" ] | assign_op *** Expression | ":=" *** Expression )
# * Expression		    ::= UnaryExpr [ binary_op Expression ]
# * ExpressionList	    ::= Expression { "," Expression }
# * IdentifierList  	::= identifier { "," identifier }
# * Operand			::= identifier | int_lit | float_lit | string_lit | "(" Expression ")"
# * PrimaryExpr		::= Operand [ { "." identifier | "[" Expression "]" | "(" [ ExpressionList ] ")"} ]
# * UnaryExpr			::= PrimaryExpr | unary_op UnaryExpr
# IfStmt			::= "if" Expression Block [ "else" ( IfStmt | Block ) ]
# SwitchStmt		::= "switch" Expression "{" *** { ExprCaseClause *** } "}"
# ExprCaseClause	::= ( "case" ExpressionList | "default" ) ":" StatementList
# ForStmt			::= "for" ( Expression | SimpleStmt ";" Expression ";" SimpleStmt ) Block
