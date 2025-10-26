import java.rmi.Remote;
import java.rmi.RemoteException;

public interface CalculadoraInterface extends Remote {
    public int soma(int num1, int num2) throws RemoteException;
    public int subtracao(int num1, int num2) throws RemoteException;
    public int multiplicacao(int num1, int num2) throws RemoteException;
    public double divisao(int num1, int num2) throws RemoteException;
}
