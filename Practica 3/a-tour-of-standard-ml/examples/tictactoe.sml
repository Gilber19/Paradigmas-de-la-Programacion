(* Definición del tipo de datos para el jugador *)
datatype Player = X | O | Empty;

(* Definición del tipo de datos para el tablero *)
type Board = Player list list;

(* Función para inicializar un tablero vacío *)
fun initBoard () = [[Empty, Empty, Empty], [Empty, Empty, Empty], [Empty, Empty, Empty]];

(* Función para imprimir el tablero *)
fun printBoard (board : Board) =
    let
        fun printRow [] = print "\n"
          | printRow (x::xs) = (case x of
                                    X => (print " X " ; printRow xs)
                                  | O => (print " O " ; printRow xs)
                                  | Empty => (print "   " ; printRow xs))
    in
        List.app printRow board
    end;

(* Función para realizar una jugada *)
fun makeMove (board : Board) player row col =
    if row < 0 orelse row > 2 orelse col < 0 orelse col > 2 then
        (print "Posición inválida. Por favor, elige una posición dentro del rango.\n"; board)
    else if List.nth(List.nth board row, col) <> Empty then
        (print "La casilla ya está ocupada. Por favor, elige otra posición.\n"; board)
    else
        let
            fun replaceAtIndex (lst, index, newval) =
                List.take (lst, index) @ newval :: List.drop (lst, index + 1)
        in
            replaceAtIndex(board, row, replaceAtIndex(List.nth(board, row), col, player))
        end;

(* Función para verificar si hay un ganador *)
fun checkWinner (board : Board) =
    let
        fun checkRows [] = false
          | checkRows (row::rest) =
                if List.all (fn x => x = X) row orelse List.all (fn x => x = O) row then true
                else checkRows rest
        fun checkColumns board = checkRows (List.transpose board)
        fun checkDiagonals board =
            let
                val diag1 = [List.nth(List.nth board 0, 0), List.nth(List.nth board 1, 1), List.nth(List.nth board 2, 2)]
                val diag2 = [List.nth(List.nth board 0, 2), List.nth(List.nth board 1, 1), List.nth(List.nth board 2, 0)]
            in
                List.all (fn x => x = X) diag1 orelse List.all (fn x => x = O) diag1 orelse
                List.all (fn x => x = X) diag2 orelse List.all (fn x => x = O) diag2
            end
    in
        checkRows board orelse checkColumns board orelse checkDiagonals board
    end;

(* Función principal para el juego del gato *)
fun playTicTacToe () =
    let
        val mutable board = initBoard ();
        val mutable currentPlayer = X;
        val rec playGame = fn () =>
            (printBoard board;
             if checkWinner board then
                (print ("¡El jugador " ^ (case currentPlayer of X => "X" | O => "O") ^ " ha ganado!\n");
                 playAgain())
             else if List.exists (fn row => List.exists (fn cell => cell = Empty) row) board then
                let
                    val (row, col) = getPlayerMove currentPlayer
                in
                    board := makeMove (!board) currentPlayer row col;
                    currentPlayer := if currentPlayer = X then O else X;
                    playGame()
                end
             else
                (print "¡Empate!\n";
                 playAgain()))
        and getPlayerMove player =
            let
                val rec getCoord = fn (message : string) =>
                    (print message;
                     case (Int.fromString (TextIO.inputLine TextIO.stdIn)) of
                         NONE => (print "Entrada inválida. Inténtalo de nuevo.\n"; getCoord message)
                       | SOME n => if n >= 0 andalso n <= 2 then n else (print "Número fuera de rango. Inténtalo de nuevo.\n"; getCoord message))
            in
                print ("Jugador " ^ (case player of X => "X" | O => "O") ^ ", ingresa la fila (0-2): ");
                val row = getCoord "";
                print ("Jugador " ^ (case player of X => "X" | O => "O") ^ ", ingresa la columna (0-2): ");
                val col = getCoord "";
                (row, col)
            end
        and playAgain () =
            let
                fun getChoice () =
                    (print "¿Quieres jugar de nuevo? (s/n): ";
                     case String.fromString (String.str (TextIO.inputLine TextIO.stdIn)) of
                         NONE => (print "Entrada inválida. Por favor, ingresa 's' para sí o 'n' para no.\n"; getChoice ())
                       | SOME "s" => playTicTacToe ()
                       | SOME "n" => print "¡Gracias por jugar!\n"
                       | _ => (print "Opción no reconocida. Por favor, ingresa 's' para sí o 'n' para no.\n"; getChoice ()))
            in
                getChoice ()
            end
    in
        playGame ()
    end;
