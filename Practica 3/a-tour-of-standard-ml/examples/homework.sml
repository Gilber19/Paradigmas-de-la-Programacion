(* Ejemplo 1: Reducción de expresiones aritméticas *)

(* Definición de tipos de datos para expresiones aritméticas *)
datatype ExpresionAritmetica = Valor of int
                            | Suma of ExpresionAritmetica * ExpresionAritmetica
                            | Multiplicacion of ExpresionAritmetica * ExpresionAritmetica;

(* Función para reducir una expresión aritmética *)
fun reducirExpresion (Suma(a, b)) = Multiplicacion(reducirExpresion(a), reducirExpresion(b))
  | reducirExpresion (Valor(n)) = Valor(n)
  | reducirExpresion (Multiplicacion(a, b)) = Multiplicacion(reducirExpresion(a), reducirExpresion(b));

(* Ejemplo de expresión aritmética: (3 + 4) * 2 *)
val expresion = Multiplicacion(Suma(Valor 3, Valor 4), Valor 2);

(* Reducción de la expresión *)
val resultado = reducirExpresion expresion;

(* Ejemplo 2: Reducción de expresiones lambda *)

(* Definición de tipos de datos para expresiones lambda *)
datatype ExpresionLambda = Variable of string
                         | LambdaAbstraccion of string * ExpresionLambda
                         | Aplicacion of ExpresionLambda * ExpresionLambda;

(* Función para reducir una expresión lambda *)
fun reducirExpresionLambda (Aplicacion(LambdaAbstraccion(x, M), N)) = sustituirVariable(M, x, N)
  | reducirExpresionLambda (Aplicacion(M, N)) = Aplicacion(reducirExpresionLambda(M), reducirExpresionLambda(N))
  | reducirExpresionLambda (Variable(x)) = Variable(x);

(* Función para sustituir una variable por otra en una expresión *)
fun sustituirVariable (Variable(x), y, N) = if x = y then N else Variable(x)
  | sustituirVariable (LambdaAbstraccion(x, M), y, N) = if x = y then LambdaAbstraccion(x, M) else LambdaAbstraccion(x, sustituirVariable(M, y, N))
  | sustituirVariable (Aplicacion(M, N), y, P) = Aplicacion(sustituirVariable(M, y, P), sustituirVariable(N, y, P));

(* Ejemplo de expresión lambda: (\x. x + 1) 2 *)
val expresionLambda = Aplicacion(LambdaAbstraccion("x", Aplicacion(Variable "x", Variable "x")), Variable "2");

(* Reducción de la expresión *)
val resultadoLambda = reducirExpresionLambda expresionLambda;
