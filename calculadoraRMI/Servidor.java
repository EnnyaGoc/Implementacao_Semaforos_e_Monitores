import java.rmi.Naming;

public class Servidor {
    public static void main(String[] args) {
        try {
            CalculadoraInterface interface_calculadora = new Calculadora();
            Naming.rebind("rmi://localhost:1099/Calculadora", interface_calculadora);
            System.out.println("Servidor da calculadora está funcionando!");
        } catch (Exception e) {
            System.err.println("Erro no servidor: " + e);
        }
    }
}
