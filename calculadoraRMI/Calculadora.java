import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;

public class Calculadora extends UnicastRemoteObject implements CalculadoraInterface {

    public Calculadora() throws RemoteException {
        super();
    }

    public int soma(int num1, int num2) {
        return num1 + num2;
    }

    public int subtracao(int num1, int num2) {
        return num1 - num2;
    }

    public int multiplicacao(int num1, int num2) {
        return num1 * num2;
    }

    public double divisao(int num1, int num2) {
        if (num2 == 0){
            return "Não é possível dividir por zero";
        }
        return (double) num1 / num2;
    }
}
