import java.rmi.Naming;

public class Cliente {
    public static void main(String[] args) {
        try {
            CalculadoraInterface interface_calculadora = (CalculadoraInterface) Naming.lookup("rmi://localhost:1099/Calculadora");

            System.out.println("A soma é: " + interface_calculadora.soma(34, 21));
            System.out.println("A Subtração: é " + interface_calculadora.subtracao(86, 43));
            System.out.println("A Multiplicação é: " + interface_calculadora.multiplicacao(74, 3));
            System.out.println("A Divisão é: " + interface_calculadora.divisao(64, 2));
        } catch (Exception e) {
            System.err.println("Erro no cliente: " + e);
        }
    }
}
